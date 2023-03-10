FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV FLASK_APP 'dongnae'

ENTRYPOINT ["flask"]

CMD ["run", "--host", "0.0.0.0", "--port", "5050"]

