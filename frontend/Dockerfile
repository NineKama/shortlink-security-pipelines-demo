FROM nginx:stable-alpine3.24-slim

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html app.js /usr/share/nginx/html/

RUN chown -R 1002 /var/cache/nginx \
 && touch /run/nginx.pid && chown 1002 /run/nginx.pid \
 && sed -i '/^user /d' /etc/nginx/nginx.conf

USER 1002
EXPOSE 8080
