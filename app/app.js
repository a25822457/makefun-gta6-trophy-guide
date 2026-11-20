// Leonida Trophy Guide — tracker logic. Re-witnessed 2026-11-20.
// Leonida Trophy Guide: tracker for all 55 GTA VI trophies.
// Progress is saved in localStorage; export/import moves it between devices.
// Spoiler setting hides story (hidden) trophies until they are earned.
const KEY = 'leonida-trophy-guide-v1';
const list = document.getElementById('list');
const searchEl = document.getElementById('search');
const gradeEl = document.getElementById('grade');
const kindEl = document.getElementById('kind');
const missableEl = document.getElementById('missable');
const spoilerEl = document.getElementById('spoiler');
const hideEarnedEl = document.getElementById('hideEarned');
const detailEl = document.getElementById('detail');
const detailCloseEl = document.getElementById('detail-close');
const detailEarnedEl = document.getElementById('detail-earned');
let detailTrophy = null;

// Round 2: trophy detail view. Clicking a card opens the full guide,
// sources and missable warning for that one trophy in a modal.
function openDetail(t) {
  detailTrophy = t;
  document.getElementById('detail-meta').textContent = metaBits(t, false).join(' · ');
  document.getElementById('detail-name').textContent = t.name;
  document.getElementById('detail-missable').hidden = !t.missable;
  document.getElementById('detail-desc').textContent = t.description;
  document.getElementById('detail-guide').textContent = t.guide;
  const src = document.getElementById('detail-sources');
  src.replaceChildren(document.createTextNode('Sources: '));
  t.sources.forEach((s, i) => {
    if (i > 0) src.append(document.createTextNode(' · '));
    const a = document.createElement('a');
    a.href = s.url;
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = s.name;
    src.append(a);
  });
  detailEarnedEl.checked = earned.has(t.name);
  detailEl.hidden = false;
  detailCloseEl.focus();
}

function closeDetail() {
  detailEl.hidden = true;
  detailTrophy = null;
}

detailCloseEl.addEventListener('click', closeDetail);
detailEl.querySelector('.modal-backdrop').addEventListener('click', closeDetail);
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !detailEl.hidden) closeDetail();
});
detailEarnedEl.addEventListener('change', () => {
  if (!detailTrophy) return;
  if (detailEarnedEl.checked) earned.add(detailTrophy.name);
  else earned.delete(detailTrophy.name);
  save();
  render();
});

let earned = new Set(JSON.parse(localStorage.getItem(KEY) ?? '[]'));
const doc = await (await fetch('data/trophies.json')).json();
const trophies = doc.trophies;

// Stage counts in the roadmap.
for (const s of [1, 2, 3, 4]) {
  const n = trophies.filter((t) => t.stage === s).length;
  const el = document.getElementById('count' + s);
  if (el) el.textContent = '· ' + n + (n === 1 ? ' trophy' : ' trophies');
}

function save() {
  localStorage.setItem(KEY, JSON.stringify([...earned]));
}

function gradeLabel(g) {
  return g.charAt(0).toUpperCase() + g.slice(1);
}

function kindLabel(k) {
  const m = {
    story: 'Story', collectible: 'Collectible', activity: 'Activity',
    robbery: 'Robbery', exploration: 'Exploration', economy: 'Money',
    completion: 'Completion', misc: 'Miscellaneous', platinum: 'Platinum',
  };
  return m[k] || k;
}

function stageLabel(s) {
  return { 1: 'Stage 1 · Story', 2: 'Stage 2 · 100%', 3: 'Stage 3 · Clean-up', 4: 'Platinum' }[s] || '';
}

// Meta bits for a trophy, de-duplicated case-insensitively: the Platinum
// trophy's grade, kind and stage are all "Platinum", which read as
// "PLATINUM · PLATINUM · PLATINUM" before this fix.
function metaBits(t, withMissable) {
  const bits = [gradeLabel(t.grade), kindLabel(t.kind), stageLabel(t.stage)];
  const seen = new Set();
  const out = [];
  for (const b of bits) {
    const k = b.toLowerCase();
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(b);
  }
  if (withMissable && t.missable) out.push('MISSABLE');
  return out;
}

