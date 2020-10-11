from flask import Flask, request, jsonify, send_file
import requests
import random
from datetime import datetime
import os

app = Flask(__name__)
directories = {}
storage_servers = {}

NUM_COPIES = 2


def get_available_servers():
    servers = list(storage_servers.keys())

    available_servers = []
    for server_url in servers:
        response = requests.get(server_url + "/ping")
        if response.status_code == 200:
            available_servers.append(server_url)

    return available_servers


def select_storage_servers_for_upload():
    available_servers = get_available_servers()
    return random.sample(available_servers, NUM_COPIES)


def select_storage_server_for_download(path, filename):
    available_servers = get_available_servers()

    selected_servers = []
    for url in available_servers:
        if f'{path}/{filename}' in storage_servers[url]:
            selected_servers.append(url)

    return random.choice(selected_servers)


def upload_file(file, path, filename):
    for server_url in select_storage_servers_for_upload():
        response = requests.post(server_url + f'/files?path={path}&filename={filename}', files={'file': file})
        storage_servers[server_url].update({f'{path}/{filename}': True})
        print(response.status_code)


def download_file(path, filename):
    server_url = select_storage_server_for_download(path, filename)
    response = requests.get(server_url + f'/files?path={path}&filename={filename}')
    print(response.status_code)
    return response.content


@app.route('/directories/<path:path>', methods=['POST'])
def create(path):
    filename = request.args.get("filename")
    if filename:
        file = request.files["file"]

        file_info = {
            "size": len(file.read()),
            "created_at": datetime.now(),
        }

        file.seek(0)

        if path not in directories:
            directories[path] = {}

        directories[path].update({filename: file_info})
        upload_file(file, path, filename)

        return "file created"

    directories.update({path: {}})
    return "directory created"


@app.route('/directories/<path:path>', methods=['DELETE'])
def remove(path):
    filename = request.args.get("filename")
    if filename:
        del directories[path][filename]
        return "file removed"

    del directories[path]
    return "directory removed"


@app.route('/directories/<path:path>', methods=['GET'])
def read(path):
    filename = request.args.get("filename")
    info = request.args.get("info")
    if filename:
        if info == "yes":
            return directories[path][filename]
        else:
            return download_file(path, filename)

    filenames = list(directories[path].keys())

    def get_child_directories(dir_path):
        return [directory for directory in directories if
                directory.startswith(path) and directory != path and len(directory.split("/")) == 2]

    directory_names = [directory.split("/")[1] for directory in get_child_directories(path)]
    return jsonify(filenames + directory_names)


@app.route('/directories/', methods=['GET'])
def read_root():
    filename = request.args.get("filename")
    if not filename:
        return directories


@app.route('/directories/<path:path>', methods=['PATCH'])
def update(path):
    filename = request.args.get("filename")
    copy_filename = request.args.get("copy_filename")
    copy_path = request.args.get("copy_path")
    delete = request.args.get("delete")

    file_info = directories[path][filename]
    directories[copy_path].update({copy_filename: file_info})

    file = download_file(path, filename)
    upload_file(file, copy_path, copy_filename)

    if delete == "yes":
        del directories[path][filename]

    return "ok"


@app.route('/storage-servers/', methods=['POST'])
def add_storage_server():
    url = request.args.get("url")
    storage_servers.update({url: {}})
    return "storage server added"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
