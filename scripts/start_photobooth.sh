
#!/bin/bash

echo "Prepare enviroment"

xset s off
xset -dpms
xset s noblank

echo "Start Photobooth..."

# the use of sudo is necessary for connecting to a network
sudo python photobooth_script.py

echo "Shutdown Photobooth..."

echo "recover enviroment"
xset s on
xset +dpms