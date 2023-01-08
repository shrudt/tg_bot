FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/bot_analytic

COPY . /usr/src/app/bot_analytic
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"

EXPOSE 5000

CMD ["python", "main.py"]