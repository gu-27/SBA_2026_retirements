#!/usr/bin/env python3
"""
build.py — Generate retirement tribute pages for all four honorees.
Run from: /Users/correia/projects/SBA_2026_retirements/
Generates: keepsake.html, wall.html, tribute.html, index.html per person.
"""

import json, html as htmllib, os

BASE = '/Users/correia/projects/SBA_2026_retirements'

with open(f'{BASE}/source/combined.json') as f:
    DATA = json.load(f)

def e(s):
    return htmllib.escape(str(s or ''))

def ebr(s):
    """Escape and turn newlines into <br> tags."""
    return htmllib.escape(str(s or '')).replace('\n', '<br>')

# ─── Person configuration ────────────────────────────────────────────────────

PEOPLE = {
    'tatao': {
        'name': 'Ta-Tao',
        'role': 'Faculty · Management Information Systems',
        'tagline': 'Educator &nbsp;·&nbsp; Adventurer &nbsp;·&nbsp; Tech Visionary &nbsp;·&nbsp; Health Advocate',
        'closing_head': 'Go Play Now',
        'closing_body': 'Go play badminton on Wednesday. Go travel somewhere with a camera. Go tell someone to eat an apple and take a walk. The SBA will be different without you — and richer for every year you were here.',
        'color':       '#1A4E8A',
        'color_dark':  '#0D2E52',
        'color_mid':   '#2A6BAA',
        'color_light': '#E8F0FA',
        'pillars': [
            ('✈️', 'The Explorer',  'From Taiwan to Spokane, his travels brought the world into Jepson.'),
            ('🏸', 'The Athlete',   'Badminton Wednesdays. Pickleball weekends. An open invitation, always.'),
            ('💡', 'The Futurist',  'First in the building to embrace new technology. Last to stop talking about it.'),
            ('🍵', 'The Healer',    'Tea. Apples. A walk. His prescription for whatever ailed you.'),
        ],
        # (emoji, label) pairs — one per entry, in entry order
        'concepts': [
            ('🤝', 'The Colleague'), ('🏸', 'The Athlete'), ('📚', 'The Teacher'),
            ('🛡️', 'The Protector'), ('💡', 'The Futurist'), ('🌱', 'The Foundation'),
            ('✈️', 'The Explorer'), ('🎯', 'The Mentor'), ('⚡', 'The Spirit'),
            ('📸', 'The Storyteller'), ('🍵', 'The Healer'), ('🌉', 'The Bridge'),
            ('✨', 'The Spark'), ('🏓', 'The Competitor'), ('🍜', 'The Host'),
            ('🏠', 'The Welcome'), ('🥡', 'The Gatherer'), ('💻', 'The Innovator'),
            ('🔬', 'The Learner'), ('🎉', 'The Encourager'), ('🥂', 'Next Chapter'),
            ('💬', 'The Honest'), ('💛', 'The Presence'), ('🎓', 'The Guide'),
            ('🏠', 'The Neighbor'), ('🌿', 'The Cultivator'), ('👋', 'The Connector'),
        ],
    },
    'jane': {
        'name': 'Jane',
        'role': 'Academic Advisor · Student Services',
        'tagline': 'Advisor &nbsp;·&nbsp; Connector &nbsp;·&nbsp; Heart of the SBA &nbsp;·&nbsp; Friend',
        'closing_head': 'The Heart Keeps Beating',
        'closing_body': "You were the institutional memory, the warm greeting, the person who always knew the answer and made sure you felt welcome finding it. The SBA is different because of you \u2014 and that doesn\u2019t retire.",
        'color':       '#8A1A3A',
        'color_dark':  '#520D22',
        'color_mid':   '#AA2A50',
        'color_light': '#FAE8EF',
        'pillars': [
            ('📚', 'The Encyclopedia', 'Decades of institutional knowledge, always shared generously.'),
            ('😄', 'The Joy',          'An infectious laugh that could change the mood of any room.'),
            ('❤️', 'The Heart',        'The standard for what it means to genuinely care for students.'),
            ('🏠', 'The Host',         'Her home, her table, her warmth — always open to the SBA family.'),
        ],
        'concepts': [
            ('🌟', 'The Welcome'), ('📚', 'The Encyclopedia'), ('🎓', 'The Guide'),
            ('😄', 'The Joy'), ('❤️', 'The Heart'), ('🏠', 'The Host'),
            ('👗', 'The Style'), ('⚡', 'The Energy'), ('🤝', 'The Friend'),
            ('📖', 'The Knowledge'), ('😂', 'The Laughter'), ('🏡', 'The Gathering'),
            ('💛', 'The Warmth'), ('✨', 'The Contagious'), ('🌸', 'The Bloom'),
            ('🗝️', 'The Key'), ('🎊', 'The Celebration'), ('💬', 'The Conversation'),
            ('🌻', 'The Sunshine'), ('🏆', 'The Standard'), ('🧭', 'The Navigator'),
            ('💌', 'The Letter'), ('🌈', 'The Color'), ('🪴', 'The Care'),
            ('🔮', 'The Wisdom'), ('✈️', 'The Adventure'), ('⭐', 'The Star'),
            ('🎭', 'The Life of the Party'),
        ],
    },
    'gary': {
        'name': 'Gary',
        'role': 'Faculty · Accounting',
        'tagline': 'Educator &nbsp;·&nbsp; Mentor &nbsp;·&nbsp; Builder &nbsp;·&nbsp; Friend',
        'closing_head': 'The Standard You Set',
        'closing_body': "You built something here that outlasts any classroom \u2014 careers, habits of mind, a sense of what excellence actually looks like. Every conversation you had with someone made them better. That doesn\u2019t retire either.",
        'color':       '#1A5C1A',
        'color_dark':  '#0D380D',
        'color_mid':   '#2A7A2A',
        'color_light': '#E8F5E8',
        'pillars': [
            ('🏗️', 'The Builder',   'He built the accounting program from the ground up, brick by brick.'),
            ('🎓', 'The Mentor',    'Generations of faculty trace their careers back to a conversation with Gary.'),
            ('💬', 'The Connector', "In hallways, at Jack & Dan\u2019s, at the Osprey \u2014 every conversation mattered."),
            ('⭐', 'The Standard',  'Tireless, thorough, and generous. He set the bar for what a colleague could be.'),
        ],
        'concepts': [
            ('🎓', 'The Mentor'), ('🏗️', 'The Builder'), ('💬', 'The Connector'),
            ('⭐', 'The Standard'), ('❤️', 'The Heart'), ('🏀', 'The Fan'),
            ('🤝', 'The Welcome'), ('💡', 'The Educator'), ('🌟', 'The Inspiration'),
            ('📊', 'The Expert'), ('⚡', 'The Energy'), ('🔥', 'The Dedication'),
            ('🏆', 'The Legacy'), ('💛', 'The Care'), ('🌱', 'The Growth'),
            ('🧠', 'The Thinker'), ('🎯', 'The Focus'), ('🌉', 'The Bridge'),
            ('🥂', 'Next Chapter'), ('✨', 'The Impact'), ('🌻', 'The Warmth'),
            ('📝', 'The Teacher'),
        ],
    },
    'maureen': {
        'name': 'Maureen',
        'role': 'Assistant to the Dean · Administration',
        'tagline': 'The Rock &nbsp;·&nbsp; The Gardener &nbsp;·&nbsp; The Artist &nbsp;·&nbsp; The Guide',
        'closing_head': 'Still Growing',
        'closing_body': 'Every Christmas cactus cutting she shared will flower again this winter. Every process she guided someone through made them a little more capable. The garden she tended — of plants and people — keeps growing.',
        'color':       '#5C1A8A',
        'color_dark':  '#380D52',
        'color_mid':   '#7A2AAA',
        'color_light': '#F2E8FA',
        'pillars': [
            ('🌱', 'The Gardener', 'Her office was a jungle. Her care grew things — plants and people alike.'),
            ('🪨', 'The Rock',     'Steady, reliable, essential. The SBA ran because Maureen made it run.'),
            ('🎨', 'The Artist',   'In London, at a museum, she revealed an artist within — still blooming.'),
            ('🌸', 'The Grace',    'Patient with late receipts. Generous with her time. Kind in every interaction.'),
        ],
        'concepts': [
            ('🌱', 'The Gardener'), ('🪨', 'The Rock'), ('🎨', 'The Artist'),
            ('🌸', 'The Grace'), ('🗂️', 'The Guide'), ('🚶', 'The Partner'),
            ('🏛️', 'The Foundation'), ('💛', 'The Warmth'), ('🌿', 'The Nurturer'),
            ('✨', 'The Steady'), ('🤗', 'The Welcome'), ('🎊', 'The Joy'),
            ('💬', 'The Conversation'), ('🌺', 'The Bloom'), ('⭐', 'The Presence'),
            ('🔑', 'The Key'), ('💌', 'The Care'), ('🌻', 'The Sunshine'),
            ('💎', 'The Gem'), ('🏡', 'The Heart'), ('🌹', 'The Kindness'),
            ('⚓', 'The Anchor'), ('🦋', 'The Change'), ('🌟', 'The Legacy'),
            ('🎵', 'The Spirit'), ('🌊', 'The Constant'),
        ],
    },
}

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'

