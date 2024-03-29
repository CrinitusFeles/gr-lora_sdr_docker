#
FROM continuumio/miniconda3
#
WORKDIR /gnuradio_lora
RUN apt update
RUN apt -y install build-essential \
      && apt install -y wget \
      && apt install -y git

RUN git clone https://github.com/tapparelj/gr-lora_sdr.git
RUN apt install -y hackrf libhackrf-dev pkg-config
RUN conda env create -f /gnuradio_lora/gr-lora_sdr/environment.yml
RUN echo "conda activate gr310" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
RUN mkdir /gnuradio_lora/gr-lora_sdr/build
WORKDIR /gnuradio_lora/gr-lora_sdr/build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
RUN make install -j 4
WORKDIR /gnuradio_lora

RUN wget https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh \
      && chmod u+x /tmp/cmake-install.sh \
      && mkdir /opt/cmake-3.24.1 \
      && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.24.1 \
      && rm /tmp/cmake-install.sh \
      && ln -s /opt/cmake-3.24.1/bin/* /usr/local/bin

RUN git clone https://github.com/pothosware/SoapyHackRF.git
RUN mkdir /gnuradio_lora/SoapyHackRF/build
WORKDIR /gnuradio_lora/SoapyHackRF/build
RUN cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
RUN make install

RUN pip install python-dotenv

COPY ./flowgraphs /gnuradio_lora
WORKDIR /gnuradio_lora
CMD python RX_TX.py