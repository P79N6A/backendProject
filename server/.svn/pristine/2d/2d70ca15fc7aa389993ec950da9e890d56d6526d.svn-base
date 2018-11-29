#!/bin/sh

export LOG=/data/logs/voice
export APP_PATH=/usr/local/app/vs
export APP=$APP_PATH/app.py

start() {
    nohup /usr/bin/python $APP --port={PORT} --host=0.0.0.0 1>>$LOG/out.log 2>>$LOG/out.log &
    retval=$?
    echo
    return $retval
}
stop() {
    kill -9 $(ps aux | grep 'app.py' | grep -v grep | awk '{print $2}')
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
