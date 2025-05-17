FROM python:3.13-slim

LABEL authors="ichitunkk"

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY bot.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run bot
CMD ["python", "bot.py"]