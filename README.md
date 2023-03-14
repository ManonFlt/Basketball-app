# Basketball-app 🏀
This repository is our final project for the Cloud Computing course.

It aims at creating a Flask application with multiple containers, a bridge network, volumes and bind mounts.


## Prerequisites
Have Docker and docker compose installed on your host machine.
Install Docker according to your OS:
- [Install Docker on Linux](https://devinci-online.brightspace.com/content/enforced/90043-MESIIN482022/Installing%20Docker%20on%20Linux.pdf?_&d2lSessionVal=G3ZDsw8zwnkzDA6EVga1ydyJu)
- [Install Docker on Windows 10/11]( https://devinci-online.brightspace.com/content/enforced/90043-MESIIN482022/Installing%20Docker%20with%20WSL2%20on%20Windows%2010%20&%2011.pdf?_&d2lSessionVal=G3ZDsw8zwnkzDA6EVga1ydyJu)
- [Install Docker on MacOS]( https://devinci-online.brightspace.com/content/enforced/90043-MESIIN482022/Installing%20Docker%20on%20macOS.pdf?_&d2lSessionVal=G3ZDsw8zwnkzDA6EVga1ydyJu)

Install docker compose:
- [Install the Compose pluging](https://docs.docker.com/compose/install/linux/)

Then, clone this repository.

## Build the app
Download this project in a linux system or subsystem (wsl typically).

Open a terminal.

Reach the root of the project via the cd command:
```bash
cd 'your root'
```
Build the docker image of the flask webapp :
```bash
docker-compose up
```
Finally, you can visit the web application at the following URL :
http://localhost:5000/
