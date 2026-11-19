# Leonida Trophy Guide screenshot capture — re-witnessed 2026-11-20
"""Capture 4 screenshots of the trophy guide at 1280x720 JPEG via Playwright.
Run from the repo root with the .pw-venv python. Serves app/ on :8080 first.
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
        # 1. Cover: hero + progress + filters + first trophies with guides/sources.
        page.screenshot(path=os.path.join(SHOTS, '1-checklist.jpg'), type='jpeg', quality=88)
        # 2. Roadmap: scroll to the roadmap section.
        page.locator('#roadmap').scroll_into_view_if_needed()
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(SHOTS, '2-roadmap.jpg'), type='jpeg', quality=88)
        # 3. Detail: missable filter on — centre the Positive Mental Attitude card.
        page.evaluate("window.scrollTo(0,0)")
        page.locator('#missable').check()
        page.wait_for_timeout(400)
        page.locator('.card', has_text='Positive Mental Attitude').scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, '3-missable.jpg'), type='jpeg', quality=88)
        # 4. Spoiler at work: story category + spoiler on — hidden trophies masked.
        page.locator('#missable').uncheck()
        page.locator('#spoiler').check()
        page.locator('#kind').select_option('story')
        page.wait_for_timeout(400)
        page.locator('.list').scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, '4-spoiler.jpg'), type='jpeg', quality=88)
        browser.close()
finally:
    server.terminate()

print('console/page errors:', errors if errors else '0')
for f in sorted(os.listdir(SHOTS)):
    fp = os.path.join(SHOTS, f)
    print(f, os.path.getsize(fp), 'bytes')
