FROM alpine:edge

WORKDIR /app

RUN apk --no-cache add bash python3
RUN pip3 install --trusted-host pypi.python.org --upgrade pip

RUN apk --no-cache add py3-lxml
ADD requirements.txt /app/
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ADD scraper /app/scraper/

ADD CONFIG /app/

ADD entry.sh /app/

ADD crontab /app/
RUN /usr/bin/crontab /app/crontab

ADD gmail_token.pickle /app/

# self-documentation
ADD Dockerfile /app/

CMD ["/bin/bash", "entry.sh"]
