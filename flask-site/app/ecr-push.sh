#!/bin/bash

#Need to supply the ECR path to contain the docker image on AWS
#Use jq command, test first that it is installed
test_json=$(echo "{ }" | jq)
if [ "$test_json" != "{}" ]; then
        echo "jq not installed"
        exit 1
fi

#Test that the file containing the AWS link exists
config='aws_links.json'

if [ ! -f "$config" ]; then
        echo "config file $config not valid"
        exit 2
fi

json=$(cat $config)

readJsonConfig() {
        echo $json | jq -r $1
}

AWS_ECR_URL=$(readJsonConfig ".AWS_ECR_URL")

docker login -u AWS -p $(aws ecr get-login-password --region eu-west-1) $AWS_ECR_URL
docker tag flask-careless-detection:latest $AWS_ECR_URL/flask-careless-detection:latest
docker push $AWS_ECR_URL/flask-careless-detection:latest