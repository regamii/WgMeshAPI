FROM python:3.10.0a7-buster

WORKDIR /usr/share/app

COPY src .

RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh .
ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "--threads", "2", "run:app"]
