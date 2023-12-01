ARG FUNCTION_DIR="/home/app/"
ARG PYTHON_VERSION=3.8
FROM ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

FROM python:${PYTHON_VERSION} AS python-alpine

ARG PYTHON_VERSION

# Install build dependencies
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx

RUN python${PYTHON_VERSION} -m pip install --upgrade pip


FROM ubuntu:22.04

ARG FUNCTION_DIR
ARG PYTHON_VERSION
# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy built dependencies from the python-alpine stage
COPY --from=python-alpine ${FUNCTION_DIR} ${FUNCTION_DIR}

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx \

RUN apt-get install -y ffmpeg

COPY requirements.txt ${FUNCTION_DIR}
RUN python${PYTHON_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}

# Copy the watchdog binary
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Create a non-root user
RUN addgroup -S app && adduser app -S -G app \
    && chown -R app:app /home/app

USER app
WORKDIR /home/app
COPY .env .
COPY handler.py ${FUNCTION_DIR}

# Set environment variables
ENV fprocess="xargs python3 handler.py"
ENV write_debug="true"

# Expose ports
EXPOSE 8080
EXPOSE 6969

# Healthcheck
HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

# Command to run the watchdog
CMD ["fwatchdog"]
