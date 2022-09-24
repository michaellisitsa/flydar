FROM python:3.9-buster

# Apt-get update and initial installations
RUN apt-get update && apt-get install 
# RUN apt-get install nodejs npm -y 

# Copy source files and install py packages
RUN mkdir -p /opt/flydar
RUN mkdir -p /opt/flydar/pip_cache
COPY . /opt/flydar
WORKDIR /opt/flydar
RUN pip install -r requirements.txt --cache-dir /opt/flydar/pip_cache

# Allow access to port 8000
EXPOSE 8000
STOPSIGNAL SIGTERM

# Start server
CMD ["/opt/flydar/start-server.sh"]