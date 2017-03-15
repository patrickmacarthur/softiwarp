FROM ubuntu:xenial
RUN apt -y update && apt -y install build-essential linux-headers-4.4.0-21-generic && apt -y clean
CMD [ "/var/tmp/softiwarp/contrib/do-build-ubuntu.sh" ]
