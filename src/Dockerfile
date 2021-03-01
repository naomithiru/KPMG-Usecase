FROM ubuntu:latest

# Install reqs
RUN apt-get update -y \
	&& apt-get install -y python3-dev python3-pip \
	tesseract-ocr tesseract-ocr-fra tesseract-ocr-nld \
	&& rm -rf /var/lib/apt/lists/*


# integrate only necessary files
RUN mkdir app
RUN mkdir app/templates

COPY src/templates /app/templates
COPY src/*.py /app/
COPY src/Procfile /app
COPY docker_requirements.txt /app

WORKDIR /app
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r docker_requirements.txt
#RUN pip3 install torch==1.7.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

# files paths in py scripts will be parsed relative to WORKDIR (KPMG-Usecase folder)
WORKDIR /

CMD python3 app/app.py