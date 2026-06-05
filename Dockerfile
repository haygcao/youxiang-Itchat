FROM python:3.13-alpine

MAINTAINER Snow Wang <admin@farseer.vip>

WORKDIR /youxiang
COPY requirements.txt requirements.txt
COPY . /youxiang

ENV TZ=Asia/Shanghai
RUN apk add --no-cache tzdata zbar && \
    cp /usr/share/zoneinfo/$TZ /etc/localtime && echo "$TZ" > /etc/timezone && \
    pip install --no-cache-dir -r requirements.txt
    
ENTRYPOINT ["python", "/youxiang/main.py"]
