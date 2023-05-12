# Social Networking application

## How do I get this set up on my system?

You would need to have docker installed in your system to run this.
[Install Docker desktop](https://www.docker.com/products/docker-desktop/)

### Backend setup
- run  `cp .env.template .env` - that will create a .env file
- run `docker-compose up` - this will build the docker containers (if they are not there) and start the containers
- run `docker-compose up -d` - if you don't want to keep the docker logs running after `docker-compose up`
- the backend will run on localhost:8000
- `docker-compose logs -f service-name-here` - to see the logs, service-name = backend | postgres | ...

### Postman API setup
- You can import the `sna.postman_collection.json` kept in the project's root
- [Postman documentation link](https://documenter.getpostman.com/view/6546877/2s93ecuVFd)

## How to see mails
- The mails are sent to mailhog on localhost:8025

## Some common commands
- `make bash` - takes you inside the backend docker container running
- `make shell`- runs django shell_plus inside the backend container
- refer to the `Makefile` for some more commands

--- 

## Features
- [] API to search other users by email and name
- [] API to send/accept/reject friend request
- [] API to list friends
- [] List pending friend requests
- [] Users can not send more than 3 friend requests within a minute