# ─── Helpers ─────────────────────────────────────────────────────────────────

def stories(key):
    return [en for en in DATA[key] if en.get('story','').strip()]

def messages(key):
    return [en for en in DATA[key] if en.get('message','').strip()]

def all_entries(key):
    return [en for en in DATA[key] if en.get('story','').strip() or en.get('message','').strip()]

# ─── INDEX page ──────────────────────────────────────────────────────────────

def build_index(key, cfg):
    c = cfg['color']
    cd = cfg['color_dark']
    name = cfg['name']
    n_stories = len(stories(key))
    n_messages = len(messages(key))

    # Pre-compute wall preview cells (avoids backslash in f-string expression)
    wall_cells = ''.join(
        f'<div style="height:30px;border-radius:4px;background:{c}; opacity:{0.4 + 0.15*i:.2f};"></div>'
        for i in range(12)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · Retirement Tribute · Gonzaga SBA 2026</title>
  {FONTS}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --navy: #001A4E; --gold: #C8952A; --gold-lt: #F5E6C8;
      --cream: #FDFBF6; --accent: {c};
    }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family: 'Inter', sans-serif; background: var(--navy); color: white; min-height: 100vh; }}
    .header {{ padding: 2.5rem 3rem 0; display: flex; align-items: center; justify-content: center; }}
    .header img {{ height: 42px; filter: brightness(0) invert(1); opacity: .7; }}
    .hero {{ text-align: center; padding: 3.5rem 2rem 3rem; }}
    .hero-eyebrow {{ font-size: .68rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: 1rem; }}
    .hero-name {{ font-family: 'Playfair Display', serif; font-size: clamp(3.5rem, 12vw, 7rem); font-weight: 700; color: white; line-height: .95; }}
    .hero-sub {{ font-size: clamp(.85rem, 1.8vw, 1rem); color: rgba(255,255,255,.4); margin-top: 1.25rem; letter-spacing: .05em; }}
    .hero-divider {{ width: 48px; height: 2px; background: var(--gold); margin: 1.75rem auto 0; border-radius: 2px; }}
    .intro {{ text-align: center; max-width: 560px; margin: 2rem auto 0; padding: 0 2rem; font-size: .88rem; line-height: 1.75; color: rgba(255,255,255,.45); }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; max-width: 1100px; margin: 3.5rem auto 0; padding: 0 2.5rem 4rem; }}
    .option-card {{ background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.1); border-radius: 16px; overflow: hidden; display: flex; flex-direction: column; transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease; text-decoration: none; color: inherit; }}
    .option-card:hover {{ transform: translateY(-6px); box-shadow: 0 24px 60px rgba(0,0,0,.4); border-color: rgba(200,149,42,.4); }}
    .card-preview {{ height: 180px; background: {cfg['color_dark']}; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }}
    .preview-name {{ font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700; color: white; text-align: center; }}
    .preview-sub {{ font-size: .6rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); text-align: center; margin-top: .4rem; }}
    .card-body {{ padding: 1.5rem 1.6rem 1.75rem; flex: 1; display: flex; flex-direction: column; }}
    .card-badge {{ display: inline-block; font-size: .58rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--gold); background: rgba(200,149,42,.12); border: 1px solid rgba(200,149,42,.25); padding: .25rem .65rem; border-radius: 100px; margin-bottom: .9rem; }}
    .card-title {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: white; line-height: 1.2; margin-bottom: .7rem; }}
    .card-desc {{ font-size: .8rem; line-height: 1.7; color: rgba(255,255,255,.45); flex: 1; }}
    .card-cta {{ display: inline-flex; align-items: center; gap: .45rem; margin-top: 1.25rem; font-size: .75rem; font-weight: 700; letter-spacing: .06em; color: var(--gold); transition: gap .2s ease; }}
    .option-card:hover .card-cta {{ gap: .75rem; }}
    footer {{ text-align: center; padding: 2rem; border-top: 1px solid rgba(255,255,255,.07); font-size: .68rem; color: rgba(255,255,255,.2); letter-spacing: .05em; }}
  </style>
