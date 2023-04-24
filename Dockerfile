FROM ubuntu:jammy
RUN apt update ; apt install -y python3.11 python3-pip
RUN python3.11 -m pip --version

ENV PATH="./result/bin/:$PATH"

COPY requirements.txt app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

COPY app app

COPY app/tests/test_main app/tests/test_main

COPY app/tests app/tests
