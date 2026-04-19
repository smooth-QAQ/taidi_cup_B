"""
批量修改所有提示词文件 - 去除越南特定内容
"""
import os
import re

base = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

# 定义每个文件的修改内容
modifications = {
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md": {
        "replacements": [
            ("top Vietnamese firms", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("based on VAS regulation", "based on regulatory classifications"),
            ("HOSE", "the applicable exchange"),
            ("Vietnamese", "companies"),
            ("Million VND", "appropriate currency units"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin_extend.md": {
        "replacements": [
            ("Vietnamese", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
            ("Million VND", "appropriate currency units"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin_extend.md": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
            ("Million VND", "appropriate currency units"),
            ("Q3 2024", "the most recent period"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin.md": {
        "replacements": [
            ("Vietnamese", "companies"),
            ("VAS", "applicable accounting standards"),
            ("VND", "currency units"),
            ("HOSE", "applicable exchange"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_short_fiin.md": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard", "applicable accounting standards"),
            ("Million VND", "units"),
            ("Q3 2024", "the most recent period"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
            ("Million VND", "currency units"),
            ("HOSE", "primary exchange"),
            ("HNX", "secondary exchange"),
            ("VN30", "major indices"),
            ("HNX30", "major indices"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/base/simple_query_v2.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese", "companies"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/vertical/universal/simple_query_v2.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese", "companies"),
            ("VAS", "applicable standards"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_simplify.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_short.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese", "companies"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/general/branch_reasoning_text2sql.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
            ("VAS", "applicable accounting standards"),
        ]
    },
    "chatbot_financial_statement/agent/prompt/chat/summarize.txt": {
        "replacements": [
            ("Vietnamese companies", "companies"),
            ("Million VND", "currency units"),
            ("Q3 2024", "the most recent period"),
        ]
    },
}

def process_file(rel_path, reps):
    full = os.path.join(base, rel_path)
    if not os.path.exists(full):
        print(f"⚠️  Not found: {rel_path}")
        return False

    try:
        with open(full, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content

        for old, new in reps:
            content = content.replace(old, new)

        # 正则替换
        content = re.sub(r'\bVietnamese\b', 'companies', content, flags=re.IGNORECASE)
        content = re.sub(r'\bMillion VND\b', 'appropriate currency units', content)
        content = re.sub(r'\bQ3 2024\b', 'the most recent available period', content)
        content = re.sub(r'\bVND\b', 'currency units', content, flags=re.IGNORECASE)
        content = re.sub(r'\bHOSE\b', 'the applicable exchange', content)
        content = re.sub(r'\bHNX\b', 'the applicable exchange', content)
        content = re.sub(r'\bVN30\b', 'major stock indices', content)
        content = re.sub(r'\bHNX30\b', 'major stock indices', content)

        # 清理空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original:
            with open(full, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ {rel_path}: {e}")
        return None

print("批量修改提示词文件...")
print("="*60)
modified = 0
unchanged = 0

for rel_path, config in modifications.items():
    result = process_file(rel_path, config["replacements"])
    if result is True:
        print(f"✅ {rel_path}")
        modified += 1
    elif result is False:
        print(f"⏭️  {rel_path} (no change needed)")
        unchanged += 1
    else:
        print(f"❌ {rel_path} (error)")

print("="*60)
print(f"\n完成！修改: {modified}, 无需修改: {unchanged}")
