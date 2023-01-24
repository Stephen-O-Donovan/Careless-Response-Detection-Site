docker build --progress=plain -t careless-ecr .
docker run -it --rm -p '8501:8501' careless-ecr 