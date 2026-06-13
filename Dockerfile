FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令，监听 CloudRun 平台提供的 PORT 环境变量
CMD ["sh", "-c", "python -c \"from app import app; import os; app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))\""]
