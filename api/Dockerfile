FROM python:3.8.13 AS base

# Append /home/app/.local/bin/ to PATH variable because
# gunicorn is installed there.
ENV PYTHONPATH=$PYTHONPATH:/src/
ENV PATH=$PATH:/home/app/.local/bin/

COPY ./ /src

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

FROM base AS build
ENTRYPOINT ["gunicorn", "--workers=8", "--bind", "0.0.0.0:5000", "app:app"]

#FROM base AS test
#RUN ["pytest", "-v", "/src/tests"]