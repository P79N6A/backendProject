#!/bin/sh

export PATH=/usr/local/app/node8/bin:$PATH
export LOG=/usr/local/app/nb/log
export APP_PATH=/usr/local/app/nb
export PID=$APP_PATH/forever.pid
export APP=$APP_PATH/app.js

start() {
    forever -p $APP_PATH -l $LOG/access.log -e $LOG/error.log -o $LOG/out.log -a --pidFile $PID start --killSignal=SIGTERM $APP
    retval=$?
    echo
    return $retval
}
stop() {
    forever stop $APP
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
