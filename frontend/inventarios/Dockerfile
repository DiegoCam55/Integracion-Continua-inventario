 
FROM node:22 AS frontend

WORKDIR /app

# Copiar solo los archivos necesarios
COPY package*.json ./

RUN npm install -g @angular/cli@latest
RUN npm install

# Copiar el resto del proyecto Angular
COPY . .

EXPOSE 4200

CMD ["npm", "start"]
