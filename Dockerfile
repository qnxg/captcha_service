FROM debian:trixie-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .

RUN uv python install
RUN uv sync --frozen --no-dev --no-install-project
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr

EXPOSE 5000
# workers 建议是 CPU 核心数 * 2 + 1
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "15", "main:app"]