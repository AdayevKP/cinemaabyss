#!/bin/sh

MOVIES_WEIGHT=1
MONOLITH_WEIGTH=1
MOVIES_DOWN=''
MONOLITH_DOWN=''

if [[ "$GRADUAL_MIGRATION" = "false"  || ${MOVIES_MIGRATION_PERCENT} -le 0 ]]; then
    MOVIES_DOWN=down
elif [[ ${MOVIES_MIGRATION_PERCENT} -ge 100 ]]; then
    MONOLITH_DOWN=down
else
    MOVIES_WEIGHT=${MOVIES_MIGRATION_PERCENT}
    MONOLITH_WEIGTH=$((100 - ${MOVIES_MIGRATION_PERCENT:-50}))
fi

export MONOLITH_DOWN
export MOVIES_DOWN
export MOVIES_WEIGHT
export MONOLITH_WEIGTH

eval "envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp && mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"
