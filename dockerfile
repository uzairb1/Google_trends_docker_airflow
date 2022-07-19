FROM python:3.8

RUN apt-get update -y 
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev libsnmp-dev


COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt
#Labels as key value pair
LABEL Maintainer="Uzi.bhatti17"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY api_key.json ./
COPY input/keywords.txt ./
COPY scripts/get_trends.py ./
# Now the structure looks like this '/usr/app/src/test.py

#CMD instruction should be used to run the software
#contained in the image, along with any arguments.

CMD [ "python", "./get_trends.py"]