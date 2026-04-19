"""
批量处理所有包含越南词汇的提示词文件
直接在Python中执行，避免Shell问题
"""
import re
import os

base_dir = r'c:\cursor_Xiangmu\taidi_cup_B\financial-assistant'

# 文件列表和它们的特定修改
files_to_modify = [
    # (相对路径, 替换规则列表)
    (
        "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_fiin.md",
        [
            (r'Vietnamese companies, either bank, cooperates and securities', 'companies, including banks, corporations, and securities firms'),
            (r'Vietnamese Accounting Standard \(VAS\)', 'applicable accounting standards'),
            (r'based on VAS regulation', 'based on regulatory classifications'),
            (r'in Million VND', 'in appropriate currency units'),
            (r'\bHOSE\b', 'the applicable exchange'),
            (r'\bHNX\b', 'the applicable exchange'),
            (r'\bVN30\b', 'major stock indices'),
            (r'\bHNX30\b', 'major stock indices'),
        ]
    ),
    (
        "chatbot_financial_statement/agent/prompt/vertical/universal/seek_database_simplify_fiin.md",
        [
            (r'top Vietnamese firms', 'companies'),
            (r'Vietnamese Accounting Standard \(VAS\)', 'applicable accounting standards'),
            (r'based on VAS regulation', 'based on regulatory classifications'),
            (r'\bHOSE\b', 'applicable exchange'),
        ]
    ),
    (
        "chatbot_financial_statement/agent/prompt/vertical/base/seek_database.md",
        [
            (r'Vietnamese companies', 'companies'),
            (r'Vietnamese Accounting Standard', 'applicable accounting standards'),
            (r'\bVAS\b', 'applicable accounting standards'),
            (r'Million VND', 'currency units'),
            (r'HOSE', 'primary exchange'),
            (r'HNX', 'secondary exchange'),
        ]
    ),
    (
        "chatbot_financial_statement/agent/prompt/general/reasoning_text2sql.txt",
        [
            (r'Vietnamese', 'companies'),
            (r'Vietnamese Accounting Standard', 'applicable accounting standards'),
            (r'\bVAS\b', 'applicable accounting standards'),
        ]
    ),
    # 添加所有需要处理的文件...
]

print("批量处理提示词文件...")
print("="*60)

modified = 0
for rel_path, replacements in files_to_modify:
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"⚠️  Not found: {rel_path}")
        continue

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content

        for old, new in replacements:
            content = re.sub(old, new, content, flags=re.IGNORECASE)

        # 清理多余空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Modified: {rel_path}")
            modified += 1
        else:
            print(f"⏭️  No change: {rel_path}")
    except Exception as e:
        print(f"❌ Error: {rel_path}: {e}")

print("="*60)
print(f"完成！修改了 {modified} 个文件")
