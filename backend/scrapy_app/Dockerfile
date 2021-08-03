FROM python:3.8-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1

# Pip dependency Twisted needs gcc
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y poppler-utils

# Install any needed packages specified in requirements.txt (for scrapyd)
ADD ./requirements.txt .
RUN pip install -r ./requirements.txt

# Set the working directory to /scrapy
WORKDIR /backend/scrapy_app

EXPOSE 6800

CMD scrapyd