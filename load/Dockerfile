# Build based on virtuoso container in order to have access to virtuoso's
# isql command.
FROM caprenter/automated-build-virtuoso

RUN apt-get update

# install dependencies
RUN apt-get install -y \
    git python3-pip \
    # Python C library building dependencies
    build-essential python3-dev


RUN git clone https://github.com/OpenDataServices/cove.git /usr/src/cove
WORKDIR /usr/src/cove
RUN git checkout resourceprojects-etl

# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

RUN pip3 install -r /usr/src/cove/requirements.txt
RUN python3 manage.py migrate --noinput
# TMP moveme
RUN apt-get install -y gettext
RUN python3 manage.py compilemessages
RUN python3 manage.py collectstatic --noinput
RUN pip3 install gunicorn
# Massive hack
RUN mkdir .ve && ln -s ../src .ve/src
# TMP moveme
RUN echo 1 && git pull
EXPOSE 80
CMD gunicorn cove.wsgi -b 0.0.0.0:80
