#!/bin/sh

create_log_file() {
    echo "Creating log file..."
    touch /var/log/cron.log
    chmod 666 /var/log/cron.log
    echo "Log file created at /var/log/cron.log"
}

monitor_logs() {
    echo "=== Monitoring cron logs ==="
    tail -f /var/log/cron.log
}

run_cron() {
    echo "=== Starting cron daemon ==="
    exec cron -f
}

# cron pornește sarcinile cu un mediu gol; salvăm variabilele containerului
# (API_KEY, API_URL, TZ) în /etc/environment ca să le vadă și sarcinile cron
env > /etc/environment
create_log_file
monitor_logs &
run_cron
