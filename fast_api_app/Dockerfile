FROM python:3.12.5

WORKDIR /backend

COPY . /backend

RUN pip install --no-cache-dir -r req.txt

EXPOSE 8945

# Run uvicorn server
CMD ["/bin/sh", "uvicorn_run.sh"]