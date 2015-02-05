#!/bin/sh

cd /root/static && exec /sbin/setuser app python3 -m http.server 8001
