FROM nginx:stable-alpine3.24-slim

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html app.js /usr/share/nginx/html/

USER 1002
EXPOSE 8080
