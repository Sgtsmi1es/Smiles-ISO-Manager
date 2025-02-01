FROM python:3.11-slim

# Install necessary packages
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir flask watchdog

# Clone your GitHub repository
RUN git clone https://github.com/Sgtsmi1es/iso-organizer.git /app

# Set the working directory
WORKDIR /app

# Expose the web port
EXPOSE 1337

# Run the application
CMD ["python", "organize_isos.py"]