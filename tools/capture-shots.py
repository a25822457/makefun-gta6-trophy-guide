# Leonida Trophy Guide screenshot capture — round 2 (2026-11-20).
"""Capture 4 screenshots of the trophy guide at 1280x720 JPEG via Playwright.
Run from the repo root with the .pw-venv python. Serves app/ on :8080 first.
Shots: 1 cover (hero + KPI strip + progress + filters), 2 trophy detail modal
(Positive Mental Attitude, the one missable trophy), 3 search demo ("bank",
spoiler on — filtered list + masked hidden trophies), 4 roadmap.
"""
import subprocess, time, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, 'screenshots')
os.makedirs(SHOTS, exist_ok=True)

server = subprocess.Popen(
    ['node', 'serve.ts', '--port', '8080'], cwd=ROOT,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path='/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome',
            args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.on('console', lambda m: errors.append(f'console.{m.type}: {m.text}') if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
        page.goto('http://localhost:8080/', wait_until='networkidle')
        page.wait_for_timeout(600)
        # Reveal everything for the cover, tick a few trophies for real progress.
        page.locator('#spoiler').uncheck()
        page.wait_for_timeout(300)
        boxes = page.locator('.card input[type="checkbox"]')
        for i in [0, 1, 2, 4, 6]:
            boxes.nth(i).check()
        page.wait_for_timeout(400)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(300)
        # 1. Cover: hero + KPI strip + progress + filters + first trophies.
        page.screenshot(path=os.path.join(SHOTS, '1-checklist.jpg'), type='jpeg', quality=88)
        # 2. Detail: open the detail modal for Positive Mental Attitude,
        # the one missable trophy — guide, sources and warning in one view.
        card = page.locator('.card', has=page.locator('h3:text-is("Positive Mental Attitude")'))
        card.locator('.detail-link').click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(SHOTS, '2-detail.jpg'), type='jpeg', quality=88)
        page.keyboard.press('Escape')
        page.wait_for_timeout(300)
        # 3. Search demo: spoiler on, type "bank" — filtered list (6 hits)
        # with hidden trophies masked, proving search + spoiler together.
        page.locator('#spoiler').check()
        page.locator('#search').fill('bank')
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, '3-search.jpg'), type='jpeg', quality=88)
        # 4. Roadmap: clear the search, scroll to the roadmap section.
        page.locator('#search').fill('')
        page.wait_for_timeout(400)
        page.locator('#roadmap').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(SHOTS, '4-roadmap.jpg'), type='jpeg', quality=88)
        browser.close()
finally:
    server.terminate()

print('console/page errors:', errors if errors else '0')
for f in sorted(os.listdir(SHOTS)):
    fp = os.path.join(SHOTS, f)
    print(f, os.path.getsize(fp), 'bytes')
