# IOT_SmartAquarium
## Building docker
````console
docker buildx build --push --platform linux/arm/v7,linux/arm64/v8 --tag ghcr.io/pippeloo/smart-aquarium:v1.0.0 .
````