</head>
<body>

<div class="header">
  <img src="source/sba-logo.png" alt="Gonzaga University School of Business Administration">
</div>

<div class="hero">
  <div class="hero-eyebrow">Retirement Tribute &nbsp;·&nbsp; Gonzaga SBA &nbsp;·&nbsp; Spring 2026</div>
  <h1 class="hero-name">{name}</h1>
  <p class="hero-sub">{cfg['tagline']}</p>
  <div class="hero-divider"></div>
</div>

<p class="intro">
  {n_messages} messages and {n_stories} stories from colleagues across the SBA.
  Choose how you&rsquo;d like to experience them.
</p>

<div class="cards">

  <a href="tribute.html" class="option-card">
    <div class="card-preview">
      <div>
        <div class="preview-name">{name}</div>
        <div class="preview-sub">Retirement Celebration</div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-badge">Option A · Scrolling Story</div>
      <h2 class="card-title">The Full Journey</h2>
      <p class="card-desc">Scroll through animated sections — stories, voices, letters, and a closing tribute. Switch to <strong style="color:rgba(255,255,255,.65)">Kiosk Mode</strong> for a full-screen auto-advancing presentation built for a TV or projector.</p>
      <div class="card-cta">Open Experience →</div>
    </div>
  </a>

  <a href="wall.html" class="option-card">
    <div class="card-preview" style="background: #0D1829; padding: .75rem;">
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;width:100%;">
        {wall_cells}
      </div>
    </div>
    <div class="card-body">
      <div class="card-badge">Option B · Memory Wall</div>
      <h2 class="card-title">Memory Wall</h2>
      <p class="card-desc">Flip cards, each labeled with the <strong style="color:rgba(255,255,255,.65)">theme of its message</strong> rather than who wrote it. Hover to reveal the full quote. Filter by theme or shuffle for a new arrangement.</p>
      <div class="card-cta">Explore Wall →</div>
    </div>
  </a>

  <a href="keepsake.html" class="option-card">
    <div class="card-preview" style="background: #F4F1EB;">
      <div style="width:120px;background:white;border-radius:3px;box-shadow:0 8px 32px rgba(0,0,0,.18);padding:.8rem .7rem;display:flex;flex-direction:column;gap:.35rem;">
        <div style="height:9px;background:{cfg['color']};border-radius:2px;width:75%;"></div>
        <div style="height:12px;background:{cfg['color']};border-radius:2px;width:50%;margin-top:.2rem;"></div>
        <div style="height:5px;border-radius:2px;background:#E0D8C8;"></div>
        <div style="height:5px;border-radius:2px;background:#E0D8C8;width:80%;"></div>
        <div style="height:5px;border-radius:2px;background:#E0D8C8;width:65%;"></div>
        <div style="height:5px;border-radius:2px;background:#E0D8C8;"></div>
        <div style="height:5px;border-radius:2px;background:#E0D8C8;width:75%;"></div>
      </div>
    </div>
    <div class="card-body">
      <div class="card-badge">Option C · Print Keepsake</div>
      <h2 class="card-title">Printable Tribute</h2>
      <p class="card-desc">A beautifully formatted document with every message and memory in full. Open in a browser and use <strong style="color:rgba(255,255,255,.65)">File → Print → Save as PDF</strong> to create a keepsake to give at the retirement event.</p>
      <div class="card-cta">View Keepsake →</div>
    </div>
  </a>

