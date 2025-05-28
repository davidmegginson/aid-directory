import os

from flask import Flask

app = Flask(__name__)

app.config['MYSQL_DATABASE'] = os.environ['MYSQL_DATABASE']
app.config['MYSQL_USERNAME'] = os.environ['MYSQL_USERNAME']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']

from aid_directory import handlers
