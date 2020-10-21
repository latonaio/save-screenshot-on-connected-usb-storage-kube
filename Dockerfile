# FROM python-library-l4t:latest
FROM latonaio/l4t:latest

# Definition of a Device & Service
RUN apt update && apt install -y  libjpeg-dev zlib1g-dev python3-tk python3-dev scrot
ENV POSITION=Runtime \
    SERVICE=save-screenshot-on-connected-usb-storage\
    AION_HOME=/var/lib/aion
RUN mkdir ${AION_HOME}
WORKDIR ${AION_HOME}
# Setup Directoties
RUN mkdir -p \
    $POSITION/$SERVICE
WORKDIR ${AION_HOME}/$POSITION/$SERVICE/
ADD . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
# CMD ["/bin/sh", "-c", "while :; do sleep 10; done"]
# CMd ["./docker-entrypoint-scripts/docker-entrypoint.sh"]
CMD ["/bin/sh", "docker-entrypoint.sh"]
