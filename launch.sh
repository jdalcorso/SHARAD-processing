docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -t --name jordydc --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) -w $(pwd) jordy:latest python \
 src/azimuth.py