FROM python:3.12-slim

WORKDIR /app
COPY requirements_optimized.txt ./
RUN pip install --no-cache-dir -r requirements_optimized.txt
COPY . .
CMD ["/bin/bash", "run_optimized.sh"]
