FROM python:3.11-slim
RUN pip install --no-cache-dir flask watchdog
WORKDIR /app
COPY . .
EXPOSE 1337
CMD ["python", "organize_isos.py"]