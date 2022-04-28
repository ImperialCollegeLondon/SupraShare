FROM mambaorg/micromamba:0.23.0

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -f /tmp/environment.yml && \
    micromamba clean --all --yes

COPY . ./

CMD gunicorn website.app:app -b :8050
EXPOSE 8050
