FROM centos/python-36-centos7

USER root

RUN yum -y install gcc-c++ pkgconfig python3-devel \
    yum -y install libXext libSM libXrender \
    yum -y install \
    epel-release \
    gcc \
    python-devel \
    python-pip \
    python-poppler \
    poppler-utils

RUN pip install --upgrade pip==20.3.3
RUN pip install --upgrade setuptools==50.3.0
 
RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code
RUN pip install --no-cache-dir -r requirements.txt --use-feature=2020-resolver

COPY . search_classify_tweets

RUN chmod -R +x /code

# RUN APPLICATION
EXPOSE 5000
CMD ["gunicorn", "-c", "search_classify_tweets/projeto/config.py", "search_classify_tweets:app"]