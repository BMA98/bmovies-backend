# Install from Ubuntu image
FROM ubuntu:18.04

# Install base libraries
RUN apt-get update && apt-get install -y curl build-essential python3 python3-dev python3-pip

# Copy data
COPY . app

# Install python dependencies
RUN pip3 install uwsgi
RUN pip3 install -r app/requirements.txt

# Open port 8000
EXPOSE 8000

# Start app
CMD ["uwsgi", "--ini", "app/uwsgi.ini"]
