FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY nhris_adk_agent /app/nhris_adk_agent
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000", "/app"]
