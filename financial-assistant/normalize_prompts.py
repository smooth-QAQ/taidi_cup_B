"""
批量去除越南特定词汇，将提示词通用化
"""
import os
import re

# 需要处理的文件列表
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

# 替换规则：每行是 (旧字符串, 新字符串)
replacements = [
    # 越南特定词汇
    (r'Vietnamese', 'companies'),
    (r'Vietnam', ''),  # 直接移除
    (r'vietnamese', 'companies'),

    # 会计标准
    (r'Vietnamese Accounting Standard \(VAS\)', 'applicable accounting standards'),
    (r'VAS', 'applicable accounting standards'),

    # 货币单位
    (r'Million VND', 'appropriate currency units'),
    (r'VND', 'currency units'),
    (r'1 Million VND', 'the standard currency unit'),

    # 时间参考
    (r'Q3 2024', 'the most recent available period'),
    (r'2024', 'the most recent year'),

    # 交易所和指数（去掉具体名称）
    (r'HOSE', 'the applicable exchange'),
    (r'HNX', 'the applicable exchange'),
    (r'VN30', 'major stock indices'),
    (r'HNX30', 'major stock indices'),

    # 特定公司名
    (r'BIDV|Vietcombank|VietinBank|Techcombank|VPBank|Eximbank', 'banks'),
    (r'VinGroup|Vingroup|VIC', 'companies'),

    # 语法修正
    (r'assistance', 'assistant'),
    (r'cooperates', 'corporations'),
]

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 应用所有替换规则
        for old, new in replacements:
            content = re.sub(old, new, content, flags=re.IGNORECASE)

        # 清理多余的空白
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Modified: {filepath}")
            return True
        else:
            print(f"⏭️  No change needed: {filepath}")
            return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Working directory: {base_dir}\n")

    modified_count = 0
    for rel_path in files_to_process:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            if process_file(full_path):
                modified_count += 1
        else:
            print(f"⚠️  File not found: {full_path}")

    print(f"\n✅ Completed! Modified {modified_count} files.")

if __name__ == '__main__':
    main()
