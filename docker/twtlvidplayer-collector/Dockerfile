FROM centos:8
COPY ./backend /app/backend
COPY ./docker/twtlvidplayer-collector/docker-entrypoint.sh /app/backend

RUN yum install -y python38 && \
    cd /app/backend && \
    python3.8 -m venv venv && \
    source venv/bin/activate && \
    python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install -r requirements.txt

CMD /bin/bash /app/backend/docker-entrypoint.sh