</div>

<footer>
  Gonzaga University &nbsp;·&nbsp; School of Business Administration &nbsp;·&nbsp; Spring 2026 &nbsp;·&nbsp; Retirement Tributes
</footer>

</body>
</html>"""

# ─── KEEPSAKE page ────────────────────────────────────────────────────────────

def build_keepsake(key, cfg):
    name = cfg['name']
    c = cfg['color']
    entries = all_entries(key)

    story_cards = ''
    msg_cards = ''

    for en in entries:
        s = en.get('story','').strip()
        m = en.get('message','').strip()
        if s:
            story_cards += f"""
        <div style="background:white;border:1px solid #D6CEBC;border-radius:6px;padding:.7rem .85rem;break-inside:avoid;margin-bottom:.55rem;">
          <p style="font-size:.78rem;line-height:1.75;color:#2A2218;">{ebr(s)}</p>
        </div>"""
        if m:
            msg_cards += f"""
        <div style="background:white;border:1px solid #D6CEBC;border-radius:6px;padding:.7rem .85rem;break-inside:avoid;margin-bottom:.55rem;">
          <p style="font-size:.78rem;line-height:1.75;color:#2A2218;">{ebr(m)}</p>
        </div>"""

    # Pick longest story as hero quote
    hero = max(entries, key=lambda x: len(x.get('message','') or x.get('story','')))
    hero_text = (hero.get('message') or hero.get('story',''))[:300]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · Retirement Keepsake · Gonzaga SBA 2026</title>
  {FONTS}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: #E8E3D8; color: #1A1610; }}
    .page {{ width: 8.5in; min-height: 11in; margin: .4in auto; background: #FDFBF7; display: flex; flex-direction: column; overflow: hidden; page-break-after: always; }}
    .page-header {{ background: {c}; padding: .4in .6in .3in; display: flex; align-items: center; justify-content: space-between; }}
    .page-header img {{ height: 44px; filter: brightness(0) invert(1); opacity: .9; }}
    .header-name {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: white; line-height: 1; text-align: right; }}
    .header-label {{ font-size: .58rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: rgba(255,255,255,.5); margin-top: .2rem; text-align: right; }}
    .page-body {{ flex: 1; padding: .4in .6in .3in; display: flex; flex-direction: column; gap: .28in; }}
    .nameplate {{ text-align: center; padding-bottom: .22in; border-bottom: 1.5px solid #D6CEBC; }}
    .nameplate-eyebrow {{ font-size: .62rem; font-weight: 600; letter-spacing: .18em; text-transform: uppercase; color: {c}; margin-bottom: .35rem; }}
    .nameplate h1 {{ font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 700; color: #002469; line-height: 1.1; margin-bottom: .2rem; }}
    .nameplate-sub {{ font-size: .72rem; color: #5A5243; }}
    .hero-quote {{ background: {c}; border-radius: 6px; padding: .35in .4in; position: relative; }}
    .hero-quote p {{ font-family: 'Playfair Display', serif; font-size: .95rem; font-style: italic; line-height: 1.7; color: white; }}
    .hero-quote::before {{ content: '\\201C'; font-family: 'Playfair Display', serif; font-size: 4rem; color: rgba(255,255,255,.2); position: absolute; top: .1in; left: .2in; line-height: 1; }}
    .section-label {{ font-size: .6rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: {c}; border-bottom: 1.5px solid #D6CEBC; padding-bottom: .1in; margin-bottom: .18in; }}
    .cols {{ columns: 2; column-gap: .3in; }}
    @media print {{
      body {{ background: white; }}
      .page {{ width: 100%; margin: 0; box-shadow: none; min-height: 100vh; }}
    }}
  </style>
</head>
<body>

<!-- PAGE 1: Cover -->
<div class="page">
  <div class="page-header">
    <img src="source/sba-logo.png" alt="Gonzaga University School of Business Administration">
    <div>
      <div class="header-name">{name}</div>
      <div class="header-label">Retirement Tribute · Spring 2026</div>
    </div>
  </div>
  <div class="page-body">
    <div class="nameplate">
      <div class="nameplate-eyebrow">Gonzaga SBA · Spring 2026</div>
      <h1>{name}</h1>
      <p class="nameplate-sub">{e(cfg['role'])}</p>
    </div>
    <div class="hero-quote">
      <p>{ebr(hero_text)}</p>
    </div>
    <div>
      <div class="section-label">Stories &amp; Memories</div>
      <div class="cols">{story_cards}</div>
    </div>
  </div>
</div>

<!-- PAGE 2: All Messages -->
<div class="page">
  <div class="page-header">
    <img src="source/sba-logo.png" alt="Gonzaga University School of Business Administration">
    <div>
      <div class="header-name">{name}</div>
      <div class="header-label">Messages from Colleagues</div>
    </div>
  </div>
  <div class="page-body">
    <div>
      <div class="section-label">Messages from Colleagues</div>
      <div class="cols">{msg_cards}</div>
    </div>
  </div>
</div>

</body>
</html>"""

