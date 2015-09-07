# A container for using python3/ipython
# with irods and graphdb (neo4j)

FROM irods/icommands:4.0.3
MAINTAINER "Paolo D'Onorio De Meo <p.donoriodemeo@gmail.com>"

# Not essential, but wise to set the lang
# Note: Users with other languages should set this in their derivative image
RUN apt-get update && apt-get install -y language-pack-en
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

# Usefull for using an interactive bash
ENV TERM xterm
# Remove duplicates in bash history terminal
RUN echo "export HISTCONTROL=ignoreboth:erasedups" > $HOME/.bashrc

# Python 3 packages
RUN apt-get install -y \
    wget curl git telnet \
    python-setuptools python3-dev python3-pip

RUN pip3 install ipython \
    click plumbum \
    py2neo neomodel \
    jupyter
    # python-irodsclient #does not work with python 3

####################################
### EPIC CLIENT - and python 2 ...
RUN apt-get install -y \
    python-pip python-dev libxml2-dev libxslt-dev && \
    pip2 install lxml httplib2 simplejson defusedxml

RUN wget http://j.mp/eudat_epic_client -q -O /opt/epicclient.py && \
    chmod +x /opt/epicclient.py && \
    ln -s /opt/epicclient.py /usr/bin/epicc
# test
RUN epicc -h

####################################
RUN useradd -ms /bin/bash dev
ENV HOME /home/dev

