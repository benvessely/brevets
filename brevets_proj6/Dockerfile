FROM python:latest 
ADD . /usr/src/app 
WORKDIR /usr/src/app 
RUN pip install -r requirements.txt 
# These lines make it so php output can be seen with docker logging
RUN ln -sf /dev/stdout /var/log/apache2/access.log \
 && ln -sf /dev/stderr /var/log/apache2/error.log
