FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:80", "aid_directory:app"]