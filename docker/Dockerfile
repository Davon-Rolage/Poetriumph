# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim
# Identify the maintainer of an image
LABEL maintainer="davon.rolage@gmail.com"
LABEL description="Django image for newA.fun"
LABEL version="1.0"

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Copy and run the worker
COPY ./docker/worker-entrypoint.sh /app
RUN chmod +x /app/worker-entrypoint.sh
ENTRYPOINT ["/app/worker-entrypoint.sh"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "poetriumph.wsgi"]
