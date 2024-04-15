FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

COPY ./email_sender.py ${LAMBDA_TASK_ROOT}
COPY ./transaction_processor.py ${LAMBDA_TASK_ROOT}
COPY ./main.py ${LAMBDA_TASK_ROOT}
COPY ./stori_logo.jpg ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]