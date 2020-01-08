FROM python:3.6.8

## The MAINTAINER instruction sets the Author field of the generated images
MAINTAINER author@sample.com
## DO NOT EDIT THESE 3 lines
RUN mkdir /physionet2019
COPY ./ /physionet2019
WORKDIR /physionet2019

## Install your dependencies here using apt-get etc.

## Do not edit if you have a requirements.txt
RUN pip install -r requirements.txt
RUN pip install pystruct
RUN pip install cvxopt
RUN pip install cython
RUN pip install joblib
RUN pip install scikit-learn
RUN pip install pickle-mixin
