FROM python

COPY pytraefik.py /usr/lib

CMD ["python /usr/lib/pytraefik.py"]
