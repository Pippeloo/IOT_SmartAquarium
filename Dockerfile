FROM python:latest

COPY ./Project/Homebridge.py ./Homebridge.py
COPY ./Project/project.py ./project.py
COPY ./Project/classes ./classes
COPY ./Project/streamCam/picam-stream.sh ./streamCam/picam-stream.sh
#COPY ./Project/streamCam/setup.config ./streamCam/setup.config
COPY ./Project/assets/fish.jpg ./assets/fish.jpg
COPY ./Project/start.sh ./start.sh

 RUN pip install --no-cache-dir rpi.gpio &&\
    pip install adafruit-blinka &&\
    pip install adafruit-circuitpython-pcd8544 &&\
    pip install pillow &&\
    pip install requests &&\
    pip install ply &&\
    pip install jinja2 &&\
    pip install pyyaml


RUN apt update

RUN apt install -y ffmpeg

RUN apt install -y git ninja-build meson libgnutls28-dev
RUN apt install -y meson libgnutls28-dev g++ pkg-config openssl python3-yaml python3-ply python3-jinja2 libboost-dev
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && cd libcamera && meson build && ninja -C build install

RUN apt install -y libepoxy-dev
RUN apt install -y libjpeg-dev
RUN apt install -y libtiff5-dev

RUN apt install -y cmake libboost-program-options-dev libdrm-dev libexif-dev
RUN cd && git clone https://github.com/raspberrypi/libcamera-apps.git && cd libcamera-apps && mkdir build && cd build && cmake ../ -DENABLE_DRM=1 -DENABLE_X11=0 -DENABLE_QT=0 -DENABLE_OPENCV=0 -DENABLE_TFLITE=0 && make install
RUN ldconfig

CMD ["bash", "start.sh"]