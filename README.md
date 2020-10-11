# DS: Distributed File System

## Naming server
`docker run --rm -it -p 80:80 vadimkerr/dfs-naming-server`

## Storage server
`docker run -p 80:80 -e IP=<SELF-IP> -e PORT=80 -e NAMING_SERVER_URL=http://<NAMING-SERVER-IP> vadimkerr/dfs-storage-server`

**Note:** at least 2 storage servers required for system to function properly

## Client

`python client.py <command> <args>`

Available commands:

Initialize: `python client.py init <NAMING-SERVER-URL>`

Create file: `python client.py touch <PATH>`

Download file: `python client.py get <REMOTE-PATH> <LOCAL-DIR>`

Upload file: `python client.py put <LOCAL-PATH> <REMOTE-DIR>`

Delete file: `python client.py rm <PATH>`

File info: `python client.py info <PATH>`

Copy file: `python client.py cp <PATH> <DIR>`

Move file: `python client.py mv <PATH> <DIR>`

List files: `python client.py ls <DIR>`

Create directory: `python client.py mkdir <DIR>`

Remove directory: `python client.py rmdir <DIR>`

## Used stack and protocols

HTTP is used as the protocol for communication and file transfers. Servers are implemented using Python and Flask.

## Docker images

Naming server: https://hub.docker.com/r/vadimkerr/dfs-naming-server

Storage server: https://hub.docker.com/r/vadimkerr/dfs-storage-server

## Connect to demo naming server

`python client.py init http://52.91.212.21`
