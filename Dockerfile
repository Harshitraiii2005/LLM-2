FROM python:3.10-slim

WORKDIR /app

COPY src/ /app/src/
COPY Dataset /app/Dataset
COPY flow.py /app/
COPY app.py /app/
COPY requirements.txt /app/
COPY start_services.sh /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5090
EXPOSE 4200
EXPOSE 9070

CMD ["bash", "start_services.sh"]
