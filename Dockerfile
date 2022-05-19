FROM python:3.9

WORKDIR /app

COPY api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python3.9", "user_profile_app.py", "--config_file", "api/config/backend-prod.yaml"]
