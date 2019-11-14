FROM sanicframework/sanic:LTS

COPY ./app /srv

RUN ulimit -n > /tmp/ulimit.txt

EXPOSE 8888

CMD ["python", "/srv/main.py"]