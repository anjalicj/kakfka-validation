# KAFKA Project to exchange & process events - Docker
## System Set up (WSL)
### Docker
    - Download & install Docker Desktop
        https://docs.docker.com/desktop/install/windows-install/

## Running the project
### Start up the zookeeper and broker containers
    - Ensure Docker is running
        `./build.sh`
    - Runs docker containers for zookeeper, broker
    - Builds image for python processing and runs a container
