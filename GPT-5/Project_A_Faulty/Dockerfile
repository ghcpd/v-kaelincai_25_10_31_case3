# Faulty environment Dockerfile (optional)
FROM python:3.12-slim
WORKDIR /app
COPY requirements_original.txt ./
RUN pip install --no-cache-dir -r requirements_original.txt || true
COPY . .
CMD ["bash", "run_original.sh"]
