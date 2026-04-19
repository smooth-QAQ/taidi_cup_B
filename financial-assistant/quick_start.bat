#!/bin/bash
# 快速启动脚本 - 用于测试附件4任务

echo "=== 快速启动财务问答系统 ==="

# 1. 检查Docker
echo "检查Docker容器..."
docker-compose up -d
sleep 5

# 2. 激活环境
echo "激活Python环境..."
conda activate text2sql 2>nul || python -m venv venv && venv\Scripts\activate

# 3. 安装依赖
echo "安装依赖..."
pip install -r requirements.txt -q

# 4. 初始化数据库（如果尚未初始化）
if [ ! -d "chatbot_financial_statement/ETL/chroma_db" ]; then
    echo "初始化数据库..."
    python setup.py --preprocess v3.2 --force True --local True --vectordb chromadb
else
    echo "数据库已存在，跳过初始化"
fi

# 5. 运行测试
echo "运行环境测试..."
python test.py

# 6. 启动应用
echo "启动Streamlit应用..."
streamlit run home.py
