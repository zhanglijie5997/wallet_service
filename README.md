# wallet_service


# 生产模式（无热重载，默认监听 0.0.0.0:8000）
fastapi run main.py

# 指定端口 + 多 worker（推荐生产用法）
fastapi run main.py --port 8000 --workers 4

# 或者传统写法（仍然有效）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4