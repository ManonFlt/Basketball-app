# We pull the python 3.8 slim-buster image which is a lighter version of python
# Python will be our base for our flask web applications
FROM python:3.8-slim-buster

# We define the working directory as "/app", it will be the root for all our project files
WORKDIR /app

# We copy all the files and directories contained in folder as the Dockerfile
COPY . .

# When we mount our web application image, we want to run the script below
# It will give the right to execute ('+x' means that we add the right to execute) the present shell script
# This shell script allows us to wait for a certain service to be run before running an other command
RUN chmod +x ./wait-for-it.sh

# Also while mounting the image, we use the pip3 package manager to install the modules required for our application to work properly
# The '-r' option means that the dependencies needed will be extracted from a certain file (here 'requirements.txt')
RUN pip3 install -r requirements.txt
