FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# 2. Ishchi papkani yaratish
WORKDIR /app

# 4. Loyihaning talablarini o‘rnatish
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
