FROM python:3.10
WORKDIR /app
COPY Requierment.txt .
RUN pip install --no-cache-dir -r Requierment.txt
COPY .. .
EXPOSE 8050
CMD ["python","tp no1.py"]

#Run these commands in terminal:
# docker build -t my_dash_app .
# docker run -p 8050:8050 my_dash_app