# ─── WALL page ───────────────────────────────────────────────────────────────

def build_wall(key, cfg):
    name = cfg['name']
    c = cfg['color']
    cd = cfg['color_dark']
    cl = cfg['color_light']
    entries = all_entries(key)
    concepts = cfg['concepts']

    cards_html = ''
    for i, en in enumerate(entries):
        text = en.get('message','').strip() or en.get('story','').strip()
        if not text:
            continue
        emoji, label = concepts[i % len(concepts)]
        qlen = len(text)
        if qlen < 80:   qsize = '1rem'
        elif qlen < 160: qsize = '.88rem'
        elif qlen < 260: qsize = '.78rem'
        else:            qsize = '.68rem'

        cards_html += f"""
    <div class="card-wrap">
      <div class="card-inner">
        <div class="card-face card-front" style="background:{cd};">
          <div style="font-size:2.5rem;line-height:1;margin-bottom:.75rem;">{emoji}</div>
          <div style="font-family:'Playfair Display',serif;font-size:1.15rem;font-style:italic;color:white;text-align:center;line-height:1.25;">{e(label)}</div>
        </div>
        <div class="card-face card-back" style="background:{cl};">
          <p style="font-family:'Playfair Display',serif;font-size:{qsize};font-style:italic;line-height:1.6;color:{cd};text-align:center;">{ebr(text)}</p>
        </div>
      </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · Memory Wall · Gonzaga SBA 2026</title>
  {FONTS}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: #0D1829; color: white; min-height: 100vh; }}
    .top-bar {{ background: #001040; padding: 1.25rem 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid rgba(255,255,255,.08); }}
    .top-bar-left {{ display: flex; align-items: center; gap: 1rem; }}
    .top-bar img {{ height: 32px; filter: brightness(0) invert(1); opacity: .6; }}
    .top-bar-title {{ font-family: 'Playfair Display', serif; font-size: 1.2rem; font-style: italic; color: white; }}
    .top-bar-sub {{ font-size: .65rem; color: rgba(255,255,255,.35); letter-spacing: .08em; text-transform: uppercase; }}
    .controls {{ display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; }}
    .ctrl-btn {{ background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.15); color: rgba(255,255,255,.7); font-family: 'Inter', sans-serif; font-size: .7rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; padding: .4rem .9rem; border-radius: 100px; cursor: pointer; transition: background .2s, color .2s; }}
    .ctrl-btn:hover, .ctrl-btn.active {{ background: {c}; border-color: {c}; color: white; }}
    .wall {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; padding: 1.5rem 2rem 3rem; max-width: 1400px; margin: 0 auto; }}
    .card-wrap {{ height: 220px; perspective: 1000px; cursor: pointer; }}
    .card-inner {{ position: relative; width: 100%; height: 100%; transform-style: preserve-3d; transition: transform .6s cubic-bezier(.4,0,.2,1); }}
    .card-wrap:hover .card-inner {{ transform: rotateY(180deg); }}
    .card-face {{ position: absolute; inset: 0; border-radius: 12px; backface-visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 1.25rem 1rem; overflow: hidden; }}
    .card-back {{ transform: rotateY(180deg); }}
    footer {{ text-align: center; padding: 1.5rem; border-top: 1px solid rgba(255,255,255,.07); font-size: .67rem; color: rgba(255,255,255,.2); }}
  </style>
</head>
<body>

<div class="top-bar">
  <div class="top-bar-left">
    <img src="source/sba-logo.png" alt="Gonzaga SBA">
    <div>
      <div class="top-bar-title">{name} · Memory Wall</div>
      <div class="top-bar-sub">Hover any card to reveal the message</div>
    </div>
  </div>
  <div class="controls">
    <button class="ctrl-btn active" onclick="shuffle()">⇄ Shuffle</button>
    <a href="index.html" class="ctrl-btn" style="text-decoration:none;">← Back</a>
  </div>
</div>

<div class="wall" id="wall">
{cards_html}
</div>

<footer>Gonzaga University · School of Business Administration · Spring 2026</footer>

<script>
  function shuffle() {{
    const wall = document.getElementById('wall');
    const cards = [...wall.children];
    cards.sort(() => Math.random() - .5);
    cards.forEach(c => wall.appendChild(c));
  }}
</script>
</body>
</html>"""

