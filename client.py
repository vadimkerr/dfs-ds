import os
import sys
from io import BytesIO
from json import dump, load
from pathlib import Path
from contextlib import suppress
import requests

with suppress(FileNotFoundError):
    with open("settings.json", 'r') as f:
        settings = load(f)
        naming_server_url = settings.get("naming_server_url")


def parse_path(path):
    return os.path.dirname(path), os.path.basename(path)


def mkdir(path):
    requests.post(f"{naming_server_url}/directories/{path}")


def rmdir(path):
    requests.delete(f"{naming_server_url}/directories/{path}")


def ls(path='.'):
    response = requests.get(f"{naming_server_url}/directories/{path}")
    return " ".join(response.json())


def get(path, external_dir='.'):
    dir_path, filename = parse_path(path)
    response = requests.get(f"{naming_server_url}/directories/{dir_path}?filename={filename}")

    with open(Path(external_dir) / filename, 'wb') as f:
        f.write(response.content)


def touch(path):
    dir_path, filename = parse_path(path)
    requests.post(f"{naming_server_url}/directories/{dir_path}?filename={filename}", files={"file": BytesIO()})


def put(external_path, path):
    _, filename = parse_path(external_path)

    with open(external_path, 'rb') as f:
        requests.post(f"{naming_server_url}/directories/{path}?filename={filename}", files={"file": f})


def rm(path):
    dir_path, filename = parse_path(path)
    requests.delete(f"{naming_server_url}/directories/{dir_path}?filename={filename}")


def cp(path, copy_path):
    dir_path, filename = parse_path(path)

    requests.patch(
        f"{naming_server_url}/directories/{dir_path}?filename={filename}&copy_path={copy_path}&copy_filename={filename}&delete=no")


def mv(path, copy_path):
    dir_path, filename = parse_path(path)

    requests.patch(
        f"{naming_server_url}/directories/{dir_path}?filename={filename}&copy_path={copy_path}&copy_filename={filename}&delete=yes")


def info(path):
    dir_path, filename = parse_path(path)

    response = requests.get(f"{naming_server_url}/directories/{dir_path}?filename={filename}&info=yes")
    return response.json()


def init(naming_server_url):
    with open("settings.json", 'w') as f:
        dump({"naming_server_url": naming_server_url}, f)


if __name__ == "__main__":
    command = sys.argv[1]
    command_args = sys.argv[2:]

    func = getattr(sys.modules[__name__], command)

    output = func(*command_args)
    if output:
        print(output)
