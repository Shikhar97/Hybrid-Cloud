## Define global args
#ARG PYTHON_VERSION=3
#FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog
#FROM --platform=${TARGETPLATFORM:-linux/amd64} python:${PYTHON_VERSION}-alpine
#
#ARG TARGETPLATFORM
#ARG BUILDPLATFORM
#
## Allows you to add additional packages via build-arg
#ARG ADDITIONAL_PACKAGE
#
#COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
#RUN chmod +x /usr/bin/fwatchdog
#RUN apk --no-cache add ca-certificates ${ADDITIONAL_PACKAGE}
#
#
## Add non root user
#RUN addgroup -S app && adduser app -S -G app
#
#WORKDIR /home/app/
#
#USER root
#RUN chown -R app /home/app && \
#  mkdir -p /home/app/python && chown -R app /home/app
#USER app
#ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
#ENV PYTHONPATH=$PYTHONPATH:/home/app/python
#
#
#
#WORKDIR /home/app/
#
#USER root
#
## Allow any user-id for OpenShift users.
#RUN chown -R app:app ./ && \
#  chmod -R 777 /home/app/python
#
#USER app
#
#
#
#
#
#
#ARG FUNCTION_DIR="/home/app/"
#ARG RUNTIME_VERSION="3.8"
#ARG DISTRO_VERSION="3.12"
#
## Stage 1 - bundle base image + runtime
## Grab a fresh copy of the image and install GCC
#FROM python:${RUNTIME_VERSION} AS python-alpine
#
#RUN apt-get update \
#    && apt-get install -y cmake ca-certificates libgl1-mesa-glx
#RUN python${RUNTIME_VERSION} -m pip install --upgrade pip
#
#
## Stage 2 - final runtime image
## Grab a fresh copy of the Python image
#FROM python-alpine
## Include global arg in this stage of the build
#ARG FUNCTION_DIR
## Set working directory to function root directory
#WORKDIR ${FUNCTION_DIR}
## Copy in the built dependencies
#COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
#
## Install ffmpeg
#RUN apt-get install -y ffmpeg
#
## Copy handler function
#COPY face-recognition/requirements.txt ${FUNCTION_DIR}
#RUN python${RUNTIME_VERSION} -m pip install --upgrade pip
#RUN python${RUNTIME_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}
#
## Copy function code
#COPY face-recognition/handler.py ${FUNCTION_DIR}
#COPY face-recognition/encoding ${FUNCTION_DIR}
#
#ENV fprocess="xargs python3 handler.py"
#EXPOSE 8080
#
#HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1
#
#CMD ["fwatchdog"]
