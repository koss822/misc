# Specify the base image
FROM node:latest

# Set a working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy all other source code files
COPY . .

# Start the app
CMD ["npm", "run", "prod"]