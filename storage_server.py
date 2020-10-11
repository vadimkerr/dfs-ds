from flask import Flask, request, jsonify, send_file
from pathlib import Path
import requests
import os
import shutil


app = Flask(__name__)
UPLOAD_DIR = Path("uploads/")


def save_file(file, dir_path, filename):
    dir_path = UPLOAD_DIR / Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    file.save(dir_path / filename)


@app.route('/files', methods=['POST'])
def upload_file():
    file = request.files.get("file")
    path = request.args.get("path")
    filename = request.args.get("filename")

    save_file(file, path, filename)

    return "ok"


@app.route('/files', methods=['GET'])
def download_file():
    path = request.args.get("path")
    filename = request.args.get("filename")

    return send_file(UPLOAD_DIR / Path(path) / filename)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


def join_cluster(naming_server_url, self_url):
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    requests.post(naming_server_url + f"/storage-servers/?url={self_url}")


if __name__ == '__main__':
    join_cluster(os.environ['NAMING_SERVER_URL'], f"http://{os.environ['IP']}:{os.environ['PORT']}")
    app.run(host='0.0.0.0', port=80)
