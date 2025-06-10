FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda install -n base -c conda-forge mamba && \
    mamba env update -n base -f environment.yml && \
    conda clean --all --yes

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi_entry:application"]

