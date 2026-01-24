FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh app/entrypoint.sh

RUN mkdir -p /var/log/nginx/proxy

ENV GRADUAL_MIGRATION=true
ENV MOVIES_MIGRATION_PERCENT=50
ENV MOVIES_SERVICE_URL=movies-service:8081
ENV MONOLITH_URL=monolith:8080

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]