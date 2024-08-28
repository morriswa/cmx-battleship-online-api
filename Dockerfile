
#
# AUTHOR: William A. Morris
# CREATION_DATE: 2024-08-28
# PURPOSE:
#   create Docker Container from generated application artifacts
#

# Container will be run on x86-64 Linux Platform
# Pull python 3.12
FROM --platform=x86-64 python:3.12-alpine

# ENV SYS_VAR=default_value

# create and move to directory /app to store artifacts
WORKDIR /app

# copy into /app folder
COPY . .
RUN pip install awscli
RUN --mount=type=secret,id=AWS_ID \
    --mount=type=secret,id=AWS_SECRET \
    --mount=type=secret,id=AWS_REGION \
    aws configure set aws_access_key_id $(cat /run/secrets/AWS_ID) && \
    aws configure set aws_secret_access_key $(cat /run/secrets/AWS_SECRET) && \
    aws configure set default.region $(cat /run/secrets/AWS_REGION) && \
    aws codeartifact login --tool pip --domain morriswa-org --repository morriswa-central
RUN pip install .

# set entrypoint (command which will run when container is started)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--chdir", "/app", "app.wsgi"]

# expose appropriate API port
EXPOSE 8000
