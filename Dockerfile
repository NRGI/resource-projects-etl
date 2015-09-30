# Build based on virtuoso container in order to have access to virtuoso's
# isql command.
FROM caprenter/automated-build-virtuoso

RUN apt-get update

RUN mkdir /usr/src/resource-projects-etl
WORKDIR /usr/src/resource-projects-etl

# install dependencies
RUN apt-get install -y \
    git python3-pip gettext \
    # Python C library building dependencies
    build-essential python3-dev

# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8   

ADD requirements_taglifter.txt requirements_taglifter.txt
# These are included by requirements.txt but by installing explicitly
# first we can use a cached copy when other requirements change.
RUN pip3 install -r requirements_taglifter.txt
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD modules modules
ADD setup.py setup.py
RUN python3 setup.py install

ENV DJANGO_SETTINGS_MODULE settings

RUN manage.py migrate --noinput
RUN manage.py compilemessages
RUN manage.py collectstatic --noinput

ADD ontology ontology

EXPOSE 80
CMD gunicorn cove.wsgi -b 0.0.0.0:80
