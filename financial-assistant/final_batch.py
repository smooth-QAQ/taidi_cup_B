"""
一次性修改所有剩余文件
"""
import os, re

base = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

# 所有需要修改的文件及其替换规则
tasks = [
    ("chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md",
     [("Vietnamese firms", "companies"), ("VAS", "applicable accounting standards"), ("HOSE", "applicable exchange")]),
    ("chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin_extend.md",
     [("Vietnamese companies", "companies"), ("VAS", "applicable standards"), ("VND", "currency units")]),
    ("chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin_extend.md",
     [("Vietnamese", "companies"), ("VAS", "applicable standards"), ("Million VND", "currency units")]),
    ("chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin.md",
     [("Vietnamese companies", "companies"), ("VAS", "applicable standards")]),
    ("chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_short_fiin.md",
     [("Vietnamese companies", "companies"), ("Million VND", "units")]),
    ("chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md",
     [("Vietnamese companies", "companies"), ("VAS", "applicable accounting standards"), ("Million VND", "currency units")]),
    ("chatbot_financial_statement/agent/prompt/vertical/base/simple_query_v2.txt",
     [("Vietnamese companies", "companies")]),
    ("chatbot_financial_statement/agent/prompt/vertical/universal/simple_query_v2.txt",
     [("Vietnamese companies", "companies"), ("VAS", "applicable standards")]),
    ("chatbot_financial_statement/agent/prompt/general/reasoning_text2sql.txt",
     [("Vietnamese companies", "companies"), ("Vietnamese", "companies"), ("VAS", "applicable accounting standards")]),
    ("chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_simplify.txt",
     [("Vietnamese companies", "companies"), ("VAS", "applicable accounting standards")]),
    ("chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_short.txt",
     [("Vietnamese companies", "companies")]),
    ("chatbot_financial_statement/agent/prompt/general/branch_reasoning_text2sql.txt",
     [("Vietnamese companies", "companies"), ("VAS", "applicable accounting standards")]),
    ("chatbot_financial_statement/agent/prompt/chat/summarize.txt",
     [("Vietnamese companies", "companies"), ("Million VND", "currency units")]),
]

c = 0
for path, reps in tasks:
    fp = os.path.join(base, path)
    if not os.path.exists(fp):
        print(f"⚠️  Not found: {path}")
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old, new in reps:
        content = content.replace(old, new)
    content = re.sub(r'\bVietnamese\b', 'companies', content, flags=re.IGNORECASE)
    content = re.sub(r'\bVAS\b', 'applicable accounting standards', content, flags=re.IGNORECASE)
    content = re.sub(r'\bMillion VND\b', 'currency units', content)
    content = re.sub(r'\bQ3 2024\b', 'the most recent period', content)
    content = re.sub(r'\bHOSE\b', 'the exchange', content)
    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {os.path.basename(path)}")
        c += 1
    else:
        print(f"⏭️  {os.path.basename(path)}")

print(f"\n✅ Modified {c} files total")
