from flask import Flask, request, render_template_string, session, redirect, url_for
import os
import zipfile
from datetime import datetime
import qrcode
import socket
import random
import string

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Tambah ini
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Template HTML yang menarik
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱➡️💻 File Transfer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px 20px;
            margin: 30px 0;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: rgba(102, 126, 234, 0.05);
            transform: translateY(-2px);
        }

        .upload-area.dragover {
            border-color: #764ba2;
            background: rgba(102, 126, 234, 0.1);
            transform: scale(1.02);
        }

        .upload-icon {
            font-size: 4em;
            color: #667eea;
            margin-bottom: 20px;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        .file-input {
            display: none;
        }

        .upload-text {
            color: #333;
            font-size: 1.2em;
            font-weight: 500;
            margin-bottom: 10px;
        }

        .upload-hint {
            color: #666;
            font-size: 0.9em;
        }

        .file-info {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            display: none;
        }

        .file-info.show {
            display: block;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .upload-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            margin-top: 20px;
        }

        .upload-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        .upload-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background: #e9ecef;
            border-radius: 3px;
            margin: 20px 0;
            overflow: hidden;
            display: none;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
        }

        .success-message {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .footer {
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .container {
                padding: 30px 20px;
                margin: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .upload-area {
                padding: 30px 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱➡️💻</h1>
            <p>Transfer Fail dari Telefon ke PC</p>
        </div>

        <form id="uploadForm" method="POST" action="/upload" enctype="multipart/form-data">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📁</div>
                <div class="upload-text">Klik atau seret fail ke sini</div>
                <div class="upload-hint">Semua jenis fail diterima</div>
                <input type="file" id="fileInput" name="file" class="file-input" required>
            </div>

            <div class="file-info" id="fileInfo">
                <strong>Fail dipilih:</strong>
                <div id="fileName"></div>
                <div id="fileSize"></div>
            </div>

            <div class="progress-bar" id="progressBar">
                <div class="progress-fill" id="progressFill"></div>
            </div>

            <button type="submit" class="upload-btn" id="uploadBtn">
                🚀 Muat Naik Fail
            </button>
        </form>

        <div class="success-message" id="successMessage"></div>

        <div class="footer">
            <p>✨ Fail akan automatik di-zip dan disimpan dengan timestamp</p>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const uploadBtn = document.getElementById('uploadBtn');
        const uploadForm = document.getElementById('uploadForm');
        const progressBar = document.getElementById('progressBar');
        const progressFill = document.getElementById('progressFill');
        const successMessage = document.getElementById('successMessage');

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect();
            }
        });

        // File selection
        fileInput.addEventListener('change', handleFileSelect);

        function handleFileSelect() {
            const file = fileInput.files[0];
            if (file) {
                fileName.textContent = file.name;
                fileSize.textContent = `Saiz: ${formatFileSize(file.size)}`;
                fileInfo.classList.add('show');
                uploadBtn.disabled = false;
                
                // Change upload area appearance
                uploadArea.style.borderColor = '#28a745';
                uploadArea.querySelector('.upload-icon').textContent = '✅';
                uploadArea.querySelector('.upload-text').textContent = 'Fail bersedia untuk dimuat naik!';
            }
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Form submission with progress
        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            if (!fileInput.files[0]) {
                alert('Sila pilih fail terlebih dahulu!');
                return;
            }

            const formData = new FormData(uploadForm);
            
            // Show progress bar
            progressBar.style.display = 'block';
            uploadBtn.disabled = true;
            uploadBtn.textContent = '📤 Sedang memuat naik...';

            // Simulate progress (since we can't track real progress easily with basic Flask)
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                progressFill.style.width = progress + '%';
            }, 100);

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                clearInterval(progressInterval);
                progressFill.style.width = '100%';
                
                setTimeout(() => {
                    progressBar.style.display = 'none';
                    successMessage.textContent = '🎉 ' + data;
                    successMessage.style.display = 'block';
                    
                    // Reset form
                    uploadBtn.textContent = '🚀 Muat Naik Fail Lain';
                    uploadBtn.disabled = false;
                    fileInfo.classList.remove('show');
                    fileInput.value = '';
                    
                    // Reset upload area
                    uploadArea.style.borderColor = '#667eea';
                    uploadArea.querySelector('.upload-icon').textContent = '📁';
                    uploadArea.querySelector('.upload-text').textContent = 'Klik atau seret fail ke sini';
                }, 500);
            })
            .catch(error => {
                clearInterval(progressInterval);
                progressBar.style.display = 'none';
                uploadBtn.disabled = false;
                uploadBtn.textContent = '🚀 Muat Naik Fail';
                alert('Ralat semasa memuat naik: ' + error);
            });
        });
    </script>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - File Transfer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header {
            margin-bottom: 30px;
        }

        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: #666;
            font-size: 1.1em;
        }

        .login-form {
            text-align: center;
            padding: 20px;
        }

        .key-input {
            font-size: 24px;
            letter-spacing: 5px;
            padding: 10px;
            width: 200px;
            text-align: center;
            margin: 20px 0;
        }

        .upload-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            margin-top: 20px;
        }

        .upload-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        .upload-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        @media (max-width: 600px) {
            .container {
                padding: 30px 20px;
                margin: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐</h1>
            <p>Masukkan Kod Akses</p>
        </div>
        <form class="login-form" method="POST" action="/verify">
            <input type="text" name="access_key" 
                   class="key-input" maxlength="6" 
                   pattern="[0-9]{6}" required
                   placeholder="000000">
            <button type="submit" class="upload-btn">
                ✅ Sahkan Kod
            </button>
        </form>
    </div>
</body>
</html>
'''

def generate_access_key():
    """Generate 6 digit random key"""
    return ''.join(random.choices(string.digits, k=6))

def get_local_ip():
    try:
        # Dapatkan IP address local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def index():
    if 'verified' not in session:
        return render_template_string(LOGIN_TEMPLATE)
    return render_template_string(HTML_TEMPLATE)

@app.route('/verify', methods=['POST'])
def verify():
    input_key = request.form.get('access_key')
    if input_key == access_key:
        session['verified'] = True
        return redirect(url_for('index'))
    return 'Kod tidak sah! Sila cuba lagi.', 401

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        original_filename = file.filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}.zip"
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.writestr(original_filename, file.read())

        return f'Fail berjaya dimuat naik dan dizip sebagai: {zip_filename}'
    return 'Tiada fail dipilih!'

if __name__ == '__main__':
    access_key = generate_access_key()
    ip_address = get_local_ip()
    server_url = f"http://{ip_address}:5000"
    
    print("🚀 Server bermula di", server_url)
    print("🔐 Kod Akses:", access_key)
    print("📱 Imbas QR code dalam fail 'server_qr.png' untuk akses")
    app.run(host='0.0.0.0', port=5000, debug=True)