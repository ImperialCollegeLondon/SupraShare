#FROM anaconda/miniconda
FROM python:3.12-slim

WORKDIR /usr/src/app

#RUN conda update conda
#COPY environment.yml .
COPY requirements.txt .
# needs by parmed to compile a c++ extension
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libxrender1 libxext6 libexpat1\
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
#RUN conda env create -f environment.yml

#COPY . /usr/src/app

#WORKDIR /usr/src/app

COPY . .

#CMD /opt/conda/envs/suprashare/bin/gunicorn website.app:server -b :8050
CMD ["gunicorn", "website.app:server", "-b", "0.0.0.0:8050"]
EXPOSE 8050
