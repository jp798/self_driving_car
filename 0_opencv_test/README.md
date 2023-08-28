##### 접속할 경우

ssh-keygen -R 172.30.1.42 (이미 등록된 IP를 삭제할 때)
ssh pi@192.168.0.12 (SSH 연결)

#### SD 이미지 백업

diskutil list
sudo dd if=/dev/disk2(원본) of=farm.img(복사할 이미지) bs= 10240 conv=sync
sudo dd if=/dev/diskn of=~/Desktop/raspberry-pi-backup.img bs=1m

###### computer vision 설치

sudo apt-get update
sudo apt-get install python3-opencv
sudo apt-get install python3-picamera

pip3 install numpy

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

sudo npm install -g --unsafe-perm node-red

### Node-RED 실행

node-red -p 1881
node-red --safe

#### Node-RED 재실행

sudo systemctl enable node-red
sudo systemctl start node-red

sudo systemctl stop node-red
sudo systemctl restart node-red
sudo systemctl status node-red
