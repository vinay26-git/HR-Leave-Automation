FROM python:3.10-slim

WORKDIR /app

COPY "Backend/Daily_Aprovels/requirements.txt" .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
