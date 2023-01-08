FROM python:3.10.8

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/tg_bot


COPY . /usr/src/app/tg_bot/
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

CMD ["python", "bot.py"]