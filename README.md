# IOT_SmartAquarium
## Building docker
````Shell
docker buildx build --push --platform linux/arm/v7,linux/arm64/v8 --tag ghcr.io/pippeloo/smart-aquarium:latest .
````

## Running the docker
````Shell
docker-compose up -d
````