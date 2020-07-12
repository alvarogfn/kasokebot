from os import environ
from Flask import Flask

app = Flask(__name__)
app.run(host= '0.0.0.0', port=environ.get('PORT'))
