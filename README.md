ssh pi@192.168.0.12 (SSH 연결)

### config (Raspberry Pi - FTP connection Config )

{
"name": "Raspberry Pi",
"host": "192.168.0.12",
"port": 22,
"type": "sftp",
"username": "pi",
"password": "1234",
"path": "/home/pi/Desktop",
"autosave": true,
"confirm": true
}

### Node-Red

npm install -g --unsafe-perm node-red

### Node-RED 실행

node-red -p 1881
node-red --safe

#### Node-RED 재실행

sudo systemctl enable node-red
sudo systemctl start node-red

sudo systemctl stop node-red
sudo systemctl restart node-red
sudo systemctl status node-red
