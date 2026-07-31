import { chromium } from "playwright";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = path.resolve(import.meta.dirname, "..");
const source = path.join(root, "scripts", "social-preview.html");
const output = path.join(root, "assets", "images", "social-preview.png");

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(source).href);
await page.screenshot({ path: output, type: "png" });
await browser.close();

console.log(output);

