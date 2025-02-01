FROM python:3.11-slim

# Install git and dependencies
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir flask watchdog

# Clone the repo
RUN git clone https://github.com/Sgtsmi1es/iso-organizer.git /app

WORKDIR /app

EXPOSE 1337

CMD ["python", "organize_isos.py"]