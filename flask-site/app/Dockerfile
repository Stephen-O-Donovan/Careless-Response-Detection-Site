FROM python:3.8-slim 
USER root
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80
ENV NAME World
CMD ["python3", "app.py"]