# ─── TRIBUTE page (scrolling + kiosk) ────────────────────────────────────────

def build_tribute(key, cfg):
    name = cfg['name']
    c = cfg['color']
    cd = cfg['color_dark']
    cm = cfg['color_mid']
    cl = cfg['color_light']
    all_msgs = messages(key)
    all_stories = stories(key)
    entries = all_entries(key)

    # Pillar blocks
    pillars_html = ''
    for emoji, title, desc in cfg['pillars']:
        pillars_html += f"""
        <div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:1.5rem;text-align:center;">
          <div style="font-size:2rem;margin-bottom:.75rem;">{emoji}</div>
          <h3 style="font-family:'Playfair Display',serif;font-size:1rem;font-style:italic;color:white;margin-bottom:.5rem;">{e(title)}</h3>
          <p style="font-size:.78rem;line-height:1.65;color:rgba(255,255,255,.5);">{e(desc)}</p>
        </div>"""

    # Story cards (all stories)
    stories_html = ''
    for i, en in enumerate(all_stories):
        align = 'left' if i % 2 == 0 else 'right'
        concepts = cfg['concepts']
        emoji, label = concepts[i % len(concepts)]
        stories_html += f"""
        <div class="reveal" style="display:flex;flex-direction:column;gap:1rem;max-width:680px;{'margin-right:auto' if align=='left' else 'margin-left:auto'};">
          <div style="display:inline-flex;align-items:center;gap:.5rem;">
            <span style="font-size:1.2rem;">{emoji}</span>
            <span style="font-size:.65rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C8952A;">{e(label)}</span>
          </div>
          <blockquote style="font-family:'Playfair Display',serif;font-size:clamp(.95rem,2vw,1.1rem);font-style:italic;line-height:1.75;color:rgba(255,255,255,.88);border-left:3px solid {c};padding-left:1.25rem;">{ebr(en['story'])}</blockquote>
        </div>"""

    # Voice cards (all messages)
    voices_html = ''
    for i, en in enumerate(all_msgs):
        concepts = cfg['concepts']
        emoji, label = concepts[i % len(concepts)]
        voices_html += f"""
        <div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:1.25rem;">
          <p style="font-size:.65rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#C8952A;margin-bottom:.6rem;">{e(label)}</p>
          <p style="font-family:'Playfair Display',serif;font-size:.88rem;font-style:italic;line-height:1.7;color:rgba(255,255,255,.8);">{ebr(en['message'])}</p>
        </div>"""

    # Kiosk slides (all entries: stories + messages)
    slides = []
    for en in entries:
        if en.get('story','').strip():
            slides.append({'text': en['story'], 'label': 'Story'})
        if en.get('message','').strip():
            slides.append({'text': en['message'], 'label': 'Message'})

    slides_js = json.dumps(slides, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} · Retirement Tribute · Gonzaga SBA 2026</title>
  {FONTS}
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{ --c: {c}; --cd: {cd}; --gold: #C8952A; }}
    html {{ scroll-behavior: smooth; }}
    body {{ font-family: 'Inter', sans-serif; background: #001030; color: white; }}
    section {{ min-height: 100vh; display: flex; flex-direction: column; justify-content: center; padding: 5rem 2rem; }}
    .inner {{ max-width: 900px; margin: 0 auto; width: 100%; }}
    .eyebrow {{ font-size: .65rem; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: 1rem; }}
    h2 {{ font-family: 'Playfair Display', serif; font-size: clamp(2rem,6vw,3.5rem); font-style: italic; line-height: 1.1; margin-bottom: 1.25rem; }}
    .reveal {{ opacity: 0; transform: translateY(28px); transition: opacity .7s ease, transform .7s ease; }}
    .reveal.visible {{ opacity: 1; transform: none; }}
    .pillar-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-top: 2rem; }}
    .stories-stack {{ display: flex; flex-direction: column; gap: 2.5rem; margin-top: 2rem; }}
    .voices-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-top: 2rem; }}
    .back-btn {{ position: fixed; top: 1rem; left: 1rem; z-index: 100; background: rgba(0,0,0,.5); border: 1px solid rgba(255,255,255,.15); color: rgba(255,255,255,.7); font-family: 'Inter', sans-serif; font-size: .72rem; padding: .45rem .9rem; border-radius: 100px; text-decoration: none; }}
    .kiosk-btn {{ position: fixed; top: 1rem; right: 1rem; z-index: 100; background: var(--c); color: white; font-family: 'Inter', sans-serif; font-size: .72rem; font-weight: 600; padding: .45rem .9rem; border-radius: 100px; border: none; cursor: pointer; }}

    /* ── KIOSK ── */
    #kiosk {{ display: none; position: fixed; inset: 0; background: var(--cd); z-index: 9999; flex-direction: column; align-items: center; justify-content: center; padding: 3rem; }}
    #kiosk.active {{ display: flex; }}
    #kiosk-label {{ font-size: .65rem; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: var(--gold); margin-bottom: 1.5rem; }}
    #kiosk-text {{ font-family: 'Playfair Display', serif; font-size: clamp(1.1rem,3vw,2rem); font-style: italic; line-height: 1.6; color: white; text-align: center; max-width: 900px; }}
    #kiosk-name {{ margin-top: 2rem; font-family: 'Playfair Display', serif; font-size: clamp(1.8rem,5vw,3.5rem); font-weight: 700; color: white; opacity: .15; }}
    #kiosk-prog {{ position: absolute; bottom: 0; left: 0; height: 3px; background: var(--gold); transition: width linear; }}
    #kiosk-counter {{ position: absolute; bottom: 1rem; right: 1.5rem; font-size: .65rem; color: rgba(255,255,255,.3); }}
    #kiosk-close {{ position: absolute; top: 1rem; right: 1rem; background: rgba(255,255,255,.1); border: none; color: rgba(255,255,255,.6); font-size: .75rem; padding: .4rem .8rem; border-radius: 100px; cursor: pointer; font-family: 'Inter', sans-serif; }}
  </style>
