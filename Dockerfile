FROM python:3.9.1

#RUN apt-get update && apt-get install -y python3-opencv
#RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN apt-get install -y tesseract-ocr

WORKDIR /input

RUN wget http://files.deeppavlov.ai/fb_text_detection_v1/archive.zip

RUN unzip archive.zip; rm archive.zip

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /

COPY *.py /

ARG SERVICE_PORT
ENV SERVICE_PORT ${SERVICE_PORT}

HEALTHCHECK --interval=5s --timeout=90s --retries=3 CMD curl --fail 127.0.0.1:${SERVICE_PORT}/healthcheck || exit 1

CMD gunicorn --workers=1 server:app -b 0.0.0.0:${SERVICE_PORT} --timeout=300
