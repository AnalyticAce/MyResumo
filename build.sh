#!/bin/bash

# Download the package
wget https://files.pythonhosted.org/packages/cc/a7/b832d1366e49db29ba99d93776d1dfff4782abb7ff0a8f29e2ae8e13970d/pangocffi-0.12.0.tar.gz

# Extract the package
tar -xzf pangocffi-0.12.0.tar.gz

# Navigate to the package directory
cd pangocffi-0.12.0

# Create a LICENSE file in the pangocffi.egg-info directory
touch pangocffi.egg-info/LICENSE

# Continue with your existing commands
wget http://archive.ubuntu.com/ubuntu/pool/main/p/pango1.0/libpango-1.0-0_1.51.0+ds-2_amd64.deb
dpkg-deb -xv libpango-1.0-0_1.51.0+ds-2_amd64.deb ~/local/
echo 'export LD_LIBRARY_PATH=$HOME/local/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
streamlit run streamlit_app.py
