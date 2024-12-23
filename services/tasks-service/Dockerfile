FROM python:3.12.1-bullseye

RUN apt-get update && apt-get install -y inotify-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install watchdog

COPY . .

RUN pip install -e .

CMD ["./start.sh"]