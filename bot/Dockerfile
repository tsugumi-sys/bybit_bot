FROM python:3.9-slim

WORKDIR /app

ADD requirements.txt /app/

RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY .env /app/.env
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
CMD ["./run.sh"]