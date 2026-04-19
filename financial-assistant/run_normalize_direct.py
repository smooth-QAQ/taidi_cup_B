"""
直接执行提示词文件批量修改
不依赖外部Shell执行
"""
import os
import re

BASE = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

files_to_process = [
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_fiin.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin_extend.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin_extend.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin.md",
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_short_fiin.md",
    "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md",
    "chatbot_financial_statement/agent/prompt/vertical/base/simple_query_v2.txt",
    "chatbot_financial_statement/agent/prompt/vertical/universal/simple_query_v2.txt",
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql.txt",
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_simplify.txt",
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_short.txt",
    "chatbot_financial_statement/agent/prompt/general/branch_reasoning_text2sql.txt",
    "chatbot_financial_statement/agent/prompt/chat/summarize.txt",
]

replacements = [
    (r'Vietnamese', 'companies'),
    (r'Vietnam', ''),
    (r'vietnamese', 'companies'),
    (r'Vietnamese Accounting Standard \(VAS\)', 'applicable accounting standards'),
    (r'\bVAS\b', 'applicable accounting standards'),
    (r'Million VND', 'appropriate currency units'),
    (r'\bVND\b', 'currency units'),
    (r'Q3 2024', 'the most recent available period'),
    (r'\bHOSE\b', 'the applicable exchange'),
    (r'\bHNX\b', 'the applicable exchange'),
    (r'\bVN30\b', 'major stock indices'),
    (r'\bHNX30\b', 'major stock indices'),
]

def process_file(filepath):
    full_path = os.path.join(BASE, filepath)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        if content != original:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, filepath
        return False, filepath
    except Exception as e:
        return None, f"{filepath}: {e}"

print("开始批量修改提示词文件...")
print("="*60)
modified = 0
errors = []

for fp in files_to_process:
    result, msg = process_file(fp)
    if result is True:
        print(f"✅ Modified: {msg}")
        modified += 1
    elif result is False:
        print(f"⏭️  No change: {msg}")
    else:
        print(f"❌ Error: {msg}")
        errors.append(msg)

print("="*60)
print(f"\n完成！修改了 {modified} 个文件")
if errors:
    print(f"错误: {errors}")
