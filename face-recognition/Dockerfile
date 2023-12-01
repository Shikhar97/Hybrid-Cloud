ARG FUNCTION_DIR="/home/app/"
ARG PYTHON_VERSION=3.8
FROM ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

FROM ubuntu:20.04

ARG FUNCTION_DIR
ARG PYTHON_VERSION

ENV DEBIAN_FRONTEND=nonintercative
ENV TZ=America/Phoenix
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install build dependencies
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx build-essential net-tools iputils-ping nano

# Update the package lists and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg

WORKDIR ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}
RUN python3 -m pip install -r requirements.txt --target ${FUNCTION_DIR}

# Copy the watchdog binary
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Create a non-root user
RUN groupadd app && useradd -g app -s /bin/sh app && chown -R app:app /home/app

WORKDIR ${FUNCTION_DIR}
COPY .env .
COPY encoding .
COPY handler.py ${FUNCTION_DIR}

USER app
# Set environment variables
ENV fprocess="xargs python3 handler.py"
ENV write_debug="true"

# Expose ports
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

# Command to run the watchdog
CMD ["fwatchdog"]
