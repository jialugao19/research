"""Run against an already-built site with the optional Playwright environment."""
from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


SITE_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ["RESEARCH_PREVIEW_URL"].rstrip("/") + "/"
CHROMIUM = os.environ["RESEARCH_CHROMIUM"]
OUTPUT = SITE_ROOT / "build-audit" / "browser"


def assert_document(page, route: str, viewport: dict[str, int]) -> dict[str, object]:
    # Verify a real document, its shared shell, and viewport containment.
    page.set_viewport_size(viewport)
    response = page.goto(BASE_URL + route, wait_until="networkidle")
    assert response.status == 200, route
    assert page.locator("h1").count() == 1, route
    assert not page.evaluate("document.documentElement.scrollWidth > window.innerWidth"), route
    header = page.locator(".site-header")
    assert header.locator(".top-nav a").all_text_contents() == ["Research", "Knowledge", "Publications", "GitHub ↗"]
    styles = page.locator("body").evaluate("e => ({background:getComputedStyle(e).backgroundColor,font:getComputedStyle(e).fontFamily,size:getComputedStyle(e).fontSize})")
    assert styles["background"] == "rgb(255, 255, 255)"
    assert styles["size"] == "16px"
    assert styles["font"].startswith("system-ui")
    if viewport["width"] < 700:
        assert page.locator(".doc-sidebar").is_hidden()
        page.locator(".mobile-navigation > summary").click()
        assert page.locator(".mobile-navigation .sidebar-nav").is_visible()
        page.locator(".mobile-navigation > summary").click()
    return {"route": route, "viewport": viewport, "styles": styles}


def check_filters(page) -> dict[str, int]:
    # Exercise topic/type/model/status combinations and reset through browser events.
    page.goto(BASE_URL + "experiments/", wait_until="networkidle")
    form = page.locator("[data-experiment-filters]")
    rows = page.locator("[data-experiment-row]:visible")
    assert rows.count() == 48
    form.locator("[name=study]").select_option("feature-engineering-market")
    form.locator("[name=type]").select_option("ablation")
    form.locator("[name=model]").select_option("GRU")
    form.locator("[name=status]").select_option("completed")
    assert rows.count() == 2
    form.locator("[name=search]").fill("0827")
    assert rows.count() == 1
    assert rows.first.get_attribute("data-id") == "0827-market-cs"
    page.reload(wait_until="networkidle")
    assert rows.count() == 1
    form.locator("[name=status]").select_option("doing")
    assert rows.count() == 0
    assert page.locator("[data-experiment-empty]").is_visible()
    form.locator("button[type=reset]").click()
    page.wait_for_function("document.querySelectorAll('[data-experiment-row]:not([hidden])').length === 48")
    assert rows.count() == 48
    return {"all": 48, "matched_question": 2, "searched": 1, "empty": 0, "reset": 48}


def check_image(page) -> dict[str, object]:
    # Open the full-resolution original and close it with the keyboard.
    page.goto(BASE_URL + "experiments/0827-market-cs/", wait_until="networkidle")
    image = page.locator(".research-figure img").first
    image.scroll_into_view_if_needed()
    page.wait_for_function("document.querySelector('.research-figure img').complete")
    assert image.evaluate("e=>e.naturalWidth > 0")
    original = image.locator("..").get_attribute("href")
    image.click()
    dialog = page.locator("dialog.image-lightbox")
    assert dialog.is_visible()
    assert dialog.locator("img").get_attribute("src").endswith(original)
    page.wait_for_function("document.querySelector('dialog img').complete && document.querySelector('dialog img').naturalWidth > 0")
    page.screenshot(path=str(OUTPUT / "original-image.png"))
    page.keyboard.press("Escape")
    assert dialog.is_hidden()
    return {"original": original, "lightbox": "passed"}


def main() -> None:
    # Cover both research pages and existing Knowledge/Publications on real Chromium.
    OUTPUT.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    missing: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=CHROMIUM, headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("response", lambda response: missing.append(response.url) if response.status >= 400 else None)
        documents = []
        routes = {
            "overview": "", "project": "projects/prediction-nn-1min/",
            "stage": "projects/prediction-nn-1min/feature-engineering/",
            "experiments": "experiments/", "study": "studies/feature-engineering-market/",
            "experiment": "experiments/0827-market-cs/", "infrastructure": "projects/experiment-infra/",
            "knowledge": "knowledge/machine-intelligence/nlp-transformers/attention-mechanism/",
            "publications": "reports/", "markdown-report": "reports/live-predictor/0805-live-predictor-quality/",
        }
        for mode, viewport in [("desktop", {"width": 1440, "height": 1000}), ("mobile", {"width": 390, "height": 844})]:
            for label, route in routes.items():
                documents.append(assert_document(page, route, viewport))
                page.screenshot(path=str(OUTPUT / f"{label}-{mode}.png"))
            filters = check_filters(page)
            page.screenshot(path=str(OUTPUT / f"filters-{mode}.png"))
            image = check_image(page)
            page.goto(BASE_URL + "experiments/0827-market-cs/", wait_until="networkidle")
            page.locator("#matched-comparison").scroll_into_view_if_needed()
            page.screenshot(path=str(OUTPUT / f"comparison-{mode}.png"))
        assert not errors, errors
        assert not missing, missing
        browser.close()
    result = {"base_url": BASE_URL, "documents": documents, "filters": filters, "image": image, "page_errors": errors, "missing_resources": missing}
    (OUTPUT / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"browser passed: {len(documents)} desktop/mobile documents, combined filters, original images, no JS/resource errors")


if __name__ == "__main__":
    main()
