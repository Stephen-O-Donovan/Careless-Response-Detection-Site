docker build --progress=plain -t demo/cds .
docker run -it --rm -p '8501:8501' demo/cds