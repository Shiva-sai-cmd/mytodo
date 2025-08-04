FROM python:3.11-slim

WORKDIR /app

# Install only necessary system dependencies (no mysqlclient needed)
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY ./backend/ .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Flask/Gunicorn
EXPOSE 5000

# Start using gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
