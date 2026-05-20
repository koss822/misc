# web-screenshots

Headless Firefox screenshot tool for web pages — including JavaScript-heavy ones (D3.js, React, Vue, etc.).  
Uses **Selenium WebDriver** to wait for JS rendering before capturing, so you get the fully rendered page rather than a blank loading state.

---

## Why not `--screenshot` / xwd / scrot?

| Method | JS renders? | Notes |
|---|---|---|
| `firefox --screenshot` | No | Captures before JS runs |
| `xwd` / `scrot` | Yes (if browser is open) | Screen capture, requires display |
| **This tool (Selenium)** | **Yes** | Waits for a CSS selector, then captures |

---

## Requirements

- Python 3.8+
- Firefox >= 78
- geckodriver

---

## Installation

```bash
bash install.sh
```

The script installs `selenium` via pip and downloads the correct `geckodriver` binary for your architecture (`x86_64` or `aarch64`).

Manual steps if preferred:

```bash
# 1. Python dependency
pip3 install selenium

# 2. geckodriver (adjust version as needed)
curl -sL https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
  | tar -xz -C /tmp/
sudo mv /tmp/geckodriver /usr/local/bin/
```

---

## Usage

### Command line

```bash
# Basic — static page
python3 screenshot.py https://example.com output.png

# JavaScript page — wait for element, then extra 3 s for animations
python3 screenshot.py http://localhost:3000 output.png "svg path" 3
```

Arguments:

```
python3 screenshot.py <url> <output.png> [css_selector] [extra_wait_seconds]
```

| Argument | Default | Description |
|---|---|---|
| `url` | — | Page URL to capture |
| `output.png` | — | Output file path |
| `css_selector` | none | Wait for this element before capturing |
| `extra_wait` | `2.0` | Seconds to wait after selector appears |

### As a library

```python
from screenshot import take_screenshot

# Static page
take_screenshot("https://example.com", "out.png")

# D3.js / React / Vue — wait for rendering
take_screenshot(
    url="http://localhost:3000",
    output_path="out.png",
    wait_css="svg path",   # wait until SVG paths exist in DOM
    extra_wait=3.0,        # wait for animations to finish
    width=1280,
    height=900,
)
```

---

## Waiting for JavaScript rendering

The key parameter is `wait_css` — a CSS selector that only appears in the DOM after JS has finished rendering.  
`WebDriverWait` blocks until the element is found (up to 15 seconds), then `extra_wait` gives animations time to finish.

Common selectors:

| Framework | Selector |
|---|---|
| D3.js chart | `svg path` |
| Chart.js | `canvas` |
| React / Vue app | `#app > *` |
| Data table loaded | `table tbody tr` |
| Custom ready flag | `.chart-ready`, `[data-loaded]` |

If the page has no JS, omit `wait_css` entirely.

---

## HTTPS with self-signed certificates

Use the internal port directly over HTTP instead of going through the HTTPS proxy:

```python
# Instead of https://myapp.local (nginx proxy with custom CA)
take_screenshot("http://127.0.0.1:8080", "out.png")
```

---

## Files

| File | Description |
|---|---|
| `screenshot.py` | Main module — `take_screenshot()` function + CLI entry point |
| `requirements.txt` | Python dependencies (`selenium`) |
| `install.sh` | One-shot installer for geckodriver + pip dependencies |

---

## License

GPL — see [../../gpl.txt](../../gpl.txt)
