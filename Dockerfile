FROM python:3.11-slim

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js 20 and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy ML service requirements & install Python dependencies
COPY web_app/ml_service/requirements.txt ./web_app/ml_service/
RUN pip install --no-cache-dir -r ./web_app/ml_service/requirements.txt

# Copy package.json files and install Node modules
COPY web_app/server/package*.json ./web_app/server/
COPY web_app/client/package*.json ./web_app/client/
RUN cd web_app/server && npm install
RUN cd web_app/client && npm install

# Copy application source code
COPY . .

# Build React client bundle for production
RUN cd web_app/client && npm run build

# Default environment variables
ENV PORT=10000
ENV NODE_ENV=production
ENV ML_SERVICE_URL=http://127.0.0.1:8000
EXPOSE 10000

# Start both Python ML microservice (127.0.0.1:8000) and Express server (0.0.0.0:$PORT)
CMD ["sh", "-c", "cd /app/web_app/ml_service && python -m uvicorn service:app --host 127.0.0.1 --port 8000 & cd /app/web_app/server && node server.js"]

