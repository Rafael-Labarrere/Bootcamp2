FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
COPY src/ /app/src/
CMD ["python", "src/web.py"]