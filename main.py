from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def stream():
    """Video streaming route. Put this in the src attribute of an img tag."""
    url = 'https://kan11.media.kan.org.il/hls/live/2024514/2024514/source1_4k/chunklist.m3u8'

    ffmpeg_process = subprocess.Popen(['ffmpeg', '-i', url, '-f', 'mp3', 'pipe:1'], stdout=subprocess.PIPE)

    def generate():
        # Read the output from FFmpeg process and yield it to the client
        while True:
            data = ffmpeg_process.stdout.read(1024)
            if not data:
                print('breaking')
                break
            yield data

    # Return the generated stream as a Flask response
    return Response(generate(), mimetype='audio/mp3')

if __name__ == '__main__':
    app.run("0.0.0.0",port=5554)
