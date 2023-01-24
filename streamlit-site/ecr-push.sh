
docker login -u AWS -p $(aws ecr get-login-password --region eu-west-1) 771941357380.dkr.ecr.eu-west-1.amazonaws.com
docker tag careless-ecr:latest 771941357380.dkr.ecr.eu-west-1.amazonaws.com/careless-ecr:latest
docker push 771941357380.dkr.ecr.eu-west-1.amazonaws.com/careless-ecr:latest