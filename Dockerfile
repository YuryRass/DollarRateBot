FROM python:3.11.5

RUN mkdir /dollar_rate_bot

WORKDIR /dollar_rate_bot

ADD requirements.txt /dollar_rate_bot/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /dollar_rate_bot
