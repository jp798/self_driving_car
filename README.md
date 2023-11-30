ssh pi@192.168.0.12 (SSH 연결)

### config (Raspberry Pi - FTP connection Config )

[
	{
		"name": "raspbot",
		"host": "192.168.0.13",
		"port": 22,
		"type": "sftp",
		"username": "pi",
		"password": "1234",
		"path": "/home/pi/Desktop",
		"autosave": true,
		"confirm": true
	}
]

####  실행 

python3  1_buzzer_test.py
python3  2_motor_test.py
python3  3_servo_test.py
python3  4_ultrasonic_test.py
python3  5_opencv_camera.py

python3 7_autoplot___test.py


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
