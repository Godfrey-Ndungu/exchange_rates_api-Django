FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install OpenTelemetry instrumentation libraries
RUN opentelemetry-bootstrap -a install

COPY . .

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=peachapi.production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
COPY entry_point.sh /entry_point.sh
RUN chmod +x /entry_point.sh
ENTRYPOINT ["/entry_point.sh"]
