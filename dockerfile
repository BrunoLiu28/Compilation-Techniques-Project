FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip llvm


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tokens.py /app/tokens.py
COPY rules.py /app/rules.py
COPY semantic.py /app/semantic.py
COPY codeGen.py /app/codeGen.py
COPY plush_compiler.py /app/plush_compiler.py
COPY test.pl /app/test.pl
COPY functions.c /app/functions.c

RUN python3 plush_compiler.py test.pl
RUN llc test.ll
RUN gcc -c test.s
RUN gcc -c functions.c
RUN gcc -no-pie -fno-PIE test.o functions.o
RUN ./a.out
CMD ["python3", "plush_compiler.py", "test.pl"]
