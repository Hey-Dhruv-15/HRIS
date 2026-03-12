FROM apache/spark:3.5.3-java17
USER root
ENV HOME=/root
ENV PIP_CACHE_DIR=/tmp/pip-cache
RUN python3 -m pip install --no-cache-dir pandas scikit-learn
USER root
