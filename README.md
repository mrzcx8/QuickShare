# QuickShare

Simple and secure file transfer system between phone and PC in local network. Transfer your files securely with just a scan and click!

## Features
- 🔐 Secure access with random generated key
- 📱 Easy mobile access via QR code
- 🗂️ Automatic file zipping with timestamp
- 💫 Beautiful and responsive UI
- 🌐 Works in local network

## Installation
1. Clone repository:
```bash
git clone https://github.com/mrzcx8/QuickShare.git
cd file-transfer-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Run server:
```bash
python File_server.py
```
2. Note the access code shown in terminal
3. Scan QR code from your mobile device
4. Enter access code to login
5. Start transferring files!

## Requirements
- Python 3.7+
- Flask
- qrcode
- Local network connection

  ## How to Install

1. Run `setup.bat` to install all dependencies
2. Run `start_server.bat` to start server
3. Scan generated QR code

## How to Use

1. Run `start_server.bat` to start server
2. Note the **Access Code** generated in terminal
3. Scan generated QR code
4. Enter access code on login screen
5. Start transfer failed after confirmation

## Security
- Random access code generated each session
- Session-based authentication
- Local network only
- Automatic file encryption (zip)

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
[MIT](LICENSE)

# QuickShare

Simple and secure file transfer system between phone and PC in local network. Transfer your files securely with just a scan and click!

Created by [Mr.Syah (mrzcx8)](https://github.com/mrzcx8)
