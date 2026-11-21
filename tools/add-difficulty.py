# Round 3: add difficulty + time_estimate to all 55 trophies (2026-11-21).
"""Add a difficulty rating (Easy/Medium/Hard/Very Hard) and a time estimate
to every trophy in app/data/trophies.json, and append the PowerPyx roadmap
as the source for the ratings. Ratings are derived from the requirement
itself (counts taken from the guide) and the PowerPyx/KeenGamer roadmap
steps: story 60-80 h, 100% checklist ~100 h, cleanup ~10 h, platinum
~200 h, hardest trophy A Long Road. Time estimates are labelled as
estimates; the five trophies whose unlock method is still unconfirmed
get time "Unknown - method unconfirmed at launch" rather than a made-up
number. Run from the repo root: python3 tools/add-difficulty.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'app', 'data', 'trophies.json')

# (difficulty, time_estimate) by trophy id.
RATINGS = {
 1: ("Very Hard", "~200 hours total — the whole roadmap"),
 2: ("Easy", "Story progress — first mission"),
 3: ("Easy", "Story progress — Chapter 1"),
 4: ("Easy", "Story progress — Chapter 2"),
 5: ("Easy", "Story progress — Chapter 3"),
 6: ("Easy", "Story progress — Chapter 4"),
 7: ("Easy", "Story progress — final mission"),
 8: ("Easy", "Story progress — one mission (Chapter 2)"),
 9: ("Easy", "Story progress — one mission"),
 10: ("Easy", "Story progress — one mission"),
 11: ("Easy", "Story progress — one mission"),
 12: ("Easy", "Story progress — one mission"),
 13: ("Easy", "Story progress — one mission"),
 14: ("Very Hard", "~100 hours — the 100% checklist stage"),
 15: ("Hard", "Several hours — 250 stunts (300 for 100%)"),
 16: ("Easy", "Under 1 hour — try 9 activities once"),
 17: ("Hard", "Several hours — 42 gold medals at 2 ranges"),
 18: ("Medium", "A few hours — win at 14 drone race locations"),
 19: ("Medium", "A few hours — win 20 races (30 for 100%)"),
 20: ("Medium", "1–2 hours — fishing challenges, then beat Cal"),
 21: ("Easy", "Under 30 minutes — finish one arcade game"),
 22: ("Easy", "Story progress — Andy's finale (after the story)"),
 23: ("Easy", "Story progress — Kenton's finale"),
 24: ("Easy", "Story progress — Billy's finale"),
 25: ("Medium", "A few hours — 8 stranger strands (cleanup stage)"),
 26: ("Easy", "Story progress — Randy's finale"),
 27: ("Easy", "Story progress — Tyrone's finale"),
 28: ("Medium", "A few hours — 18 meditation spots; Chapter 1 one is missable"),
 29: ("Easy", "Story progress — Bret's hunt (Jason-only)"),
 30: ("Medium", "Accumulates while collecting — 3 of 18 card sets"),
 31: ("Medium", "Accumulates while travelling — scan 100 locations"),
 32: ("Medium", "Accumulates — 50 of 80 challenges (70 for 100%)"),
 33: ("Easy", "About 30 minutes — lose a 4-star wanted level with your partner"),
 34: ("Medium", "About 1 hour — rob 3 shops back-to-back without losing the wanted level"),
 35: ("Medium", "Accumulates while driving — discover 100 vehicles (200 for 100%)"),
 36: ("Easy", "Under 30 minutes — 5 takedowns in one Combat Focus"),
 37: ("Easy", "About 30 minutes — steal a jet at VCIA and fly off"),
 38: ("Easy", "About 30 minutes — steal a Rhino at Mile Zero"),
 39: ("Medium", "About 1 hour — needs the Snap Gun and a clean, undetected run"),
 40: ("Medium", "A few hours — rob 5 bank vaults and escape"),
 41: ("Easy", "About 30–60 minutes — tail and rob one armored truck"),
 42: ("Easy", "Accumulates while travelling — visit all 6 regions"),
 43: ("Medium", "A few hours — one illegal operation per gang (9 gangs)"),
 44: ("Easy", "Unknown — method unconfirmed at launch"),
 45: ("Easy", "Unknown — method unconfirmed at launch"),
 46: ("Medium", "About 1 hour — Kingpin Bowling robbery, 3 valuables"),
 47: ("Hard", "Several hours — max Strength for both Jason and Lucia"),
 48: ("Medium", "Accumulates across play — 500 criminal-profile actions"),
 49: ("Medium", "Unknown — method unconfirmed at launch"),
 50: ("Medium", "Unknown — method unconfirmed at launch"),
 51: ("Easy", "Unknown — method still being confirmed at launch"),
 52: ("Medium", "Accumulates — launder $250,000 in Marked Bills"),
 53: ("Easy", "Accumulates naturally — spend $100,000 across shops"),
 54: ("Easy", "About 1 hour — buy all 8 garages (~$160,000)"),
 55: ("Easy", "About 1 hour — register 10 vehicles"),
}

POWERPYX = {
  "name": "PowerPyx — GTA 6 Trophy Guide & Roadmap",
  "url": "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-trophy-guide-roadmap/",
}

with open(PATH, encoding='utf-8') as f:
    doc = json.load(f)

assert len(doc['trophies']) == 55, len(doc['trophies'])
for t in doc['trophies']:
    diff, time_est = RATINGS[t['id']]
    assert diff in ("Easy", "Medium", "Hard", "Very Hard"), t['id']
    t['difficulty'] = diff
    t['time_estimate'] = time_est
    if not any(s.get('url') == POWERPYX['url'] for s in t['sources']):
        t['sources'].append(dict(POWERPYX))

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
    f.write('\n')

from collections import Counter
print('counts:', dict(Counter(t['difficulty'] for t in doc['trophies'])))
print('unknown time:', [t['id'] for t in doc['trophies'] if t['time_estimate'].startswith('Unknown')])
print('wrote', PATH)
