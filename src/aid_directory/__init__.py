import os

from flask import Flask

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'db')
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE', 'aid_directory')
app.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT', '3306')
app.config['MYSQL_USERNAME'] = os.environ['MYSQL_USERNAME']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']

from aid_directory import handlers
