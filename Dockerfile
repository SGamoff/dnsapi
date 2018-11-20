FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /dnsapi
RUN mkdir /isc

WORKDIR /dnsapi

ADD ./dnsapi/ /dnsapi
COPY ./requirements/base.txt /dnsapi/requirements.txt
COPY ./requirements/isc/ /isc/
RUN cd /isc && python setup.py install 

RUN pip install -r requirements.txt
