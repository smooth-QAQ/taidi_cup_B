"""
测试数据库连接和核心模块
"""
import psycopg2
import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("1. 环境变量检查")
print("=" * 60)

required_vars = ['OPENAI_API_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: 未设置")

print("\n" + "=" * 60)
print("2. 数据库连接测试")
print("=" * 60)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

# 检查是否有None值
none_vars = [k for k, v in db_config.items() if v is None]
if none_vars:
    print(f"⚠️  以下数据库配置项为None: {none_vars}")
    print("请检查 .env 文件配置")
else:
    try:
        conn = psycopg2.connect(**db_config)
        print("✅ 数据库连接成功!")

        # 检查现有表
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cur.fetchall()
            print(f"\n📋 数据库中的表 ({len(tables)}个):")
            for table in tables:
                print(f"  - {table[0]}")

        conn.close()
        print("\n✅ 数据库测试完成!")

    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n请确保:")
        print("1. PostgreSQL 服务正在运行")
        print("2. 数据库已创建")
        print("3. 用户名和密码正确")

print("\n" + "=" * 60)
print("3. 核心模块导入测试")
print("=" * 60)

try:
    sys.path.append('chatbot_financial_statement')
    from agent.text2sql import Text2SQL
    print("✅ Text2SQL 模块导入成功")
except Exception as e:
    print(f"❌ Text2SQL 导入失败: {e}")

try:
    from agent.chatbot import Chatbot
    print("✅ Chatbot 模块导入成功")
except Exception as e:
    print(f"❌ Chatbot 导入失败: {e}")

try:
    from ETL.dbmanager import HubVerticalUniversal
    print("✅ DBManager 模块导入成功")
except Exception as e:
    print(f"❌ DBManager 导入失败: {e}")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
