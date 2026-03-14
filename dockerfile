# syntax=docker/dockerfile:1.9-labs  # 启用高级特性，可选

# ------------------- Builder Stage -------------------
FROM python:3.12-slim-bookworm AS builder

# 安装 uv（官方镜像方式，最稳定）
COPY --from=ghcr.io/astral-sh/uv:0.5.4 /uv /usr/local/bin/uv

WORKDIR /

# 复制依赖文件，先缓存依赖层
COPY pyproject.toml uv.lock* requirements.txt* ./

# 安装依赖（生产模式，无 dev 依赖）
RUN uv venv /venv && \
    . /venv/bin/activate && \
    uv sync --frozen --no-dev --no-install-project

# 复制项目代码并安装项目本身
COPY . .
RUN . /venv/bin/activate && uv sync --frozen --no-dev

# ------------------- Production Stage -------------------
FROM python:3.12-slim-bookworm

# 创建非 root 用户（安全最佳实践）
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app
USER appuser

# 只复制 venv + 必要文件
COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 暴露端口
EXPOSE 8000

# 健康检查（生产必备）
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1   # 假设你有 /health 端点

# 生产启动（Gunicorn + Uvicorn，4 worker 示例，根据 CPU 调整）
CMD ["gunicorn", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "src.myapp.main:app"]