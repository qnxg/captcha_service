FROM python:3.14.0rc3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr
COPY . .
EXPOSE 5000
# workers 建议是 CPU 核心数 * 2 + 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "15", "main:app"]