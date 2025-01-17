FROM ansible/centos7-ansible:latest

# add yum repos to properly install gcc and yum-utils
RUN yum update -y && \
##  yum-config-manager --setopt=gpgcheck=0 --add-repo http://https://dl.fedoraproject.org/pub/epel/8/Everything/x86_64/ --nogpgcheck && \
#    touch /var/lib/rpm/* && \
    yum install --setopt=gpgcheck=0 -y yum-utils gcc && yum clean all && \
    yum install python3 -y

# Flask environment variables
ENV FLASK_APP=setup.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    LC_ALL=en_US.utf-8 \
    LANG=en_US.utf-8 \
    PIP_CONFIG_FILE=/app/pip.conf 

WORKDIR /app

# create python symlink so gcc can find python3.6m when installing modules requiring compilation
RUN mkdir /opt/rh/rh-python36 -p && ln -s /opt/middleware/redhat_python/3.6.3 /opt/rh/rh-python36/root

# Install dependencies
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy application source code into image
COPY . .

# Setup runtime
RUN chmod -R g+rwx .
EXPOSE 8080
CMD ["python", "setup.py"]