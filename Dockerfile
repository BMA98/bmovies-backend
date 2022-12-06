# Install a Python image
FROM python:3.9

# Copy data
COPY . app

WORKDIR app

RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev

# Install python dependencies
RUN pip3 install uwsgi
RUN pip install psycopg2-binary
RUN pip3 install -r requirements.txt

# Open port 8000
EXPOSE 8000

# Start app
CMD ["uwsgi", "--ini", "uwsgi.ini"]
