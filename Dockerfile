FROM python:3.7-alpine

# Required for Pillow
RUN apk --no-cache add build-base jpeg-dev zlib-dev freetype-dev openjpeg-dev \
                       tiff-dev

ADD . /pyconx

WORKDIR /pyconx


RUN pip install -r requirements.txt


CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "riddle:create_app()  " ]
