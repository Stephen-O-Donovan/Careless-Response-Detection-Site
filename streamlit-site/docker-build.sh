

# # build Docker image in current directory
# docker build -t 'latest' .
# # Run docker image with port 8501 and volumes
# docker run -it --rm --port '8501:8501' -v '$(pwd)/data:/usr/scr/app/data:delegated' -v '$(pwd)/project:/usr/scr/app/project:delegated' latest

docker-compose up -d
# docker build --progress=plain -t careless-ecr .
# docker run -it --rm -p '8501:8501' careless-ecr 