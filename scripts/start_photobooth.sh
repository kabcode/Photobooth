
#!/bin/bash

echo "Prepare enviroment"

xset s off
xset -dpms
xset s noblank

echo "Start Photobooth..."

python photobooth_script.py

echo "Shutdown Photobooth..."

echo "recover enviroment"
xset s on
xset +dpms