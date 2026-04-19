"""
批量修改提示词文件 - 去除越南特定内容
直接在当前Python环境中执行
"""
import os
import re

BASE_DIR = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

# 文件映射：(相对路径, 需要进行的替换操作列表)
file_replacements = {
    # seek_database_fiin.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_fiin.md": [
        ("Vietnamese companies, either bank, cooperates and securities", "companies, including banks, corporations, and securities firms"),
        ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
        ("based on VAS regulation", "based on regulatory classifications"),
        ("in Million VND", "in appropriate currency units"),
    ],
    # seek_database_simplify_fiin.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md": [
        ("top Vietnamese firms", "companies"),
        ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
        ("based on VAS regulation", "based on regulatory classifications"),
    ],
    # seek_database_simplify_fiin_extend.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin_extend.md": [
        ("Vietnamese", "companies"),
        ("Vietnamese Accounting Standard (VAS)", "applicable accounting standards"),
        ("VAS", "applicable accounting standards"),
    ],
    # openai_seek_database_simplify_fiin_extend.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin_extend.md": [
        ("Vietnamese companies", "companies"),
        ("Vietnamese Accounting Standard", "applicable accounting standards"),
        ("VAS", "applicable accounting standards"),
        ("Million VND", "appropriate units"),
    ],
    # openai_seek_database_simplify_fiin.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_simplify_fiin.md": [
        ("Vietnamese", "companies"),
        ("VAS", "applicable standards"),
        ("VND", "currency units"),
    ],
    # openai_seek_database_short_fiin.md
    "chatbot_financial_statement/agent/prompt/vertical/universal/openai_seek_database_short_fiin.md": [
        ("Vietnamese companies", "companies"),
        ("Vietnamese Accounting Standard", "applicable accounting standards"),
        ("Million VND", "units"),
    ],
    # base/seek_database.md
    "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md": [
        ("Vietnamese companies", "companies"),
        ("VAS", "applicable accounting standards"),
        ("Million VND", "currency units"),
        ("HOSE", "the primary exchange"),
        ("HNX", "secondary exchanges"),
        ("VN30", "major indices"),
        ("HNX30", "major indices"),
    ],
    # universal/simple_query_v2.txt
    "chatbot_financial_statement/agent/prompt/vertical/universal/simple_query_v2.txt": [
        ("Vietnamese", "companies"),
        ("VAS", "applicable standards"),
    ],
    # base/simple_query_v2.txt
    "chatbot_financial_statement/agent/prompt/vertical/base/simple_query_v2.txt": [
        ("Vietnamese", "companies"),
    ],
    # general/reasoning_text2sql.txt
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql.txt": [
        ("Vietnamese", "companies"),
        ("VAS", "applicable accounting standards"),
    ],
    # general/reasoning_text2sql_simplify.txt
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_simplify.txt": [
        ("Vietnamese", "companies"),
        ("VAS", "applicable accounting standards"),
    ],
    # general/reasoning_text2sql_short.txt
    "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql_short.txt": [
        ("Vietnamese", "companies"),
    ],
    # general/branch_reasoning_text2sql.txt
    "chatbot_financial_statement/agent/prompt/general/branch_reasoning_text2sql.txt": [
        ("Vietnamese", "companies"),
        ("VAS", "applicable accounting standards"),
    ],
    # chat/summarize.txt
    "chatbot_financial_statement/agent/prompt/chat/summarize.txt": [
        ("Vietnamese", "companies"),
        ("Million VND", "currency units"),
    ],
}

def modify_file(rel_path, changes):
    """修改单个文件"""
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(full_path):
        print(f"⚠️  Not found: {rel_path}")
        return False

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for old, new in changes:
            content = content.replace(old, new)

        # 额外处理一些正则表达式模式
        content = re.sub(r'\bVietnamese\b', 'companies', content, flags=re.IGNORECASE)
        content = re.sub(r'\bMillion VND\b', 'appropriate currency units', content, flags=re.IGNORECASE)
        content = re.sub(r'\bQ3 2024\b', 'the most recent period', content)
        content = re.sub(r'\bVND\b', 'currency units', content, flags=re.IGNORECASE)

        # 清理多余空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {rel_path}: {e}")
        return None

print("开始批量修改提示词文件...")
print("="*60)

modified = 0
unchanged = 0
errors = []

for rel_path, changes in file_replacements.items():
    result = modify_file(rel_path, changes)
    if result is True:
        print(f"✅ Modified: {rel_path}")
        modified += 1
    elif result is False:
        print(f"⏭️  No change: {rel_path}")
        unchanged += 1
    else:
        errors.append(rel_path)

print("="*60)
print(f"\n✅ Complete! Modified: {modified}, Unchanged: {unchanged}")
if errors:
    print(f"Errors: {errors}")
