FROM ubuntu:xenial

RUN apt-get clean && apt-get update && apt-get install -y locales
# setup environment
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

# setup keys
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list

# setup environment
EXPOSE 8080
EXPOSE 7681
EXPOSE 11345

# install bootstrap tools
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        sudo \
        wget \
        nano \
        libgsl-dev \
        swig \
        libgeos++-dev \
        libgeos-dev \
        python-rosdep \
        python-rosinstall \
        python-vcstools \
        python-rosinstall-generator \
        python-wstool \
        build-essential \
        python-dev \
        python3-dev \
        python-pip \
        python3-pip \
        python-virtualenv \
        python-wheel \
        python-setuptools \    
        python3-setuptools && \            
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip2 install --upgrade pip && \
    pip3 install --upgrade pip    

RUN adduser --disabled-password --gecos '' docker && \
    adduser docker sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

# bootstrap rosdep
RUN sudo rosdep init &&\
    rosdep update

# install ros packages
ENV ROS_DISTRO kinetic

# from kinetic-desktop-xenial
RUN sudo apt-get update && \
    sudo apt-get install -y \
        ros-kinetic-desktop-full=1.3.1-0* && \
    sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D2486D2DD83DB69272AFE98867170598AF249743
RUN sudo echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable xenial main" | sudo tee -a /etc/apt/sources.list.d/gazebo-stable.list && \
    sudo apt-get update && \ 
    sudo apt-get install -q -y \
            gazebo7 \
            libgazebo7-dev \
            imagemagick \
            libjansson-dev \
            nodejs \
            nodejs-legacy \
            npm \
            psmisc \
            xvfb \
            locate \ 
            libignition-math2-dev \
            ros-kinetic-turtlebot-simulator \
            ros-kinetic-turtlebot3-simulations && \
    sudo apt-get clean && \        
    sudo rm -rf /var/lib/apt/lists/*


# clone player/stage
RUN cd && \
    git clone https://github.com/playerproject/player && \
    cd player && \
    mkdir build && \
    cd build && \
    cmake -DBUILD_PLAYERCC=ON -DBUILD_PYTHONCPP_BINDINGS=ON -j2 .. && \
    make -j2 && \
    sudo make install -j2

RUN cd && \
    git clone https://github.com/rtv/Stage stage && \
    cd stage && \
    mkdir build && \
    cd build && \
    cmake -j2 .. && \
    make -j2 && \
    sudo make install -j2    

ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib

RUN sudo -H pip2 install gym && \
    sudo -H pip3 install gym

# clone dl repositories
ENV PYTHONPATH $PYTHONPATH:/home/docker/dl-learning
RUN cd && \
    git clone https://github.com/JdeRobot/robotics-gym.git && \
    cd robotics-gym && \
    sudo python setup.py install && \
    cd && \
    git clone https://github.com/JdeRobot/dl-learning.git && \
    cd dl-learning && \
    sudo -H pip2 install -r requirements.txt && \
    sudo -H pip3 install -r requirements.txt

# clone gzweb
ENV GZWEB_WS /home/docker/gzweb
RUN cd && \
    hg clone https://bitbucket.org/osrf/gzweb $GZWEB_WS && \
    /bin/bash -c "source /usr/share/gazebo/setup.sh" && \
    cd ${GZWEB_WS} && \
    hg up default  &&\
    sudo xvfb-run -s "-screen 0 1280x1024x24" ./deploy.sh -m -t

RUN echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc && \
    echo "source /opt/ros/kinetic/setup.sh" >> ~/.bashrc && \
    /bin/bash -c "source ~/.bashrc"

RUN wget -P /tmp/ https://bitbucket.org/osrf/gazebo_models/get/default.tar.gz &&\
    mkdir -p $HOME/.gazebo/models &&\
    sudo tar -xvf /tmp/default.tar.gz -C $HOME/.gazebo/models --strip 1 &&\
    rm /tmp/default.tar.gz && \
    sudo chown -R docker:docker $HOME/.gazebo/models

WORKDIR $GZWEB_WS

CMD gzserver --verbose & npm start
