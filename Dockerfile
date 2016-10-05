FROM python:3-alpine
MAINTAINER Baard Johansen "baard.johansen@sesam.io"
COPY ./app /app
WORKDIR /app
# build deps required when installing sesamclient python bindings
RUN buildDeps='build-base openssl-dev libffi-dev' \
 && apk add --no-cache $buildDeps \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del $buildDeps
EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["todo-service.py"]