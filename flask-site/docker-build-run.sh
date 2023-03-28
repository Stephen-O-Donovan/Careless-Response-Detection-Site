docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker build --tag flask-careless-detection .
docker run -p 80:80 flask-careless-detection
# curl localhost:80