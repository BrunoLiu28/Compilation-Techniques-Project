FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip llvm gcc

# Install the required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /plush

# For the compiler
COPY tokens.py /plush/tokens.py
COPY rules.py /plush/rules.py
COPY semantic.py /plush/semantic.py
COPY codeGen.py /plush/codeGen.py
COPY plush_compiler.py /plush/plush_compiler.py

# For testing and running the program
# COPY test.pl /plush/test.pl
COPY functions.c /plush/functions.c
COPY plush.sh /plush/plush.sh
COPY runProgram.sh /plush/runProgram.sh
COPY /maxRangeSquared/ /plush/maxRangeSquared/
COPY /bubbleSort/ /plush/bubbleSort/
COPY /fibonacci/ /plush/fibonacci/
COPY /leapYear/ /plush/leapYear/
COPY /exampleForImports/ /plush/exampleForImports/


# CMD ["python3", "plush_compiler.py", "test.pl"]
