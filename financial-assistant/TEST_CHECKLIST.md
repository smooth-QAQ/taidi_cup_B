# 金融问答助手 - 测试清单

## ✅ 第一步：环境准备

### 1.1 创建 .env 配置文件
在 `chatbot_financial_statement/` 目录创建 `.env` 文件：

```bash
cd chatbot_financial_statement
cp .env.example .env
# 编辑 .env 填入实际值
```

**必需配置：**
- [ ] `OPENAI_API_KEY` - OpenAI API 密钥
- [ ] `DB_NAME` - 数据库名
- [ ] `DB_USER` - 数据库用户名
- [ ] `DB_PASSWORD` - 数据库密码
- [ ] `DB_HOST` - 数据库地址 (默认 localhost)
- [ ] `DB_PORT` - 数据库端口 (默认 5432)

### 1.2 安装依赖
```bash
pip install -r requirements.txt
```

## ✅ 第二步：数据库测试

### 2.1 检查 PostgreSQL 服务
```bash
# Windows
net start | findstr postgres

# 或检查服务
sc query postgresql*
```

### 2.2 创建数据库
```sql
CREATE DATABASE financial_db;
```

### 2.3 运行连接测试
```bash
python test_db_connection.py
```

**预期输出：**
- ✅ 数据库连接成功
- ✅ 表列表显示

## ✅ 第三步：初始化数据

### 3.1 检查数据文件
确认以下目录存在：
```
chatbot_financial_statement/
├── csv/              # 包含 v2/, v3/ 等子目录
├── data/             # 初始化后生成
└── graphics/         # 图标文件
```

### 3.2 运行数据初始化
```bash
# 方式1: 使用本地嵌入模型（推荐）
python setup.py --preprocess v3.2 --local True --force True

# 方式2: 使用 OpenAI 嵌入
python setup.py --preprocess v3.2 --openai True --force True
```

**注意：** 首次运行可能需要较长时间（10-30分钟），取决于数据量。

## ✅ 第四步：验证向量数据库

### 4.1 检查 ChromaDB 是否生成
```bash
ls data/vector_db_*
```

应该看到类似：
- `vector_db_vertical_local_v3.2/`
- `vector_db_vertical_openai_v3.2/`

## ✅ 第五步：测试核心功能

### 5.1 简单导入测试
```bash
python -c "
import sys
sys.path.insert(0, 'chatbot_financial_statement')
from agent.text2sql import Text2SQL
print('✅ Text2SQL 模块正常')
"
```

### 5.2 测试初始化
```bash
python -c "
import sys
sys.path.insert(0, 'chatbot_financial_statement')
from initialize import initialize_text2sql
# 需要配置完整，可能需要实际数据库
"
```

## ✅ 第六步：启动 Streamlit 界面

### 6.1 启动应用
```bash
cd chatbot_financial_statement
streamlit run home.py
```

### 6.2 测试页面导航
- [ ] 主页正常显示
- [ ] Chat 页面可输入问题
- [ ] Text2SQL 页面可调试 SQL
- [ ] Reasoning 页面显示推理过程

### 6.3 测试查询功能
尝试以下示例问题：
- "What is the revenue of the company VIC?"
- "What is the CASA of banking industry from 2016 to 2023?"
- "Top 5 bank with the highest Bad Debt Ratio in Q3 2024?"

## ❌ 常见问题排查

### 问题1: ModuleNotFoundError
**解决:** 确保在正确目录运行，或添加路径
```bash
cd chatbot_financial_statement
python -m streamlit run home.py
```

### 问题2: 数据库连接失败
**检查清单：**
- [ ] PostgreSQL 服务已启动
- [ ] 数据库 `financial_db` 已创建
- [ ] 用户名密码正确
- [ ] 防火墙允许 5432 端口

### 问题3: 向量数据库未找到
**解决:** 重新运行 setup.py 初始化

### 问题4: OpenAI API 错误
**检查：**
- [ ] API Key 正确
- [ ] 账户有足够额度
- [ ] 网络连接正常

## 📊 第七步：功能验证清单

### 核心功能
- [ ] 自然语言问题识别
- [ ] 公司代码提取
- [ ] SQL 生成
- [ ] SQL 执行
- [ ] 结果展示

### 高级功能
- [ ] 自我调试（Self-Debug）
- [ ] 自我纠正（Self-Correction）
- [ ] 自我反思（Self-Reflection）

### 聊天功能
- [ ] 对话历史保存
- [ ] 上下文理解
- [ ] 多轮对话

## 📈 性能优化建议

1. **向量检索优化**
   - 调整 `top_k` 参数
   - 启用重排序（Reranker）

2. **SQL 生成优化**
   - 使用 Few-Shot 示例
   - 调整 temperature 参数

3. **缓存策略**
   - 启用结果缓存
   - 复用会话状态

## 📝 日志检查

查看应用日志：
```bash
tail -f ~/.streamlit/logs/streamlit.log
```

或在代码中添加调试：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 下一步

完成所有测试后：
1. 整理测试结果
2. 修复发现的问题
3. 优化性能和用户体验
4. 准备部署文档

---

**最后更新：** 请根据实际测试结果填写检查项
