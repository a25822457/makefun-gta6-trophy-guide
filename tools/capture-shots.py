# Leonida Trophy Guide screenshot capture — round 3 (2026-11-21).
"""Capture 4 screenshots of the trophy guide at 1280x720 JPEG via Playwright.
Run from the repo root with the .pw-venv python. Serves app/ on :8080 first.
Shots: 1 cover (hero + KPI strip incl. difficulty stat + filters + first
trophies with difficulty badges), 2 trophy detail modal (A Long Road —
Very Hard, ~100 hours), 3 difficulty filter demo ("Hard" selected,
3 Hard trophies), 4 roadmap.
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
        # 1. Cover: hero + KPI strip + filters (incl. difficulty) + first
        # trophies with their difficulty badges and time estimates.
        page.screenshot(path=os.path.join(SHOTS, '1-checklist.jpg'), type='jpeg', quality=88)
        # 2. Detail: open the detail modal for A Long Road — Very Hard,
        # ~100 hours, the hardest trophy in the game.
        card = page.locator('.card', has=page.locator('h3:text-is("A Long Road")'))
        card.locator('.detail-link').click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(SHOTS, '2-detail.jpg'), type='jpeg', quality=88)
        page.keyboard.press('Escape')
        page.wait_for_timeout(300)
        # 3. Difficulty filter demo: spoiler on, filter to "Hard" — the 3
        # Hard trophies (Cunning Stunts, The Shootist, Personal Best).
        page.locator('#spoiler').check()
        page.locator('#difficulty').select_option('Hard')
        page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0,0)")
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, '3-search.jpg'), type='jpeg', quality=88)
        # 4. Roadmap: clear the filter, scroll to the roadmap section.
        page.locator('#difficulty').select_option('all')
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
