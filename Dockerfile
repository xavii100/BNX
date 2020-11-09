FROM docker-enterprise-prod.artifactrepository.citigroup.net/developersvcs-python-ai/redhat-python3.6/rhel7/redhat-python-rhel7:latest

# add yum repos to properly install gcc and yum-utils
RUN yum-config-manager --setopt=gpgcheck=0 --add-repo http://openopen.nam.nsroot.net/openopen/not-cert/rhel7-x86_64/latest/RPMS.all --nogpgcheck && \
    yum-config-manager --setopt=gpgcheck=0 --add-repo http://openopen.nam.nsroot.net/openopen/repos/rhel-7-server-rpms/

# install gcc to compile python packages.
RUN touch /var/lib/rpm/* && \
    yum install --setopt=gpgcheck=0 -y yum-utils gcc && \
    yum clean all

# Flask environment variables.
ENV FLASK_APP=setup.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    LC_ALL=en_US.utf-8 \
    LANG=en_US.utf-8 \
    PIP_CONFIG_FILE=/app/pip.conf

WORKDIR /app

#RUN yum install -y mailx
RUN yum install -y mailx --setopt=gpgcheck=0 
RUN echo "set smtp=imbapprelay.wlb2.nam.nsroot.net" >> /etc/mail.rc
RUN echo "set ssl-verify=ignore" >> /etc/mail.rc
RUN echo "set nss-config-dir=/etc/pki/nssdb/" >> /etc/mail.rc

# create python symlink so gcc can find python3.6m when installing modules requiring compilation
RUN mkdir /opt/rh/rh-python36 -p && ln -s /opt/middleware/redhat_python/3.6.3 /opt/rh/rh-python36/root

# Install dependencies
COPY pip.conf requirements.txt ./
RUN pip install -r requirements.txt

# Copy application source code into image
COPY . ./

# Setup runtime .
RUN chmod -R g+rwx .
EXPOSE 8080
CMD ["flask", "run"]