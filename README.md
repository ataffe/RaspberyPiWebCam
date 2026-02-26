# RaspberyPiWebCam

Repository for the medium article "Building a Low-Cost, Real-Time, Wireless Wi-Fi Cam with Python, WebRTC, and a Raspberry Pi"

## Running the example
### Streamer.py
```bash
python streamer.py --signaling tcp-socket --signaling-host 0.0.0.0 --signaling-port 8008
```

### Receiver.py
Assuming the raspberry pi ip address is: 10.0.0.5
```bash
python streamer.py --signaling tcp-socket --signaling-host 10.0.0.5 --signaling-port 8008
```