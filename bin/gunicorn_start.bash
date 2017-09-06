#!/bin/bash

NAME="PairGo_API"
DJANGODIR=~/workplace/pairgo_back
SOCKFILE=~/workplace/pairgo_back/run/gunicorn.sock
USER=deploy
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=pairgo_rest.settings
DJANGO_WSGI_MODULE=pairgo_rest.wsgi

echo "Starting $NAME as `whoami`"

#activate virtualenv
cd ~/workplace/pairgo
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#create run dict if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

#Start your django unicorn
#programs meant to be run under supervisor not damon
exec  ~/workplace/pairgo/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
	--name $NAME \
	--workers $NUM_WORKERS \
	--user=$USER \
	--bind=unix:$SOCKFILE \
	--log-level=debug \
	--log-file=-
