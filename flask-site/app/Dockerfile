FROM python:3.8-slim 
COPY requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python3", "app.py"]
