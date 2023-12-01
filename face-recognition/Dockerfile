ARG FUNCTION_DIR="/home/app/"
ARG PYTHON_VERSION=3.8
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

FROM --platform=${TARGETPLATFORM:-linux/amd64} python:${PYTHON_VERSION}-alpine as build-image

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

COPY requirements.txt .

# Install build dependencies
RUN apk --no-cache add build-base python3-dev

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --target "/home/app/"

FROM ubuntu:20.04

ARG FUNCTION_DIR
# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y cmake ca-certificates libgl1-mesa-glx ffmpeg

# Copy built dependencies from the build-image stage
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Copy the watchdog binary
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

# Create a non-root user
RUN addgroup -S app && adduser app -S -G app \
    && chown -R app:app /home/app

USER app
WORKDIR /home/app
COPY .env .

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
