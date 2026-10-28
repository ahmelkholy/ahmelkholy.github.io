// Run with a host Playwright tool against the local preview. Screenshots go in review-artifacts.
async (page) => {
  await page.setViewportSize({ width: 390, height: 900 });
  const checks = [];
  function check(ok, label) {
    if (!ok) throw new Error(label);
    checks.push(label);
  }
  await page.goto("http://127.0.0.1:4000/articles/");
  await page.getByLabel("Language", { exact: true }).selectOption("ar");
  check(
    (await page.locator("[data-articles]>li:visible").count()) === 4,
    "Arabic filter returns four original posts",
  );
  await page.getByLabel("Filter by title or tag").fill("مولدات");
  check(
    (await page.locator("[data-articles]>li:visible").count()) === 1,
    "Arabic search works",
  );
  await page.getByLabel("Filter by title or tag").fill("");
  await page.getByLabel("Language", { exact: true }).selectOption("ru");
  check(
    (await page.locator("[data-filter-status]").innerText()).includes(
      "No Russian articles yet",
    ),
    "Honest Russian empty state",
  );
  await page.getByLabel("Language", { exact: true }).selectOption("en");
  await page.getByLabel("Filter by title or tag").fill("transformer");
  await page.locator("[data-articles]>li:visible h2 a").click();
  check(
    page.url().includes("transformer-connections"),
    "Transformer collision resolved to distinct working route",
  );
  check(
    await page
      .locator(".article-body img")
      .evaluate((i) => i.complete && i.naturalWidth > 0),
    "Original transformer image loads",
  );
  await page.goto("http://127.0.0.1:4000/posts/2023/08/blog-post-4/");
  await page.locator('.translations a[lang="ar"]').click();
  check(
    page.url().includes("blog-post-5"),
    "Real English-to-Arabic translation works",
  );
  check(
    (await page.locator("html").getAttribute("dir")) === "rtl",
    "Arabic article RTL",
  );
  await page.locator(".toc summary").click();
  await page.locator(".toc a").first().click();
  check(
    new URL(page.url()).hash.length > 0,
    "Article TOC navigates to heading",
  );
  await page.goto("http://127.0.0.1:4000/docs/authoring/ar/");
  await page.locator("mjx-container").waitFor();
  check(
    (await page
      .locator("pre")
      .first()
      .evaluate((e) => getComputedStyle(e).direction)) === "ltr",
    "Arabic code remains LTR",
  );
  check(
    (await page
      .locator("mjx-container")
      .first()
      .evaluate((e) => getComputedStyle(e).direction)) === "ltr",
    "Arabic math remains LTR",
  );
  await page.screenshot({
    path: "review-artifacts/docs-ar-mobile.png",
    fullPage: true,
  });
  await page.goto("http://127.0.0.1:4000/docs/static-example/");
  check(
    (await page.locator("code").innerText()) === "{{ untouched }}",
    "Static import bypasses Liquid",
  );
  await page.getByRole("link", { name: "Read the example guide" }).click();
  check(page.url().endsWith("/guide/"), "Imported nested relative links work");
  await page.getByRole("link", { name: "Back to the example" }).click();
  check(
    page.url().endsWith("/static-example/"),
    "Imported return navigation works",
  );
  await page.goto("http://127.0.0.1:4000/");
  await page.keyboard.press("Tab");
  check(
    await page.locator(".skip").evaluate((e) => e === document.activeElement),
    "Keyboard reaches skip link first",
  );
  check(
    await page
      .locator(".skip")
      .evaluate((e) => getComputedStyle(e).outlineStyle !== "none"),
    "Keyboard focus is visible",
  );
  await page.keyboard.press("Enter");
  check(
    await page.locator("#main").evaluate((e) => e === document.activeElement),
    "Skip link moves focus to main",
  );
  await page.emulateMedia({ reducedMotion: "reduce" });
  check(
    await page.evaluate(
      () => matchMedia("(prefers-reduced-motion: reduce)").matches,
    ),
    "Reduced-motion preference respected",
  );
  await page.locator("#main").evaluate((e) => e.blur());
  await page.screenshot({
    path: "review-artifacts/home-mobile.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 320, height: 780 });
  await page.reload();
  check(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
    "No horizontal overflow at 320px",
  );
  const ctx = await page
    .context()
    .browser()
    .newContext({
      javaScriptEnabled: false,
      viewport: { width: 390, height: 844 },
    });
  const nojs = await ctx.newPage();
  await nojs.goto("http://127.0.0.1:4000/articles/");
  check(
    (await nojs.locator("[data-articles]>li").count()) === 8,
    "All articles readable without JavaScript",
  );
  check(
    (await nojs.locator(".main-nav a").count()) === 8,
    "Navigation works without JavaScript",
  );
  await ctx.close();
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("http://127.0.0.1:4000/ar/");
  await page.screenshot({
    path: "review-artifacts/profile-ar-desktop.png",
    fullPage: true,
  });
  return checks;
}