</head>
<body>

<a href="index.html" class="back-btn">← Back</a>
<button class="kiosk-btn" onclick="startKiosk()">⊞ Kiosk Mode</button>

<!-- HERO -->
<section style="background: linear-gradient(160deg, {cd} 0%, #001030 100%);">
  <div class="inner" style="text-align:center;">
    <p class="eyebrow reveal">Retirement Tribute &nbsp;·&nbsp; Gonzaga SBA &nbsp;·&nbsp; Spring 2026</p>
    <h1 style="font-family:'Playfair Display',serif;font-size:clamp(4rem,14vw,9rem);font-weight:700;color:white;line-height:.9;" class="reveal">{name}</h1>
    <p style="font-size:clamp(.8rem,2vw,.95rem);color:rgba(255,255,255,.4);margin-top:1.25rem;letter-spacing:.06em;" class="reveal">{cfg['tagline']}</p>
    <div style="width:48px;height:2px;background:#C8952A;margin:2rem auto 0;border-radius:2px;" class="reveal"></div>
  </div>
</section>

<!-- PILLARS -->
<section style="background:#001030;">
  <div class="inner">
    <p class="eyebrow reveal">Who They Are</p>
    <h2 class="reveal">Four ways to know {name}.</h2>
    <div class="pillar-grid">
      {pillars_html}
    </div>
  </div>
