
FROM python:3.7

ADD ./requirements.txt /code/requirements.txt
WORKDIR /code

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD . /code

RUN pip install uwsgi
CMD uwsgin --ini run.ini