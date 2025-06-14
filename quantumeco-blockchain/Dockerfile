FROM node:18-slim

WORKDIR /app

# Install Python for blockchain interface
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package*.json ./
RUN npm install

# Copy Python requirements
COPY python_interface/requirements.txt ./python_interface/
RUN cd python_interface && python3 -m pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8546

# Start the blockchain service
CMD ["node", "truffle-config.js"]
