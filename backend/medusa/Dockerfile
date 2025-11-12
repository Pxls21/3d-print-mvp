# Medusa.js Backend Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (cache layer)
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Build Medusa
RUN npm run build

# Expose ports
EXPOSE 9000 7001

# Start Medusa
CMD ["npm", "run", "dev"]
