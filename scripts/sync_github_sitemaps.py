#!/usr/bin/env python3
"""Manually validate/check or update the five GitHub sitemap mirrors.

Default/--check never writes files. --write validates every remote response first,
stages complete replacements, then uses per-file atomic replacement with rollback
on a caught failure. A machine crash is not a six-file transaction: always run
--check and review the diff before publishing. No scheduler or deployment is run.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from urllib.parse import unquote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://he20000405-pixel.github.io"
MIRROR = "https://guides.chonggrok.com"
ROUTES = {
    "portal": "/",
    "chatgpt": "/chatgpt-plus-pro-china-guide/",
    "grok": "/supergrok-china-guide/",
    "claude": "/claude-pro-max-china-guide/",
    "gemini": "/gemini-google-ai-pro-china-guide/",
}
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
MAX_BYTES = 50 * 1024 * 1024
DATE = re.compile(r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?\Z")


class SyncError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_map(alias, data):
    if alias not in ROUTES or not data or len(data) > MAX_BYTES:
        raise SyncError("Unexpected source map or empty/oversized XML")
    try:
        data.decode("utf-8-sig", errors="strict")
        if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
            raise ValueError("DTD/entity declarations are not permitted")
        root = ET.fromstring(data)
    except (UnicodeError, ET.ParseError, ValueError) as error:
        raise SyncError(f"{alias}: invalid UTF-8 XML: {error}") from error
    if root.tag != NS + "urlset" or not 0 < len(root) <= 50000:
        raise SyncError(f"{alias}: invalid sitemap namespace/root or URL count")
    urls = []
    for entry in root:
        locations = entry.findall(NS + "loc")
        if entry.tag != NS + "url" or len(locations) != 1 or not locations[0].text:
            raise SyncError(f"{alias}: each URL entry needs exactly one loc")
        loc = locations[0].text
        parsed = urlsplit(loc)
        decoded_path = unquote(parsed.path)
        product_routes = tuple(route for name, route in ROUTES.items() if name != "portal")
        if (len(loc) > 2048 or any(c.isspace() for c in loc)
                or parsed.scheme != "https" or parsed.netloc != "he20000405-pixel.github.io"
                or not parsed.path.startswith(ROUTES[alias]) or parsed.query or parsed.fragment
                or not decoded_path.startswith(ROUTES[alias])
                or (alias == "portal" and any(decoded_path == route.rstrip("/") or decoded_path.startswith(route) for route in product_routes))
                or any(part in (".", "..") for part in decoded_path.split("/"))):
            raise SyncError(f"{alias}: URL is outside its canonical HTTPS scope: {loc}")
        modified = entry.findall(NS + "lastmod")
        if len(modified) > 1:
            raise SyncError(f"{alias}: repeated lastmod: {loc}")
        for node in modified:
            value = node.text or ""
            try:
                if not DATE.fullmatch(value):
                    raise ValueError("use a W3C date or timezone-qualified datetime")
                date = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if date.tzinfo is None:
                    date = date.replace(tzinfo=timezone.utc)
                if date > datetime.now(timezone.utc):
                    raise ValueError("lastmod is in the future")
            except ValueError as error:
                raise SyncError(f"{alias}: invalid lastmod {value!r}: {error}") from error
        urls.append(loc)
    if len(urls) != len(set(urls)):
        raise SyncError(f"{alias}: duplicate loc values")
    return urls


def fetch_all():
    opener = build_opener(NoRedirect())
    payloads, combined, counts = {}, set(), {}
    for alias, route in ROUTES.items():
        url = ORIGIN + route + "sitemap.xml"
        request = Request(url, headers={"Accept-Encoding": "identity", "User-Agent": "ChongGrok-sitemap-sync/1.0"})
        with opener.open(request, timeout=30) as response:
            if (response.status != 200 or response.url != url
                    or response.headers.get_content_type() not in ("application/xml", "text/xml")
                    or response.headers.get("Content-Encoding", "identity").lower() != "identity"):
                raise SyncError(f"{alias}: unexpected HTTP status, redirect, MIME or content encoding")
            data = response.read(MAX_BYTES + 1)
        urls = validate_map(alias, data)
        if combined.intersection(urls):
            raise SyncError(f"{alias}: duplicate URL across source sitemaps")
        combined.update(urls)
        counts[alias] = len(urls)
        payloads[f"github-sitemaps/{alias}.xml"] = data
    index = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    index += "".join(f"  <sitemap><loc>{MIRROR}/github-sitemaps/{alias}.xml</loc></sitemap>\n" for alias in ROUTES)
    index += "</sitemapindex>\n"
    payloads["github-sitemap-index.xml"] = index.encode("utf-8")
    return payloads, counts, len(combined)


def targets(root, payloads):
    root = root.resolve()
    allowed = {f"github-sitemaps/{alias}.xml" for alias in ROUTES} | {"github-sitemap-index.xml"}
    if set(payloads) != allowed:
        raise SyncError("Only the six fixed mirror files may be updated")
    result = {}
    for relative in payloads:
        path = root / relative
        if (path.is_symlink() or not path.resolve().is_relative_to(root)
                or path.parent.is_symlink() or not path.parent.is_dir()
                or (path.exists() and not path.is_file())):
            raise SyncError(f"Unsafe or missing mirror directory: {relative}")
        result[relative] = path
    return result


def stage(path, data, mode):
    fd, name = tempfile.mkstemp(prefix=".sitemap-sync-", suffix=".tmp", dir=path.parent)
    staged = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(staged, mode)
        return staged
    except BaseException:
        staged.unlink(missing_ok=True)
        raise


def write_validated(root, payloads):
    paths = targets(root, payloads)
    lock = root / ".github-sitemap-sync.lock"
    temporary, replaced, backups = [], [], {}
    incomplete_rollback = False
    try:
        handle = lock.open("x", encoding="utf-8")
    except FileExistsError as error:
        raise SyncError("Another sync or an interrupted sync holds .github-sitemap-sync.lock; inspect it before retrying") from error
    try:
        with handle:
            handle.write(str(os.getpid()) + "\n")
        old = {rel: path.read_bytes() if path.exists() else None for rel, path in paths.items()}
        changed = [rel for rel in payloads if old[rel] != payloads[rel]]
        staged = {}
        for rel in changed:
            path = paths[rel]
            mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
            staged[rel] = stage(path, payloads[rel], mode)
            temporary.append(staged[rel])
            if old[rel] is not None:
                backups[rel] = stage(path, old[rel], mode)
                temporary.append(backups[rel])
        try:
            for rel in changed:
                path = paths[rel]
                if (path.read_bytes() if path.exists() else None) != old[rel]:
                    raise SyncError(f"Concurrent change detected: {rel}")
                os.replace(staged[rel], path)
                replaced.append(rel)
            if any(paths[rel].read_bytes() != payloads[rel] for rel in payloads):
                raise SyncError("Read-back did not match the validated payloads")
        except BaseException as error:
            rollback_errors = []
            for rel in reversed(replaced):
                try:
                    if paths[rel].read_bytes() != payloads[rel]:
                        raise SyncError("file was changed by another process")
                    if old[rel] is None:
                        paths[rel].unlink()
                    else:
                        os.replace(backups[rel], paths[rel])
                except Exception as rollback_error:
                    rollback_errors.append(f"{rel}: {rollback_error}")
            if rollback_errors:
                incomplete_rollback = True
                preserved = [str(path) for path in backups.values() if path.exists()]
                raise SyncError("Write failed; inspect incomplete rollback before publishing: " + "; ".join(rollback_errors)
                                + ". Recovery backups retained: " + ", ".join(preserved)
                                + ". Lock retained: " + str(lock)) from error
            raise
        return changed
    finally:
        for path in temporary:
            if not incomplete_rollback or path not in backups.values():
                path.unlink(missing_ok=True)
        if not incomplete_rollback:
            lock.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only comparison (default)")
    mode.add_argument("--write", action="store_true", help="update validated mirrors locally; does not publish")
    args = parser.parse_args(argv)
    try:
        payloads, counts, total = fetch_all()
        paths = targets(ROOT, payloads)
        stale = [rel for rel, path in paths.items() if not path.exists() or path.read_bytes() != payloads[rel]]
        print("Validated source URLs: " + ", ".join(f"{alias}={count}" for alias, count in counts.items()) + f"; unique total={total}")
        if not stale:
            print("All six local mirrors match; no files changed.")
            return 0
        if not args.write:
            print("Outdated/missing mirrors (read-only check): " + ", ".join(stale))
            return 1
        changed = write_validated(ROOT, payloads)
        for rel in changed:
            print("Updated " + rel + " sha256=" + hashlib.sha256(payloads[rel]).hexdigest())
        print("Local update complete. Review, build, deploy, and check Google sitemap processing separately.")
        return 0
    except Exception as error:
        print("Sitemap sync failed: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
