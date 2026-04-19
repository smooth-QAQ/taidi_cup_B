"""
直接执行修改的脚本 - 不使用Shell
"""
import re

BASE = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

def modify_file(rel_path, replacements):
    """修改文件"""
    full = f"{BASE}\\{rel_path}"
    try:
        with open(full, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        for old, new in replacements:
            content = content.replace(old, new)
        if content != original:
            with open(full, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error {rel_path}: {e}")
        return None

# 定义每个文件的替换规则
tasks = [
    (
        "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_fiin.md",
        [
            ("Vietnamese companies, either bank, cooperates and securities", "companies, including banks, corporations, and securities firms"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("based on VAS regulation", "based on regulatory classifications"),
            ("in Million VND", "in appropriate currency units"),
            ("HOSE", "the applicable exchange"),
            ("HNX", "the applicable exchange"),
            ("VN30", "major stock indices"),
            ("HNX30", "major stock indices"),
        ]
    ),
    (
        "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md",
        [
            ("top Vietnamese firms", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("based on VAS regulation", "based on regulatory classifications"),
            ("HOSE", "applicable exchanges"),
        ]
    ),
    (
        "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md",
        [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
            ("Million VND", "currency units"),
        ]
    ),
]

print("Starting batch modification...")
print("="*60)
count = 0
for path, reps in tasks:
    if modify_file(path, reps):
        print(f"✅ {path}")
        count += 1
    else:
        print(f"⏭️  {path} (no change)")

print("="*60)
print(f"Modified {count} files")
