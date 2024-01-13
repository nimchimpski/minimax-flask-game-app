from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'server, this is a test flask app with no templates'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)