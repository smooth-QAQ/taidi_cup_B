"""
修改提示词文件的独立脚本
"""

import re
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

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

# 替换规则列表
replacements = [
    (r'Vietnamese?', 'companies'),
    (r'Vietnam', ''),
    (r'Vietnamese Accounting Standard \(VAS\)', 'applicable accounting standards'),
    (r'\bVAS\b', 'applicable accounting standards'),
    (r'Million VND', 'appropriate currency units'),
    (r'\bVND\b', 'currency units'),
    (r'Q3 2024', 'the most recent available period'),
    (r'\bHOSE\b', 'the applicable exchange'),
    (r'\bHNX\b', 'the applicable exchange'),
    (r'\bVN30\b', 'major stock indices'),
    (r'\bHNX30\b', 'major stock indices'),
    (r'assistance', 'assistant'),
    (r'cooperates', 'corporations'),
]

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        changes = []

        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                changes.append(pattern)
                content = new_content

        # 清理多余空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Modified: {filepath} (changes: {', '.join(changes)})")
            return True
        else:
            print(f"⏭️  No change: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Error: {filepath} - {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Working dir: {base_dir}\n")
    print("="*60)

    modified = 0
    for rel_path in files_to_process:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            if process_file(full_path):
                modified += 1
        else:
            print(f"⚠️  Not found: {rel_path}")

    print("="*60)
    print(f"\n✅ Done! Modified {modified} files.")

if __name__ == '__main__':
    main()
