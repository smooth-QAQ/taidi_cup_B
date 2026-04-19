"""
执行批量修改
"""
import os
import re

base = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

files_map = {
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md": [
        ("top Vietnamese firms", "companies"),
        ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
        ("based on VAS regulation", "based on regulatory classifications"),
        ("HOSE", "the applicable exchange"),
    ],
    "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md": [
        ("Vietnamese companies", "companies"),
        ("Vietnamese Accounting Standard", "applicable accounting standards"),
        ("VAS", "applicable accounting standards"),
        ("Million VND", "currency units"),
    ],
}

count = 0
for rel, reps in files_map.items():
    fp = os.path.join(base, rel)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        orig = c
        for o, n in reps:
            c = c.replace(o, n)
        if c != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"✅ {rel}")
            count += 1
        else:
            print(f"⏭️  {rel}")
    else:
        print(f"⚠️  Not found: {rel}")

print(f"\nDone: {count} files modified")
