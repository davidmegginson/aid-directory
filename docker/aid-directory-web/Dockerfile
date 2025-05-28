FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#CMD ["gunicorn", "--workers", "3", "--threads", "3", "aid_directory:app"]
CMD ["flask", "--app=aid_directory:app", "run", "--host=0.0.0.0", "--port=80", "--reload"]