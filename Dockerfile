#base image
FROM python:3.14.2
#workdir
WORKDIR /app
#copy
COPY . /app
#run
RUN pip install -r requirements.txt
#port
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]