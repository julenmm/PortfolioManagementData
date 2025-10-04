FROM apache/superset:latest

USER root
# Create the venv now (the base image makes it at runtime; we do it here so we can pip install at build)
RUN python3 -m venv /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip setuptools wheel

COPY requirements.txt /tmp/requirements.txt
RUN /app/.venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

USER superset
