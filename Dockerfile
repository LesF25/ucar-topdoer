FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY conf /app/conf
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r conf/requirements.txt -c conf/constraints.txt

COPY . /app/

RUN chmod +x /app/scripts/start.sh

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["/app/scripts/start.sh"]
