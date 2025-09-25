FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.11

RUN yum update -y && yum install -y \
    wget \
    unzip \
    which \
    xorg-x11-server-Xvfb \
    gtk3 \
    libXScrnSaver \
    GConf2 \
    alsa-lib \
    && yum clean all

# Chromeとchromedriverをインストール
RUN wget -O /tmp/chrome-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/119.0.6045.105/linux64/chrome-linux64.zip \
    && unzip /tmp/chrome-linux64.zip -d /opt/ \
    && mv /opt/chrome-linux64 /opt/chrome \
    && chmod +x /opt/chrome/chrome \
    && wget -O /tmp/chromedriver-linux64.zip https://storage.googleapis.com/chrome-for-testing-public/119.0.6045.105/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver-linux64.zip -d /opt/ \
    && mv /opt/chromedriver-linux64/chromedriver /opt/chromedriver \
    && chmod +x /opt/chromedriver \
    && ls -la /opt/chromedriver \
    && rm -rf /tmp/*

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]