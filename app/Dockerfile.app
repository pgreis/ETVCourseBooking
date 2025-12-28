FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

RUN mkdir -p /app/src/utils
COPY src/utils/db /app/src/utils/db

RUN mkdir -p /app/logger
COPY logger /app/logger

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8501
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Start Streamlit
CMD ["python", "-m", "streamlit", "run", "sl_course_table.py"]