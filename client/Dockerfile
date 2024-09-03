# Using a node base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package.json y yarn.lock
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

# Instalar específicamente el módulo de Rollup para Linux
RUN yarn add --optional @rollup/rollup-linux-x64-gnu

# Limpiar caché y reconstruir
RUN yarn cache clean

# Copy the rest of the application
COPY . .

# Expose the port used by Vite
EXPOSE 5173

# Command to start the application
CMD ["yarn", "dev"]
