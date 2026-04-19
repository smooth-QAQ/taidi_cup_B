"""
批量运行脚本 - 处理附件4问题并生成图表
运行方式: python batch_runner.py --input 附件4.xlsx
"""

import os
import sys
import json
import argparse
import pandas as pd
import logging
from pathlib import Path

# 添加项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DIR = os.path.join(BASE_DIR, 'chatbot_financial_statement')
sys.path.insert(0, CHAT_DIR)
sys.path.insert(0, BASE_DIR)
os.chdir(CHAT_DIR)

from agent import Text2SQL
from agent.const import Text2SQLConfig
from agent.prompt.prompt_controller import (
    PromptConfig,
    FIIN_VERTICAL_PROMPT_UNIVERSAL_OPENAI_EXTEND
)
from agent.chart_generator import generate_and_save_chart
from initialize import initialize_text2sql
from agent.const import TEXT2SQL_FAST_GEMINI_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_questions_from_xlsx(file_path: str) -> tuple[list[tuple[str, str]], bool]:
    """
    从Excel文件读取问题列表

    Args:
        file_path: Excel文件路径

    Returns:
        questions: [(问题编号, 问题文本), ...]
        has_id: 是否有问题编号
    """
    df = pd.read_excel(file_path, sheet_name=0)

    questions = []
    has_id = False

    # 检查是否有"问题编号"列
    if '问题编号' in df.columns:
        has_id = True
        # 遍历每一行
        for idx, row in df.iterrows():
            qid = str(row['问题编号']).strip()
            qtext = str(row.get('问题', row.iloc[0])).strip()
            if qtext and qtext != 'nan':
                questions.append((qid, qtext))
    else:
        # 使用第一列作为问题
        for idx, row in df.iterrows():
            qtext = str(row.iloc[0]).strip()
            if qtext and qtext != 'nan':
                questions.append((None, qtext))

    return questions, has_id


def read_questions_from_json(file_path: str) -> list[tuple[str, str]]:
    """
    从JSON文件读取问题列表（兼容 generated_questions_v*.json 格式）

    Args:
        file_path: JSON文件路径

    Returns:
        questions: [(None, 问题文本), ...] （JSON文件不包含编号）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    def extract_questions(obj):
        """递归提取所有 questions 字段"""
        if isinstance(obj, dict):
            if 'questions' in obj:
                # 找到 questions 字段
                for q in obj['questions']:
                    if isinstance(q, str):
                        questions.append((None, q))
                    elif isinstance(q, dict) and 'question' in q:
                        questions.append((None, q['question']))
            # 继续递归
            for v in obj.values():
                extract_questions(v)
        elif isinstance(obj, list):
            for item in obj:
                extract_questions(item)

    extract_questions(data)
    return questions


def read_questions(file_path: str) -> list[tuple[str, str]]:
    """
    根据文件扩展名读取问题

    Args:
        file_path: 文件路径

    Returns:
        questions: [(问题编号或None, 问题文本), ...]
    """
    ext = Path(file_path).suffix.lower()

    if ext in ['.xlsx', '.xls']:
        questions, _ = read_questions_from_xlsx(file_path)
    elif ext == '.json':
        questions = read_questions_from_json(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return questions


def initialize_chatbot() -> Text2SQL:
    """
    初始化Text2SQL实例

    Returns:
        text2sql: Text2SQL实例
    """
    prompt_config = FIIN_VERTICAL_PROMPT_UNIVERSAL_OPENAI_EXTEND
    text2sql_config = TEXT2SQL_FAST_GEMINI_CONFIG

    text2sql = initialize_text2sql(
        text2sql_config,
        prompt_config,
        version='v3.2',
        message=False
    )

    return text2sql


def process_single_question(
    text2sql: Text2SQL,
    qid: str,
    question: str,
    index: int,
    result_dir: str
) -> dict:
    """
    处理单个问题

    Args:
        text2sql: Text2SQL实例
        qid: 问题编号
        question: 问题文本
        index: 题目序号
        result_dir: 结果保存目录

    Returns:
        result: 包含问题编号、问题、SQL、回答、图表路径的字典
    """
    result = {
        '问题编号': qid if qid else f'B{index:03d}',
        '问题': question,
        '生成SQL': '',
        '回答': '',
        '图表路径': ''
    }

    try:
        # 调用Text2SQL
        output = text2sql.solve(question)

        # 提取SQL
        if output.sql:
            result['生成SQL'] = '; '.join(output.sql)

        # 提取回答（从history中获取assistant的回复）
        if output.history:
            for msg in reversed(output.history):
                if msg.get('role') == 'assistant':
                    result['回答'] = msg.get('content', '')[:500]  # 截取前500字符
                    break

        # 提取第一个Table的DataFrame并生成图表
        if output.execution_tables:
            first_table = output.execution_tables[0]
            if hasattr(first_table, 'table') and first_table.table is not None:
                df = first_table.table

                # 生成图表路径
                chart_id = qid if qid else f'B{index:03d}'
                chart_path = os.path.join(result_dir, f'{chart_id}_{index}.jpg')

                # 生成并保存图表
                saved_path = generate_and_save_chart(df, question, chart_path)
                result['图表路径'] = saved_path

    except Exception as e:
        logger.error(f"处理问题 {qid} 时出错: {str(e)}")
        result['生成SQL'] = f"Error: {str(e)}"
        result['回答'] = f"处理失败: {str(e)}"

    return result


def main():
    parser = argparse.ArgumentParser(description='批量处理附件4问题并生成图表')
    parser.add_argument('--input', required=True, help='输入文件路径（支持.xlsx和.json）')
    parser.add_argument('--output', default='result_2.xlsx', help='输出Excel文件路径（默认：result_2.xlsx）')
    parser.add_argument('--result-dir', default='result', help='图表保存目录（默认：result）')
    parser.add_argument('--start', type=int, default=1, help='起始题目编号（默认：1）')

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    # 创建结果目录
    os.makedirs(args.result_dir, exist_ok=True)

    # 读取问题列表
    print(f"\n正在读取问题文件: {args.input}")
    questions = read_questions(args.input)
    total = len(questions)

    if total == 0:
        print("错误: 未找到任何问题")
        sys.exit(1)

    print(f"共找到 {total} 个问题\n")

    # 初始化Chatbot
    print("正在初始化Text2SQL...")
    text2sql = initialize_chatbot()
    print("初始化完成\n")

    # 存储结果
    results = []

    # 处理每个���题
    for idx, (qid, question) in enumerate(questions, start=args.start):
        # 显示进度
        display_id = qid if qid else f'B{idx:03d}'
        question_preview = question[:30] + '...' if len(question) > 30 else question
        print(f"[{idx}/{total}] 处理中: {display_id} - {question_preview}")

        result = process_single_question(
            text2sql,
            qid,
            question,
            idx,
            args.result_dir
        )
        results.append(result)

        # 每处理5个问题打印一次统计
        if idx % 5 == 0:
            print(f"  已完成: {idx}/{total} ({(idx/total)*100:.1f}%)")

    # 保存结果到Excel
    df_results = pd.DataFrame(results)

    # 确保列顺序
    columns = ['问题编号', '问题', '生成SQL', '回答', '图表路径']
    df_results = df_results[columns]

    df_results.to_excel(args.output, index=False, engine='openpyxl')

    print(f"\n处理完成！")
    print(f"结果已保存到: {args.output}")
    print(f"图表保存在: {args.result_dir}/")


if __name__ == '__main__':
    main()
