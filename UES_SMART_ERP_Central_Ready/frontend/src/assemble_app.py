#!/usr/bin/env python3
"""
Assembles the complete UES SMART ERP Desktop & Canvas Web Application
and verifies it with check_web_app.py.
"""
import os
import json
from head_part import HEAD_HTML
from core_js_part import CORE_JS
from views_part1 import VIEWS_PART1_JS
from views_part2 import VIEWS_PART2_JS
from views_part3 import VIEWS_PART3_JS
from handlers_part import HANDLERS_JS
from events_part import EVENTS_JS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_PATH = os.path.join(BASE_DIR, "db_snapshot.json")
DIST_DIR = os.path.abspath(os.path.join(BASE_DIR, "../dist"))
OUT_CANVAS = os.environ.get("UES_OPTIONAL_CANVAS_EXPORT", "")

def build():
    os.makedirs(DIST_DIR, exist_ok=True)
    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        full_seed = json.load(f)
        # Never embed usernames, password hashes, tokens, or client records in HTML.
        seed_json_str = json.dumps({key: [] for key in full_seed if isinstance(full_seed[key], list)}, ensure_ascii=False)

    script = ("(function(){\n'use strict';\n" + f"const SEED_DB = {seed_json_str};\n" + CORE_JS + "\n" + VIEWS_PART1_JS + "\n" + VIEWS_PART2_JS + "\n" + VIEWS_PART3_JS + "\n" + HANDLERS_JS + "\n" + EVENTS_JS + "\n})();\n")
    os.makedirs(os.path.join(DIST_DIR,"assets"),exist_ok=True)
    with open(os.path.join(DIST_DIR,"assets","ues-app.js"),"w",encoding="utf8") as f:
        f.write(script)
    full_html = HEAD_HTML + '\n<script src="/assets/ues-app.js" defer></script>\n</body>\n</html>\n'
    dist_file = os.path.join(DIST_DIR,"UES_SMART_ERP.html")
    with open(dist_file,"w",encoding="utf8") as f: f.write(full_html)
    if OUT_CANVAS:
        os.makedirs(os.path.dirname(OUT_CANVAS), exist_ok=True)
        with open(OUT_CANVAS,"w",encoding="utf8") as f: f.write(full_html)

    print(f"Built UES_SMART_ERP.html ({len(full_html)} bytes)")

if __name__ == "__main__":
    build()
