FROM almalinux:8
COPY ./backend /app/backend
COPY ./web /app/web

RUN curl -sL https://rpm.nodesource.com/setup_14.x | bash - && \
    yum install -y python38 nodejs && \
    cd /app/backend && \
    python3.8 -m venv venv && \
    source venv/bin/activate && \
    python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install -r requirements.txt && \
    cd /app/web && \
    npm install @vue/cli && \
    npx vue-cli-service build

CMD /bin/sh -c "cd /app/backend && source venv/bin/activate && python3.8 server.py"

