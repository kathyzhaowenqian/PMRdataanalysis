FROM python:3.10

# Set build-time environment variable lots of todo
ARG DJANGO_SECRET_KEY

ARG POSTGRESQL_INTERNAL_HOST
ARG POSTGRESQL_INTERNAL_PORT
ARG POSTGRESQL_INTERNAL_PASSWORD
ARG POSTGRESQL_INTERNAL_USERNAME
ARG POSTGRESQL_INTERNAL_DBNAME


ARG ALI_ECS_EXTERNAL_IP
ARG ALIYUN_ACCESS_ID
ARG ALIYUN_ACCESSKEY_SECRET


# Set environment variables,lots of to do
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY

ENV POSTGRESQL_INTERNAL_HOST $POSTGRESQL_INTERNAL_HOST
ENV POSTGRESQL_INTERNAL_PORT $POSTGRESQL_INTERNAL_PORT
ENV POSTGRESQL_INTERNAL_PASSWORD $POSTGRESQL_INTERNAL_PASSWORD
ENV POSTGRESQL_INTERNAL_USERNAME $POSTGRESQL_INTERNAL_USERNAME
ENV POSTGRESQL_INTERNAL_DBNAME $POSTGRESQL_INTERNAL_DBNAME


ENV ALI_ECS_EXTERNAL_IP $ALI_ECS_EXTERNAL_IP
ENV ALIYUN_ACCESS_ID $ALIYUN_ACCESS_ID
ENV ALIYUN_ACCESSKEY_SECRET $ALIYUN_ACCESSKEY_SECRET


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



LABEL version ="0.1"
LABEL maintainer="Kathy Zhao"

# 创建一个项目文件
RUN mkdir /pmrdataanalysis

# 创建一个 static 静态文件夹，用来存放 python manage.py collectstatic 的目录
RUN mkdir /djangostatic


# 把当前路径下的 django项目 文件夹(比如myobject1)的内容 拷贝到容器 /djangotest 文件夹下
# 注意如果是文件夹的话，这里的必须是相对路径
COPY . /pmrdataanalysis

# 进入到容器内工作目录就是 /anglissData
WORKDIR /pmrdataanalysis

# 设置时间为上海时间
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


# 安装 requirements.txt 模块
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
