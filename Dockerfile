# Using multi-stage build to separate the juypternotebook and the GUI stuff
# see<https://docs.docker.com/build/building/multi-stage/>
# Using slim because the spec required python 3.13.* agh.
FROM python:3.13-slim AS ml

# Based on the spec, we need tensorflow 2.20 and the following
# imports. This should mimic uni servers
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "tensorflow[and-cuda]==2.20.*" \
    ipython \
    jupyter \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    pillow \
    scikit-learn

# Create a non-root user with UID 1000 and a real home directory
RUN useradd -m -u 1000 -s /bin/bash mluser

WORKDIR /workspace
CMD ["bash"]


# Interactive.py needs the machine learning stuff so we will
# grab that form that image and then add the rest of the stuff 
FROM ml AS gui

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# python3-tk is for grabimage.py
# Currently unsure what the interactive.py uses, so,
# these might be required:
#   libgl1 \
#   libglib2.0-0 \
#   libxext6 \
#   libsm6 \
#   libxrender1 \
# pyscreenshot is needed for garbimage.py
# scrot is needed for the screenshot that pyscreenshot runs
RUN apt-get update && apt-get install -y \
    python3-tk \
    scrot \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pyscreenshot


WORKDIR /workspace
CMD ["bash"]

# TODO(shenukp1) Nov 11, 2026: possible add this information to the readme later