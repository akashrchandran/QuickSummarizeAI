from flask import Flask, render_template, request, jsonify
from summarize import get_subtitles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.post('/api/summary')
def video():
    print(request.data)
    video_id = request.json.get('video_id')
    print(video_id)
    subtitles = get_subtitles(video_id)
    return jsonify({
        "error": False,
        "subtitles": subtitles
    })

if __name__ == '__main__':
    app.run(debug=True)