</section>

<!-- STORIES -->
<section style="background: linear-gradient(180deg, #001030 0%, {cd}22 100%);">
  <div class="inner">
    <p class="eyebrow reveal">Stories &amp; Memories</p>
    <h2 class="reveal">Moments that stick.</h2>
    <div class="stories-stack">
      {stories_html}
    </div>
  </div>
</section>

<!-- VOICES -->
<section style="background:#000D26;">
  <div class="inner">
    <p class="eyebrow reveal">Voices</p>
    <h2 class="reveal">What colleagues say.</h2>
    <div class="voices-grid">
      {voices_html}
    </div>
  </div>
</section>

<!-- CLOSING -->
<section style="background: linear-gradient(160deg, {cd} 0%, #001030 100%);">
  <div class="inner" style="text-align:center;">
    <p class="eyebrow reveal">From All of Us</p>
    <h2 class="reveal" style="color:white;">{e(cfg['closing_head'])}</h2>
    <p style="font-size:clamp(.9rem,2vw,1.1rem);line-height:1.8;color:rgba(255,255,255,.6);max-width:620px;margin:0 auto;" class="reveal">{e(cfg['closing_body'])}</p>
    <div style="width:48px;height:2px;background:#C8952A;margin:2.5rem auto 0;border-radius:2px;"></div>
    <p style="margin-top:1.5rem;font-size:.72rem;color:rgba(255,255,255,.2);letter-spacing:.08em;text-transform:uppercase;">Gonzaga University · School of Business Administration · Spring 2026</p>
  </div>
</section>

<!-- KIOSK OVERLAY -->
<div id="kiosk">
  <button id="kiosk-close" onclick="stopKiosk()">✕ Exit</button>
  <div id="kiosk-label">Memory</div>
  <div id="kiosk-text"></div>
  <div id="kiosk-name">{name}</div>
  <div id="kiosk-prog"></div>
  <div id="kiosk-counter"></div>
</div>

<script>
  // ── Scroll reveal ──
  const obs = new IntersectionObserver(els => els.forEach(el => {{ if (el.isIntersecting) el.target.classList.add('visible'); }}), {{ threshold: 0.15 }});
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

  // ── Kiosk ──
  const SLIDES = {slides_js};
  const INTERVAL = 9000;
  let cur = 0, timer = null, prog = null;

  function showSlide(n) {{
    cur = (n + SLIDES.length) % SLIDES.length;
    const s = SLIDES[cur];
    document.getElementById('kiosk-label').textContent = s.label;
    document.getElementById('kiosk-text').textContent = s.text;
    document.getElementById('kiosk-counter').textContent = (cur + 1) + ' / ' + SLIDES.length;
    const bar = document.getElementById('kiosk-prog');
    bar.style.transition = 'none'; bar.style.width = '0%';
    requestAnimationFrame(() => {{
      requestAnimationFrame(() => {{
        bar.style.transition = 'width ' + INTERVAL + 'ms linear';
        bar.style.width = '100%';
      }});
    }});
  }}

  function startKiosk() {{
    document.getElementById('kiosk').classList.add('active');
    showSlide(0);
    timer = setInterval(() => showSlide(cur + 1), INTERVAL);
    document.addEventListener('keydown', kioskKey);
    document.getElementById('kiosk').addEventListener('click', () => {{ clearInterval(timer); showSlide(cur + 1); timer = setInterval(() => showSlide(cur + 1), INTERVAL); }});
  }}

  function stopKiosk() {{
    clearInterval(timer);
    document.getElementById('kiosk').classList.remove('active');
    document.removeEventListener('keydown', kioskKey);
  }}

  function kioskKey(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{ clearInterval(timer); showSlide(cur + 1); timer = setInterval(() => showSlide(cur + 1), INTERVAL); }}
    if (e.key === 'ArrowLeft') {{ clearInterval(timer); showSlide(cur - 1); timer = setInterval(() => showSlide(cur + 1), INTERVAL); }}
    if (e.key === 'Escape') stopKiosk();
  }}
</script>
</body>
</html>"""

# ─── Build all pages ──────────────────────────────────────────────────────────

for key, cfg in PEOPLE.items():
    folder = os.path.join(BASE, key)
    os.makedirs(folder, exist_ok=True)

    pages = {
        'index.html':    build_index(key, cfg),
        'keepsake.html': build_keepsake(key, cfg),
        'wall.html':     build_wall(key, cfg),
        'tribute.html':  build_tribute(key, cfg),
    }

    for filename, content in pages.items():
        path = os.path.join(folder, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✓  {key}/{filename}')

print('\nDone.')
