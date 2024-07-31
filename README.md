# wake-on-lan-docker-bridge
Docker container that can act as a TCP to UDP bridge allowing for containers to run Wake-On-Lan commands from bridge networking

```
docker-compose up

echo <<WOL_MAC_ADDRESS>> | nc <<DOCKER_HOST_IP>> 55555
```