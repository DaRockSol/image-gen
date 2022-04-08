FROM python:buster

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8181

ENTRYPOINT [ "python3" ]

CMD ["stickmanreturns.py"]