# Install from Ubuntu image
FROM ubuntu:18.04

# Install base libraries
RUN apt-get update && apt-get install -y curl build-essential python3 python3-dev python3-pip

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
# Install UnixODBC
RUN apt-get install -y unixodbc-dev unixodbc

# Copy data
COPY . app

# Install python dependencies
RUN pip3 install uwsgi
RUN pip3 install -r app/requirements.txt

# Open port 8000
EXPOSE 8000

# Start app
CMD ["uwsgi", "--ini", "app/uwsgi.ini"]
