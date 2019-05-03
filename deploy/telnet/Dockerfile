FROM python:3.7-alpine

# Required for Pillow
RUN apk --no-cache add build-base jpeg-dev zlib-dev freetype-dev openjpeg-dev \
                       tiff-dev

ADD ../../. /pyconx

WORKDIR /pyconx


RUN pip install -r requirements.txt



CMD ["pyhton", "-m", "riddle/game/wasp10/old" ]
