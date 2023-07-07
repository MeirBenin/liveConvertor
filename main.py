from flask import Flask, Response, request

import subprocess


app = Flask(__name__)

@app.route('/')
def convert_stream_to_mp3():
    """convert m3u8 stream to mp3"""
    url = request.args.get('url','')
    def generate():
       print(url)
       with subprocess.Popen(['ffmpeg', '-i', url, '-f', 'mp3', '-'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
           while True:
                data = process.stdout.read(1024)
                if not data:
                    break
                yield data

    response = Response(generate(), mimetype='audio/mp3')
    response.headers.set('Cache-Control', 'no-cache')
    response.headers.set('Connection', 'keep-alive')
    return response


if __name__ == '__main__':
    app.run("0.0.0.0",port=5554)
