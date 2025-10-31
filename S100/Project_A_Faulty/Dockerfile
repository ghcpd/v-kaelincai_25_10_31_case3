FROM python:3.8-slim

WORKDIR /app
COPY requirements_original.txt ./
RUN pip install --no-cache-dir -r requirements_original.txt
COPY . .
CMD ["/bin/bash", "run_original.sh"]
