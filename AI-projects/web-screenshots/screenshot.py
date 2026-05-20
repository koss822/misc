#!/usr/bin/env python3
"""
screenshot.py — headless Firefox web page screenshot via Selenium.

Takes a screenshot of any URL, including JavaScript-heavy pages (D3, React, Vue…),
by waiting for a CSS selector to appear before capturing.

Usage (CLI):
    python3 screenshot.py <url> <output.png> [css_selector] [extra_wait_seconds]

Usage (import):
    from screenshot import take_screenshot
    take_screenshot("http://localhost:3000", "out.png", wait_css="#app .chart")
"""

import os
import sys
import time
from shutil import which

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _find_geckodriver() -> str:
    path = which("geckodriver")
    if path:
        return path
    candidates = ["/usr/local/bin/geckodriver", "/usr/bin/geckodriver"]
    for c in candidates:
        if os.path.isfile(c):
            return c
    raise FileNotFoundError(
        "geckodriver not found. Install it and put it on PATH.\n"
        "Download: https://github.com/mozilla/geckodriver/releases"
    )


def take_screenshot(
    url: str,
    output_path: str,
    wait_css: str | None = None,
    extra_wait: float = 2.0,
    width: int = 1280,
    height: int = 900,
    geckodriver_path: str | None = None,
) -> None:
    """
    Take a headless Firefox screenshot of `url` and save it to `output_path`.

    Args:
        url:              Page URL to capture.
        output_path:      Destination file path (PNG).
        wait_css:         CSS selector to wait for before screenshotting.
                          Use this for JS-rendered pages so the content has time to appear.
        extra_wait:       Additional seconds to wait after `wait_css` appears (for animations).
        width:            Viewport width in pixels.
        height:           Viewport height in pixels.
        geckodriver_path: Path to geckodriver binary. Auto-detected if None.
    """
    gecko = geckodriver_path or _find_geckodriver()

    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")

    service = Service(gecko, log_output=open(os.devnull, "w"))
    driver = webdriver.Firefox(options=options, service=service)

    try:
        driver.get(url)
        driver.set_window_size(width, height)

        if wait_css:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_css))
            )

        if extra_wait > 0:
            time.sleep(extra_wait)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        driver.save_screenshot(output_path)
        print(f"Saved: {output_path}  ({os.path.getsize(output_path) // 1024} KB)")
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <url> <output.png> [css_selector] [extra_wait]")
        sys.exit(1)

    _url    = sys.argv[1]
    _output = sys.argv[2]
    _css    = sys.argv[3] if len(sys.argv) > 3 else None
    _wait   = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0

    take_screenshot(_url, _output, wait_css=_css, extra_wait=_wait)
