FROM python:3.11-slim

# Install necessary packages
RUN pip install --no-cache-dir watchdog flask

# Set the working directory
WORKDIR /app

# Copy the organization script
COPY organize_isos.py ./

# Set environment variable for ISO directory
ENV ISO_DIR=/mnt/user/isos

# Expose port 1337 for the web portal
EXPOSE 1337

# Set the default command
CMD ["python", "organize_isos.py"]
