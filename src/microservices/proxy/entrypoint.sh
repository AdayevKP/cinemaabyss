#!/bin/sh

if [ "$GRADUAL_MIGRATION" = "false" ]; then
    MOVIES_DOWN=down
    MOVIES_WEIGHT=1
    MONOLITH_WEIGTH=1
elif [ ${MOVIES_MIGRATION_PERCENT} -eq 100 ]; then
    MONOLITH_DOWN=down
    MOVIES_WEIGHT=1
    MONOLITH_WEIGTH=1
else
    MOVIES_WEIGHT=${MOVIES_MIGRATION_PERCENT}
    MONOLITH_WEIGTH=$((100 - ${MOVIES_MIGRATION_PERCENT:-50}))
    MOVIES_DOWN=''
fi

export MONOLITH_DOWN
export MOVIES_DOWN
export MOVIES_WEIGHT
export MONOLITH_WEIGTH

eval "envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp && mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"
