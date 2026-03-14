# wallet_service


# 开发时（带 --reload 热更新）
uvicorn main:app --reload

# 或者更详细一点
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 生产环境（去掉 --reload，建议加 workers）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4