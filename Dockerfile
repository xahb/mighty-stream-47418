FROM python:3
ADD clahelpbot.py .
ADD sql_queries.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD python3 ./clahelpbot.py