FROM python:3.9

WORKDIR /code

# copy the content of the local directory to the working directory
COPY requirements.txt .

# install dependencies
RUN apt-get -y update
RUN apt-get -y install curl
RUN apt-get install zip -y
RUN apt-get install unzip -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/72.0.3626.69/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

# install FFMPEG on EC2 Amazon Linux
RUN apt-get install ffmpeg libsm6 libxext6 -y