FROM python:3.8-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Pip dependency Twisted needs gcc
RUN apt-get update
RUN apt-get install -y gcc

# create root directory for our project in the container
RUN mkdir /scrapy_app

# Set the working directory to /scrapy
WORKDIR /backend/scrapy_app

# Install any needed packages specified in requirements.txt
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# Copy spiders
COPY scrapy.cfg /scrapy_app
COPY scrapy_app /backend/scrapy_app/scrapy_app

EXPOSE 6800

CMD scrapyd