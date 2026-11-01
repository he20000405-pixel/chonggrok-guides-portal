# Publishing

## Cloudflare Pages

1. Connect the GitHub repository `he20000405-pixel/chonggrok-guides-portal`.
2. Select `main` as the production branch.
3. Use `bundle exec jekyll build` as the build command.
4. Use `_site` as the output directory.
5. Set `RUBY_VERSION` to a Cloudflare-supported Ruby 3.x release.
6. Verify the generated `pages.dev` site before adding a custom domain.
7. Add `guides.chonggrok.com` through Pages > Custom domains. Do not create the DNS record manually first.

## Safety boundary

Only the `guides` subdomain may be created for this project. Do not modify apex, `www`, MX, NS, TXT, DNSSEC, SSL/TLS mode, Workers routes, redirects, cache rules, WAF rules, login, payment or verification settings.

## GitHub sitemap mirror maintenance

After publishing content updates to the GitHub knowledge bases, the maintainer must run `python scripts/sync_github_sitemaps.py --check`. Default mode is also read-only: exit 0 means the six local mirror files match, 1 means they are outdated or missing, and 2 means fetching, validation or writing failed.

To refresh them, run `python scripts/sync_github_sitemaps.py --write`, then run `--check` again. The script only reads the five fixed GitHub sitemap URLs, validates all responses before writing, and preserves their original bytes, article URLs and dates. Replacements are atomic per file with rollback on caught failures; after interruption, verify the files before publishing.

Review the diff, build the portal, publish through the existing Cloudflare Pages integration, and verify both the deployed XML and Google's successful sitemap reading. Keep the portal's original sitemap, robots, articles and domain settings unchanged. The script is manual: it does not run automatically, commit, deploy, submit to Google, or guarantee indexing.

