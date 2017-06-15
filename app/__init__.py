import os
import logging
from json import dumps
from flask import Flask, render_template, request, redirect, url_for

import sqs

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
BOTO_QUEUE_NAME_LAT_LNG = 'lat_lng_queue'


def send_message(queue, data):
    queue.send_message(MessageBody=data)


def get_data(result):
    start_lat = float(result.get('start_lat'))
    start_lng = float(result.get('start_lng'))
    end_lat = float(result.get('end_lat'))
    end_lng = float(result.get('end_lng'))
    data = {
        'start_lat': start_lat,
        'start_lng': start_lng,
        'end_lat': end_lat,
        'end_lng': end_lng
    }
    return data


@app.route('/')
def index():
    return render_template("map.html", GOOGLE_API_KEY=GOOGLE_API_KEY)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.method == 'POST':
        result = request.form
        data = get_data(result)
        send_message(lat_lng_queue, dumps(data))
        return redirect(url_for('index'))
    return render_template('error.html')


if __name__ == '__main__':
    logging.basicConfig(level=20, format='%(asctime)s:{}'.format(logging.BASIC_FORMAT))
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    lat_lng_queue = sqs.get_queue('lat_lng_queue')
    try:
        app.run(debug=False)
    except Exception as e:
        logging.exception(e)
        raise
