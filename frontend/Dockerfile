FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Копируем с правильным путём
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Указываем правильный порт для Nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
