# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim
# Identify the maintainer of an image
LABEL maintainer="davon.rolage@gmail.com"
LABEL description="Django image for poetry.newa.fun"
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

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "poetriumph.wsgi"]
