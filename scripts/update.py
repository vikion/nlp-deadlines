#!/usr/bin/env python3
"""Build data/deadlines.json = curated.json + community data from ccfddl/ccf-deadlines.

Curated entries win: a community venue+year already in curated.json is skipped.
Run: pip install pyyaml && python scripts/update.py
"""
import json, re, sys, urllib.request, urllib.error, datetime as dt
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://raw.githubusercontent.com/ccfddl/ccf-deadlines/main/conference/AI/"
# ccf file -> display name (missing files are skipped)
VENUES = {"acl": "ACL", "emnlp": "EMNLP", "naacl": "NAACL", "eacl": "EACL",
          "coling": "COLING", "lrec": "LREC", "interspeech": "Interspeech",
          "aaai": "AAAI", "ijcai": "IJCAI", "iclr": "ICLR", "icml": "ICML", "nips": "NeurIPS"}
MIN_YEAR = dt.date.today().year

def tz_offset(tz):
    m = re.match(r"UTC([+-])(\d{1,2})(?::?(\d{2}))?$", (tz or "").strip())
    if tz and tz.strip().upper() == "AOE": return "-12:00"
    if not m: return "+00:00"
    return f"{m[1]}{int(m[2]):02d}:{m[3] or '00'}"

def fetch(name):
    try:
        with urllib.request.urlopen(BASE + name + ".yml", timeout=30) as r:
            return yaml.safe_load(r.read())
    except urllib.error.URLError as e:
        print(f"skip {name}: {e}", file=sys.stderr); return None

def main():
    cur = json.loads((ROOT / "data/curated.json").read_text())
    curated = cur["entries"]
    have = {(e["venue"], e["year"]) for e in curated}
    out = list(curated)
    for fname, venue in VENUES.items():
        data = fetch(fname)
        if not data: continue
        for conf in data if isinstance(data, list) else [data]:
            for c in conf.get("confs", []):
                y = c.get("year")
                if not y or y < MIN_YEAR or (venue, y) in have: continue
                for t in c.get("timeline", []):
                    d = str(t.get("deadline", "")).strip()
                    if not re.match(r"\d{4}-\d{2}-\d{2}", d): continue
                    out.append({"venue": venue, "year": y,
                        "label": t.get("comment") or "Submission deadline",
                        "category": "conference",
                        "date": d.replace(" ", "T")[:19] + tz_offset(c.get("timezone")),
                        "event_dates": c.get("date"), "place": c.get("place"),
                        "link": c.get("link"), "source": "ccf-deadlines"})
    (ROOT / "data/deadlines.json").write_text(json.dumps(
        {"generated": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z", "venues": cur.get("venues", {}), "entries": out},
        indent=1, ensure_ascii=False))
    print(f"wrote {len(out)} entries")

if __name__ == "__main__":
    main()
