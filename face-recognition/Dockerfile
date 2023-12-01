ARG FUNCTION_DIR="/home/app/"
ARG PYTHON_VERSION=3.8
FROM ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

FROM ubuntu:22.04

ARG FUNCTION_DIR
ARG PYTHON_VERSION

# Install build dependencies
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx

# Update the package lists and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN python${PYTHON_VERSION} -m pip install --upgrade pip

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg

WORKDIR ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}
RUN python${PYTHON_VERSION} -m pip install -r requirements.txt --target ${FUNCTION_DIR}

# Copy the watchdog binary
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Create a non-root user
RUN addgroup -S app && adduser app -S -G app \
    && chown -R app:app /home/app

WORKDIR ${FUNCTION_DIR}
COPY .env .
COPY handler.py ${FUNCTION_DIR}

USER app
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
