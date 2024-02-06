FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m ensurepip --upgrade
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "bot.py" ]