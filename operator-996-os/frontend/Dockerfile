# ============================================================
# 🧠 Operator-996 Cognitive OS - Frontend Dockerfile (CRA Version)
# ============================================================

# ---------- Build Stage ----------
FROM node:18-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---------- Nginx Stage ----------
FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from CRA (React)
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

