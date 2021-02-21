FROM python:3.8
MAINTAINER Nathan Pezzotti
WORKDIR /flask_blog
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY flask_blog flask_blog
COPY config.py .
ENV FLASK_APP flask_blog
CMD ["flask", "run", "-h", "0.0.0.0"]
