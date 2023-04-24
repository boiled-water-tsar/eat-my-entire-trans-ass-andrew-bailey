FROM python:3.11-alpine

RUN addgroup app && adduser -DG app app
USER app
ENV PATH /home/app/.local/bin:$PATH

WORKDIR /code
COPY . /code

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "-u", "defend_trans.py"]
