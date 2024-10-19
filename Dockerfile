FROM python:3.12

WORKDIR /usr/src/gazpromik
COPY requirements.txt .
ENV PYTHONPATH="/usr/src/gazpromik"
RUN pip install -r requirements.txt

COPY . ./
CMD ["python3", "./start.py"]



