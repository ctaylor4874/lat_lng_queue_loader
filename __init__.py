import os
from flask import Flask, render_template, request

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

@app.route('/')
def index():
    return render_template("map.html", GOOGLE_API_KEY=GOOGLE_API_KEY)


# @app.route('/send_data', methods=['POST'])
# def send_data():
#     points = request.args('points')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
