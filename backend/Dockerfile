FROM python:3.9-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /backend

# Pip dependency Twisted needs gcc
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y poppler-utils
RUN pip install pipenv

# Set the working directory to /django
WORKDIR /backend

# Install needed packages specified in requirements.txt
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# OCCAM Transcription
RUN pip install git+https://github.com/CrossLangNV/OCCAM_transcription.git

# Copy App
COPY . .

RUN chmod +x start.sh