FROM continuumio/miniconda3

RUN conda config --add channels  conda-forge
RUN conda install python==3.6.5
RUN conda install -y rdkit==2018.03.1.0 flask=0.12.2 flask-cors=3.0.3
RUN pip install scikit-learn==0.21.3 gunicorn==19.7.1 dash pandas

COPY . ./
CMD gunicorn website.app:app -b :8050

EXPOSE 8050