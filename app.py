from flask import Flask, render_template, request, jsonify
from summarize import get_subtitles, get_summary
from youtube_transcript_api._errors import NoTranscriptFound, CouldNotRetrieveTranscript

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcript')
def transcript():
    video_id = request.args.get('video_id')
    return get_subtitles(video_id)

@app.post('/api/summary')
def video():
    try:
        video_id = request.json.get('video_id')
        subtitles = get_subtitles(video_id)
        return get_summary(subtitles)
    except NoTranscriptFound:
        return jsonify({'error': True, 'message': 'English captions not available for this video.'}), 404
    except CouldNotRetrieveTranscript as e:
        return jsonify({'error': True, 'message': e.cause.split('\n')[0]}), 500
    except Exception as e:
        return jsonify({'error': True, 'message': "Some error occured while proccessing."}), 500

if __name__ == '__main__':
    app.run(debug=False, threaded=True)