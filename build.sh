#!/bin/bash

wget http://archive.ubuntu.com/ubuntu/pool/main/p/pango1.0/libpango-1.0-0_1.51.0+ds-2_amd64.deb
dpkg-deb -xv libpango-1.0-0_1.51.0+ds-2_amd64.deb ~/local/
echo 'export LD_LIBRARY_PATH=$HOME/local/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
streamlit run streamlit_app.py
