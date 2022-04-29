FROM continuumio/miniconda3

RUN conda update conda
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new env
SHELL ["conda", "run", "-n", "suprashare", "/bin/bash", "-c"]

COPY . ./

CMD gunicorn website.app:server -b :8050
EXPOSE 8050
