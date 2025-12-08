from collections import defaultdict
from datetime import date
from pathlib import Path

import feedparser
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"
DIGEST_ROOT = "digests"


# -------- config --------

def load_config(path=CONFIG_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# -------- core logic --------

def fetch_headlines(feeds, max_per_feed):
    items = []
    for f in feeds:
        d = feedparser.parse(f["url"])
        for e in d.entries[:max_per_feed]:
            title = getattr(e, "title", "").strip()
            link = getattr(e, "link", "").strip()
            if not title:
                continue
            items.append(
                {
                    "source_id": f["id"],
                    "source_name": f["name"],
                    "lang": f["lang"],
                    "category": f.get("category", "Uncategorized"),
                    "title": title,
                    "link": link,
                }
            )
    return items


def dedupe(items):
    seen, out = set(), []
    for x in items:
        key = (x["lang"], x["category"], x["title"].lower())
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out


def group_by_category(items):
    grouped = defaultdict(list)
    for it in items:
        grouped[it["category"]].append(it)
    return grouped


def export_markdown(grouped, lang, date_format, root=DIGEST_ROOT):
    today = date.today()
    year_dir = Path(root) / lang / str(today.year)
    year_dir.mkdir(parents=True, exist_ok=True)

    fname = today.strftime(date_format) + ".md"
    path = year_dir / fname

    lines = [f"# Daily News Digest ({lang}) – {today.strftime(date_format)}", ""]

    for category in sorted(grouped.keys()):
        lines.append(f"## {category}")
        lines.append("")
        for item in grouped[category]:
            # - [Source] Headline ([link](...))
            lines.append(
                f"- [{item['source_name']}] {item['title']} "
                f"([link]({item['link']}))"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_for_lang(cfg, lang):
    feeds = [f for f in cfg["feeds"] if f.get("lang") == lang]
    if not feeds:
        return None

    max_per_feed = cfg.get("max_per_feed", 30)
    dfmt = cfg.get("date_format", "%Y-%m-%d")

    items = fetch_headlines(feeds, max_per_feed)
    items = dedupe(items)
    grouped = group_by_category(items)
    return export_markdown(grouped, lang, dfmt)


def main():
    cfg = load_config()

    paths = []
    for lang in ("en", "ko"):
        p = run_for_lang(cfg, lang)
        if p:
            paths.append(p)

    for p in paths:
        print("Saved:", p)


if __name__ == "__main__":
    main()
