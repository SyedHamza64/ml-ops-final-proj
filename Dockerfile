# Dockerfile

# 1. Pick a base image
FROM python:3.9-slim

# 2. Set your working directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your code
COPY . .

# 5. Define the default command (replace with your entrypoint)
CMD ["python", "src/main.py"]
