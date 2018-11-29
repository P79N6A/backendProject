#!/bin/sh

export LOG=/dockerdata/log
export APP_PATH=/usr/local/app/nb
export CONF=$APP_PATH/cfg/gun.conf
export PID=$APP_PATH/gun.pid

start() {
    nohup gunicorn -k gevent -c $CONF --chdir $APP_PATH --pid $PID app:app 1>>$LOG/out.log 2>>$LOG/out.log &
    retval=$?
    echo
    return $retval
}
stop() {
    #kill -9 $(ps aux | grep 'flask' | grep -v grep | awk '{print $2}')
    #killall gunicorn
    kill $(cat $PID)
    retval=$?
    echo
    return $retval
}
restart() {
    stop
    start
}
case "$1" in
    start|stop|restart)
        $1
        ;;
    status)
        status $APP_PATH
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart}"
        exit 2
esac
