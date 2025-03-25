# Grab Python3.12 Lambda base image
FROM public.ecr.aws/lambda/python:3.12.2024.01.05.15

# Install required tools
RUN yum install -y git golang

# Clone and build Ddosify Engine
RUN git clone https://github.com/getanteon/anteon.git /tmp/anteon
WORKDIR /tmp/anteon/ddosify_engine
RUN go build -o ddosify_engine

# Move the binary to a location in PATH
RUN cp ddosify_engine /usr/local/bin/
RUN chmod +x /usr/local/bin/ddosify_engine

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler 
CMD [ "lambda_function.handler" ]