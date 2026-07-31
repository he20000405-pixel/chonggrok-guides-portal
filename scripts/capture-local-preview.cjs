const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const baseUrl = process.argv[2] || "http://127.0.0.1:8765";
const outputDir = path.resolve(process.argv[3] || "tmp/preview-screenshots");
const pages = [
  "/",
  "/products/",
  "/how-it-works/",
  "/security/",
  "/knowledge/",
  "/editorial-policy/",
  "/about/",
  "/en/",
  "/404.html",
];
const auditViewports = [
  { width: 1440, height: 900 },
  { width: 390, height: 844 },
  { width: 360, height: 800 },
];

const isExpectedPlatformMessage = (message) =>
  message.includes("static.cloudflareinsights.com/beacon.min.js") ||
  message.includes("Applying inline style violates the following Content Security Policy");

fs.mkdirSync(outputDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const failures = [];

  for (const viewport of auditViewports) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    page.on("console", (message) => {
      if (message.type() === "error" && !isExpectedPlatformMessage(message.text())) {
        failures.push(`console ${viewport.width}px: ${message.text()}`);
      }
    });
    page.on("pageerror", (error) => {
      failures.push(`pageerror ${viewport.width}px: ${error.message}`);
    });

    for (const pagePath of pages) {
      const response = await page.goto(`${baseUrl}${pagePath}`, {
        waitUntil: "networkidle",
      });
      if (!response || response.status() >= 400) {
        failures.push(`${pagePath} returned ${response?.status() || "no response"}`);
      }

      const result = await page.evaluate(() => {
        const overflowing = [...document.querySelectorAll("body *")]
          .filter((element) => {
            const style = getComputedStyle(element);
            return (
              style.display !== "none" &&
              element.scrollWidth > element.clientWidth + 2 &&
              style.overflowX === "visible"
            );
          })
          .slice(0, 8)
          .map((element) => ({
            tag: element.tagName,
            className: element.className,
            scrollWidth: element.scrollWidth,
            clientWidth: element.clientWidth,
          }));

        const clippedButtons = [...document.querySelectorAll(".button")]
          .filter(
            (element) =>
              element.scrollWidth > element.clientWidth + 2 ||
              element.scrollHeight > element.clientHeight + 2,
          )
          .map((element) => element.textContent.trim());

        return {
          documentWidth: document.documentElement.scrollWidth,
          viewportWidth: window.innerWidth,
          overflowing,
          clippedButtons,
          h1Count: document.querySelectorAll("h1").length,
        };
      });

      if (result.documentWidth > result.viewportWidth + 1) {
        failures.push(
          `${pagePath} overflows at ${viewport.width}px: ${result.documentWidth}px`,
        );
      }
      if (result.overflowing.length) {
        failures.push(
          `${pagePath} element overflow at ${viewport.width}px: ${JSON.stringify(result.overflowing)}`,
        );
      }
      if (result.clippedButtons.length) {
        failures.push(
          `${pagePath} clipped buttons at ${viewport.width}px: ${result.clippedButtons.join(", ")}`,
        );
      }
      if (result.h1Count !== 1) {
        failures.push(
          `${pagePath} has ${result.h1Count} H1 elements at ${viewport.width}px`,
        );
      }

      if (pagePath === "/") {
        await page.screenshot({
          path: path.join(
            outputDir,
            `home-${viewport.width}x${viewport.height}.png`,
          ),
        });

        if (viewport.width <= 390) {
          await page.locator("[data-menu-open]").click();
          await page.waitForTimeout(250);
          const drawerState = await page.locator("[data-drawer]").evaluate((drawer) => ({
            hidden: drawer.getAttribute("aria-hidden"),
            open: drawer.classList.contains("is-open"),
            expanded: document
              .querySelector("[data-menu-open]")
              ?.getAttribute("aria-expanded"),
          }));
          if (
            drawerState.hidden !== "false" ||
            !drawerState.open ||
            drawerState.expanded !== "true"
          ) {
            failures.push(
              `Mobile drawer did not open correctly at ${viewport.width}px: ${JSON.stringify(drawerState)}`,
            );
          }
          await page.screenshot({
            path: path.join(
              outputDir,
              `home-${viewport.width}x${viewport.height}-menu.png`,
            ),
          });
          await page.keyboard.press("Escape");
          await page.waitForTimeout(250);
          const closedState = await page.locator("[data-drawer]").evaluate((drawer) => ({
            hidden: drawer.getAttribute("aria-hidden"),
            open: drawer.classList.contains("is-open"),
          }));
          if (closedState.hidden !== "true" || closedState.open) {
            failures.push(
              `Mobile drawer did not close correctly at ${viewport.width}px: ${JSON.stringify(closedState)}`,
            );
          }
        }
      }
    }

    await context.close();
  }

  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  await page.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
  const cardHeights = await page
    .locator(".product-card")
    .evaluateAll((cards) => cards.map((card) => Math.round(card.getBoundingClientRect().height)));
  if (new Set(cardHeights).size !== 1) {
    failures.push(`Desktop product cards are not equal height: ${cardHeights.join(", ")}`);
  }
  await page.screenshot({
    path: path.join(outputDir, "home-full-desktop.png"),
    fullPage: true,
  });
  await context.close();

  await browser.close();

  if (failures.length) {
    console.error(failures.join("\n"));
    process.exit(1);
  }
  console.log(`Audit passed. Screenshots: ${outputDir}`);
})();
