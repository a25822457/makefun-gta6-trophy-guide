# Leonida Trophy Guide — GTA VI, all 55 trophies

[![make.fun · gta6-trophy-guide-01](https://make.fun/badge/gta6-trophy-guide-01.svg)](https://make.fun/bounty/gta6-trophy-guide-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-guide-01)
[![rank](https://make.fun/badge/gta6-trophy-guide-01/a25822457/makefun-gta6-trophy-guide/rank.svg)](https://make.fun/bounty/gta6-trophy-guide-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-guide-01)
[![reward](https://make.fun/badge/gta6-trophy-guide-01/a25822457/makefun-gta6-trophy-guide/reward.svg)](https://make.fun/bounty/gta6-trophy-guide-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-guide-01)

An offline trophy guide and tracker for Grand Theft Auto VI (PlayStation 5). Built for the make.fun "Build the best GTA 6 trophy guide" bounty.

## What it is

- **All 55 trophies** — 1 Platinum, 2 Gold, 6 Silver, 46 Bronze; 28 of them hidden — with the official name, description and grade for each, exactly as PlayStation publishes them.
- **A guide for every trophy, in our own words**, saying what to do, where and how, and when it can be missed. Every concrete claim names its source beside it.
- **A tracker** — tick trophies off as you earn them; progress is saved in your browser (localStorage), with export/import to move it between devices.
- **Filters** — by grade, by category (story, collectibles, activities, robberies, exploration, money, completion, miscellaneous), missable only, search, and hide-earned.
- **Spoiler setting** — hides the 28 hidden (story) trophies until you have earned them, so the guide never spoils the story.
- **A roadmap to the Platinum** — about 200 hours: play the story, reach 100% completion, then clean up the rest. It flags the one trophy that can be missed and the save habits that keep you safe.

## The one missable trophy

**Positive Mental Attitude** — meditate at all 18 spots. Lucia's balcony meditation in Chapter 1 (after the mission Down to Earth, find her in Jason's kitchen in the morning and follow her to the balcony) disappears once Chapter 1 ends, and there is no mission replay. Do it in Chapter 1 and keep a Chapter 1 save. The guide flags this everywhere it matters.

## Save habits

There is no mission replay and no New Game Plus, so keep a manual save at the start of every chapter and one untouched save from just before the final mission. Cheats switch off trophies and saving — keep them off your trophy save.

## Honest about the unknown

Five hidden trophies — In The Beginning…, Capital Offense, Bad Luck, I Guess, The Truth Is Out There and Ten Pin — have no confirmed unlock method at launch. The guide says so for each of them instead of inventing a location or a step, and will be updated once players confirm the trigger.

## Sources

- KeenGamer — GTA 6 Trophy Guide & Platinum Roadmap (published 2026-11-19): https://www.keengamer.com/articles/guides/gta-6-trophy-guide-platinum-roadmap-all-55-trophies/
- Output Lag — GTA 6 Trophy List: https://outputlag.com/guides/gta-6-trophy-list/
- Push Square — GTA 6 Trophy Guide & Roadmap: https://www.pushsquare.com/guides/gta-6-trophy-guide-and-roadmap
- PlayStation official trophy list (via Exophase / PSNProfiles): https://www.exophase.com/game/grand-theft-auto-vi-psn/trophies/
- Rockstar Games — GTA 6 official site: https://www.rockstargames.com/VI

## Run it

`node serve.ts` serves `app/` on http://localhost:8080. No network is needed — the app loads nothing from outside.

## Screenshots

Taken from the real app in a headless browser (see `tools/capture-shots.py`):

1. `1-checklist.jpg` — the checklist with guides and sources open, progress bar and filters visible.
2. `2-roadmap.jpg` — the roadmap to the Platinum.
3. `3-missable.jpg` — the one missable trophy, Positive Mental Attitude, with its full guide and sources.
4. `4-spoiler.jpg` — the spoiler setting at work: earned story trophies revealed, un-earned hidden ones masked.

## Make.fun

Built for the make.fun bounty [gta6-trophy-guide-01](https://make.fun/bounty/gta6-trophy-guide-01).

Re-witnessed 2026-11-20: all 55 guides re-verified against post-launch sources.
