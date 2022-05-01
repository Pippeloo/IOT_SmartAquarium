FROM python:latest

COPY ./Project/Homebridge.py ./Homebridge.py
COPY ./Project/project.py ./project.py
COPY ./Project/classes ./classes
COPY ./Project/streamCam/picam-stream.sh ./streamCam/picam-stream.sh
COPY ./Project/streamCam/setup.config ./streamCam/setup.config
COPY ./Project/assets/fish.jpg ./assets/fish.jpg
COPY ./Project/start.sh ./start.sh

 RUN pip install --no-cache-dir rpi.gpio &&\
    pip install adafruit-blinka &&\
    pip install adafruit-circuitpython-pcd8544 &&\
    pip install pillow &&\
    pip install ply &&\
    pip install jinja2 &&\
    pip install pyyaml


RUN apt update

RUN apt install -y ffmpeg
RUN apt install -y git ninja-build meson libgnutls28-dev
RUN apt install -y meson libgnutls28-dev g++ pkg-config openssl python3-yaml python3-ply python3-jinja2 libboost-dev
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && cd libcamera && meson build && ninja -C build install

CMD ["bash", "start.sh"]