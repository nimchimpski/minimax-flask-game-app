#!/bin/bash


sudo systemctl restart ttt
sudo systemctl enable ttt
sudo systemctl status ttt
sudo systemctl reload nginx

# make it executable with:
# chmod +x restart-ttt.sh