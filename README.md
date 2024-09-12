# execute-python-api

## Simple Flask API that accepts Python scripts in the request body and returns the resultof the main() function

### Requirements for use:
1. Request body must be in the JSON form {"script": "def main(): ...}
2. The script in the request must contain a function main()
3. The function main() must return a JSON object (e.g. {"result": "Hello World!"})

### Characteristics of the Service:
1. Uses nsjail to execute python scripts safely
2. Scripts sent in the request will have access to pandas, numpy, and os python packages by default (Use 'pd' for pandas, 'np' for numpy, 'os' for os)
3. Returns ONLY the result of the main() function - print statements will not be returned 

### Running Service Locally
1. Pull the docker image from docker hub: 'docker pull billyramundo/sandbox:v1.0' (dockerhub link: https://hub.docker.com/layers/billyramundo/sandbox/v1.0/images/sha256-15c015dad06f46760fe6dce678334a15d34cc2e7c1a23f9f3cc37623023aabaa?context=repo)
2. Run the image in a container, exposing the correct port: 'docker run -p 8080:8080 billyramundo/sandbox:v1.0'
3. Hit the endpoint at port 8080 on localhost with an appropriate request

### Example request:
The markdown syntax causes problems if I try to directly place a script here in the curl request, so you can use the make_python_script directory in this project to make your own.

Just write a python script in the script.py file (or there is an example there already). Then run the create_request.py file, which will output correctly formatted json to the payload.json file. Then you can run the below command to try out the service. You must be in the make_python_script directory for this command to work as-is (you will have to change the path to payload.json otherwise)

#### Local testing:
curl -X POST http://127.0.0.1:8080/execute -H "Content-Type: application/json" --data @payload.json

#### Publicly Accessible Google Cloud Run Service:
curl -X POST https://execute-python-868716487270.us-central1.run.app/execute -H "Content-Type: application/json" --data @payload.json