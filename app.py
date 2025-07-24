from flask import Flask, request, jsonify
from flask_cors import CORS 
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/formats', methods=['POST'])
def get_formats():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats_raw = info.get('formats', [])
            formats = []
            for f in formats_raw:
                if not f.get('url'):
                    continue
                formats.append({
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('height') or 'audio',
                    'note': f.get('format_note') or ''
                })
        return jsonify({'formats': formats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    format_id = data.get('format_id')
    if not url or not format_id:
        return jsonify({'error': 'Missing URL or format_id'}), 400
    ydl_opts = {
        'format': format_id,
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'quiet': True,
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

