FROM ubuntu:14.04

# Let the conatiner know that there is no tty
ENV DEBIAN_FRONTEND noninteractive

# Update the package list
RUN apt-get update

# install dependencies
RUN apt-get install -y \
    git python3-pip \
    # Python C library building dependencies
    build-essential python3-dev \
    # Libraries necessary for connecting to virtuoso
    unixodbc-dev libvirtodbc0

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
ADD odbcinst.ini /etc/odbcinst.ini
ADD load.py /load.py
CMD python3 load.py
