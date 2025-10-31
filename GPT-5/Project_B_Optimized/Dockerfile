# Optimized environment Dockerfile (optional)
FROM python:3.12-slim
WORKDIR /app
COPY requirements_optimized.txt ./
RUN pip install --no-cache-dir -r requirements_optimized.txt || true
COPY . .
CMD ["bash", "run_optimized.sh"]
