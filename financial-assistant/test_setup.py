import os
import sys

def test_environment():
    print("=" * 60)
    print("环境测试")
    print("=" * 60)

    # 检查 .env 文件
    env_path = os.path.join(os.path.dirname(__file__), 'chatbot_financial_statement', '.env')
    if os.path.exists(env_path):
        print("✅ .env 文件存在")
    else:
        print("⚠️  .env 文件不存在")

    # 测试数据库连接
    print("\n测试数据库连接...")
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv(env_path)

        db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }
        if None not in db_config.values():
            conn = psycopg2.connect(**db_config)
            print("✅ 数据库连接成功!")
            conn.close()
        else:
            print("⚠️  数据库配置不完整")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")

    # 测试模块导入
    print("\n测试核心模块导入...")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chatbot_financial_statement'))

    try:
        from agent.text2sql import Text2SQL
        print("✅ Text2SQL 模块导入成功")
    except Exception as e:
        print(f"❌ Text2SQL 导入失败")

    try:
        from agent.chatbot import Chatbot
        print("✅ Chatbot 模块导入成功")
    except Exception as e:
        print(f"❌ Chatbot 导入失败")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_environment()