function matches(t) {
  const q = searchEl.value.trim().toLowerCase();
  if (q && !(t.name + ' ' + t.description + ' ' + t.guide).toLowerCase().includes(q)) return false;
  if (gradeEl.value !== 'all' && t.grade !== gradeEl.value) return false;
  if (kindEl.value !== 'all' && t.kind !== kindEl.value) return false;
  if (missableEl.checked && !t.missable) return false;
  if (hideEarnedEl.checked && earned.has(t.name)) return false;
  return true;
}

function render() {
  list.replaceChildren();
  let shown = 0;
  for (const t of trophies) {
    if (!matches(t)) continue;
    shown++;
    const isEarned = earned.has(t.name);
    const isHidden = spoilerEl.checked && t.hidden && !isEarned;
    const card = document.createElement('article');
    card.className = 'card' + (isEarned ? ' earned' : '') + (t.missable ? ' missable' : '');
    card.dataset.grade = t.grade;

    const head = document.createElement('div');
    head.className = 'card-head';
    const box = document.createElement('input');
    box.type = 'checkbox';
    box.checked = isEarned;
    box.setAttribute('aria-label', 'Mark ' + t.name + ' earned');
    box.addEventListener('change', () => {
      if (box.checked) earned.add(t.name);
      else earned.delete(t.name);
      save();
      render();
    });
    head.append(box);

    const title = document.createElement('div');
    title.className = 'card-title';
    const name = document.createElement('h3');
    name.textContent = isHidden ? 'Hidden trophy — earn it to reveal' : t.name;
    title.append(name);
    const meta = document.createElement('p');
    meta.className = 'meta';
    const bits = isHidden ? [gradeLabel(t.grade)] : metaBits(t, true);
    meta.textContent = bits.join(' · ');
    title.append(meta);
    head.append(title);
    card.append(head);

    if (!isHidden) {
      const desc = document.createElement('p');
      desc.className = 'desc';
      desc.textContent = t.description;
      card.append(desc);

      const guide = document.createElement('p');
      guide.className = 'guide';
      guide.textContent = t.guide;
      card.append(guide);

      const src = document.createElement('p');
      src.className = 'sources';
      src.textContent = 'Sources: ';
      t.sources.forEach((s, i) => {
        if (i > 0) src.append(document.createTextNode(' · '));
        const a = document.createElement('a');
        a.href = s.url;
        a.target = '_blank';
        a.rel = 'noopener';
        a.textContent = s.name;
        src.append(a);
      });
      card.append(src);

      const more = document.createElement('button');
      more.type = 'button';
      more.className = 'detail-link';
      more.textContent = 'Full guide & sources →';
      more.addEventListener('click', (e) => {
        e.stopPropagation();
        openDetail(t);
      });
      card.append(more);
    } else {
      const note = document.createElement('p');
      note.className = 'spoiler-note';
      note.textContent = 'This is one of the 28 hidden trophies. Turn off “Hide story spoilers” to see it, or tick it off once you have earned it.';
      card.append(note);
    }
    // Clicking the card (not its checkbox) opens the trophy detail view.
    card.addEventListener('click', (e) => {
      if (e.target.closest('input[type="checkbox"], .detail-link')) return;
      if (isHidden) return;
      openDetail(t);
    });
    list.append(card);
  }

  const total = trophies.length;
  const pct = Math.round((earned.size / total) * 100);
  document.getElementById('bar').style.width = pct + '%';
  document.getElementById('progress').textContent =
    earned.size + ' of ' + total + ' earned · ' + pct + '% to the Platinum';
  const byGrade = ['platinum', 'gold', 'silver', 'bronze'].map((g) => {
    const n = trophies.filter((t) => t.grade === g).length;
    const e = trophies.filter((t) => t.grade === g && earned.has(t.name)).length;
    return gradeLabel(g) + ' ' + e + '/' + n;
  }).join(' · ');
  document.getElementById('grades').textContent = byGrade + (shown !== total ? ' · showing ' + shown : '');
}

document.getElementById('export').addEventListener('click', () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify([...earned], null, 2)], { type: 'application/json' }));
  a.download = 'leonida-trophy-progress.json';
  a.click();
});
document.getElementById('import').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    const names = JSON.parse(await file.text());
    const valid = new Set(trophies.map((t) => t.name));
    earned = new Set(names.filter((n) => valid.has(n)));
    save();
    render();
  } catch (err) {
    alert('That file could not be read as trophy progress.');
  }
});
for (const el of [searchEl, gradeEl, kindEl, missableEl, spoilerEl, hideEarnedEl]) {
  el.addEventListener('input', render);
  el.addEventListener('change', render);
}
render();
