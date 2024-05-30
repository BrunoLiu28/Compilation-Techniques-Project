FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY tokens.py /app/tokens.py
COPY rules.py /app/rules.py
COPY semantic.py /app/semantic.py
COPY codeGen.py /app/codeGen.py
COPY plush_parser.py /app/plush_parser.py


CMD ["python", "plush_parser.py", "test.pl"]
