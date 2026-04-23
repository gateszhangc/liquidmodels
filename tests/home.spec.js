const { test, expect } = require("@playwright/test");

test.describe("Liquid Models static site", () => {
  test("desktop homepage renders SEO content, model filters, and images", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Liquid Models/i);
    await expect(page.locator("h1")).toContainText("Liquid Models");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /Liquid Foundation Models/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://liquidmodels.lol/");
    await expect(page.getByText("This site is independent and not affiliated with Liquid AI.")).toBeVisible();

    await expect(page.locator(".model-card")).toHaveCount(4);
    await page.getByRole("button", { name: "Vision" }).click();
    await expect(page.locator(".model-card:not([hidden])")).toHaveCount(1);
    await expect(page.locator("[data-results-count]")).toHaveText("Showing 1 model group");
    await expect(page.getByText("LFM2.5-VL-1.6B")).toBeVisible();

    await page.getByRole("button", { name: "All" }).click();
    await expect(page.locator(".model-card:not([hidden])")).toHaveCount(4);

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout keeps key actions reachable without horizontal overflow", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByRole("link", { name: "Explore models" })).toBeVisible();
    await page.getByRole("link", { name: "Explore models" }).click();
    await expect(page.locator("#models")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await page.getByRole("button", { name: "Nano" }).click();
    await expect(page.locator(".model-card:not([hidden])")).toHaveCount(1);

    await context.close();
  });

  test("launch SEO assets are crawlable and analytics scripts are absent", async ({ page, request }) => {
    await page.goto("/");

    const html = await page.content();
    expect(html).not.toContain("googletagmanager.com");
    expect(html).not.toContain("clarity.ms");
    expect(html).not.toContain("google-analytics.com");

    const structuredData = await page.locator('script[type="application/ld+json"]').evaluateAll((nodes) =>
      nodes.map((node) => JSON.parse(node.textContent || "{}"))
    );
    expect(structuredData.some((entry) => entry["@type"] === "WebSite" && entry.url === "https://liquidmodels.lol/")).toBe(true);
    expect(structuredData.some((entry) => entry["@type"] === "FAQPage")).toBe(true);

    const robots = await request.get("/robots.txt");
    expect(robots.ok()).toBe(true);
    expect(robots.headers()["content-type"]).toMatch(/text\/plain/);
    expect(await robots.text()).toMatch(/Sitemap: https:\/\/liquidmodels\.lol\/sitemap\.xml/);

    const sitemap = await request.get("/sitemap.xml");
    expect(sitemap.ok()).toBe(true);
    expect(sitemap.headers()["content-type"]).toMatch(/application\/xml/);
    expect(await sitemap.text()).toMatch(/<loc>https:\/\/liquidmodels\.lol\/<\/loc>/);
  });
});
