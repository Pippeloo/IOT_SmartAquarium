# IOT_SmartAquarium
## Files Project
All the files used for the project can be found under 'Project'

## Starting the project
To manually start the project execute the 'start.sh' under 'Project' this will launch everything

## Building docker
````Shell
docker buildx build --push --platform linux/arm/v7,linux/arm64/v8 --tag ghcr.io/pippeloo/smart-aquarium:latest .
````

## Running the docker
````Shell
docker-compose up -d
````