FROM python:3.9.8-slim
COPY requirements.txt /
EXPOSE 8000
RUN pip3 install -r /requirements.txt
COPY . /
WORKDIR /
RUN chmod +x run.sh
ENTRYPOINT ["sh","/run.sh"]