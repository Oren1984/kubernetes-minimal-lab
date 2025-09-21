# Dockerfile to build a minimal demo service for the Kubernetes lab
# Installs dependencies and starts a basic HTTP server/app

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8080
ENV PORT=8080
CMD ["python", "app.py"]
