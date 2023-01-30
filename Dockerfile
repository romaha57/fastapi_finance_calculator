FROM python

COPY . .

WORKDIR .

EXPOSE 8000

RUN pip install -r requirements.txt


CMD ["python", "main.py"]