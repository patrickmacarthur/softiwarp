FROM centos:7
RUN yum -y install binutils gcc make kernel-devel-3.10.0-514.el7.x86_64 && yum clean all
RUN yum -y --enablerepo=C7.2.1511-base install kernel-devel-3.10.0-327.el7.x86_64 && yum clean all
RUN yum -y --enablerepo=C7.1.1503-base install kernel-devel-3.10.0-229.el7.x86_64 && yum clean all
RUN yum -y --enablerepo=C7.0.1406-base install kernel-devel-3.10.0-123.el7.x86_64 && yum clean all
CMD [ "/var/tmp/softiwarp/contrib/do-build-centos.sh" ]
