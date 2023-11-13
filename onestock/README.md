## Build
    docker build --tag eu.gcr.io/flows-onestock-dev/onestock -f runs/onestock/Dockerfile .

## Run in development mode

    docker run --rm -p 9090:8080 -e PORT=8080 -e ENV=dev -v /home/guillaumepayen/sa/flows-onestock-dev.json:/root/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/root/key.json -e ONESTOCK_LOGIN=darj_user -e ONESTOCK_PASSWORD="XXXXX" -v /home/guillaumepayen/projects/flows-onestock/runs/onestock/src:/app/src eu.gcr.io/flows-onestock-dev/onestock

## Call the API
    curl -d '{"message":{"data": "TEST"}}' -H "Content-Type: application/json" -X POST http://localhost:9090
