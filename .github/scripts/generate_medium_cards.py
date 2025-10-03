#!/usr/bin/env python3
import feedparser, re, html
from bs4 import BeautifulSoup

USER = "ishaileshmishra"
FEED = f"https://medium.com/feed/@{USER}"
OUT = "README_ARTICLES.md"
MAX = 6  # how many items to show

def extract_image(entry):
    # Try to find first image in content, or fall back to placeholder
    if 'content' in entry:
        html_content = entry.content[0].value
        soup = BeautifulSoup(html_content, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img['src']
    # try media_thumbnail
    if 'media_content' in entry:
        return entry.media_content[0].get('url')
    return "https://via.placeholder.com/800x400?text=Medium+Article"

def excerpt(entry, max_chars=160):
    summary = entry.get('summary', '')
    text = BeautifulSoup(summary, 'html.parser').get_text()
    text = html.unescape(text).strip()
    if len(text) > max_chars:
        return text[:max_chars].rsplit(' ',1)[0] + "…"
    return text

feed = feedparser.parse(FEED)
items = feed.entries[:MAX]

card_template = []
card_template.append("## 📚 My Articles\n")
card_template.append("\n<p align=\"center\" style=\"margin-bottom:6px\">A quick look at my latest Medium posts</p>\n")
card_template.append("<div style=\"display:flex; gap:12px; overflow-x:auto; padding:6px 2px; -webkit-overflow-scrolling:touch;\">\n")

for e in items:
    title = e.title
    link = e.link
    img = extract_image(e)
    desc = excerpt(e, 140)
    card = f"""
  <a href="{link}" style="text-decoration:none; color:inherit; display:block; min-width:300px; max-width:320px;">
    <div style="border-radius:8px; overflow:hidden; box-shadow:0 6px 18px rgba(0,0,0,0.15); background:#0f1115;">
      <img alt="{title}" src="{img}" style="width:100%; height:140px; object-fit:cover; display:block;">
      <div style="padding:10px 12px;">
        <h4 style="margin:0 0 6px; font-size:15px;">{title}</h4>
        <p style="margin:0; font-size:13px; color:#bdbdbd; line-height:1.3; max-height:66px; overflow:hidden;">{desc}</p>
        <p style="margin-top:8px; font-size:12px; color:#79ff97;">Read on Medium →</p>
      </div>
    </div>
  </a>
"""
    card_template.append(card)

card_template.append("</div>\n")
card_template.append("\n<p style=\"font-size:12px; color:#9e9e9e; margin-top:8px\">Auto-updated from Medium RSS.</p>\n")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(''.join(card_template))

print(f"Wrote {OUT} with {len(items)} items")
