import random
import string
import requests
import base64
import hashlib
import os
import urllib.parse
import subprocess
from datetime import datetime

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

try:
    import pyfiglet
    HAS_PYFIGLET = True
except ImportError:
    HAS_PYFIGLET = False

def print_success(text):
    print(f"  >> {text}")

def print_error(text):
    print(f"  >> {text}")

def print_info(text):
    print(f"  >> {text}")

def password_generator(*args):
    if not args:
        length = input("  >> Enter password length (default 16): ").strip()
        length = int(length) if length else 16
    else:
        try:
            length = int(args[0])
        except ValueError:
            print_error("Invalid length, using 16.")
            length = 16
    
    if length < 4: length = 4
    if length > 128: length = 128
    
    use_upper = input("  >> Include uppercase letters? (y/n, default y): ").strip().lower() != 'n'
    use_lower = input("  >> Include lowercase letters? (y/n, default y): ").strip().lower() != 'n'
    use_digits = input("  >> Include numbers? (y/n, default y): ").strip().lower() != 'n'
    use_special = input("  >> Include special characters? (y/n, default y): ").strip().lower() != 'n'
    
    count_input = input("  >> Number of passwords to generate (default 5): ").strip()
    try:
        count = int(count_input) if count_input else 5
        if count < 1: count = 1
        if count > 50: count = 50
    except:
        count = 5
    
    chars = ""
    if use_upper: chars += string.ascii_uppercase
    if use_lower: chars += string.ascii_lowercase
    if use_digits: chars += string.digits
    if use_special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        print_error("No character types selected!")
        return
    
    for i in range(count):
        password = ''.join(random.choice(chars) for _ in range(length))
        strength = "Weak" if length < 8 else ("Medium" if length < 12 else "Strong")
        print_success(f"Password {i+1}: {password}  ({strength})")

def url_shortener(*args):
    if not args:
        url = input("  >> Enter URL to shorten: ").strip()
    else:
        url = args[0]
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print_info("Shortening URL...")
    try:
        response = requests.get('https://tinyurl.com/api-create.php', params={'url': url}, timeout=10)
        if response.status_code == 200:
            short_url = response.text.strip()
            if short_url and 'error' not in short_url.lower():
                print_success("URL shortened successfully!")
                print_info(f"Original: {url}")
                print_info(f"Shortened: {short_url}")
            else:
                print_error("Failed to shorten URL")
        else:
            print_error(f"Failed to shorten URL. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Error: {e}")

def base64_tool(*args):
    print_info("1. Encode")
    print_info("2. Decode")
    choice = input("  >> Select option (1-2): ").strip()
    text = input("  >> Enter text: ").strip()
    if not text:
        print_error("No text entered")
        return
    try:
        if choice == '1':
            encoded = base64.b64encode(text.encode()).decode()
            print_success(f"Encoded: {encoded}")
        elif choice == '2':
            decoded = base64.b64decode(text).decode()
            print_success(f"Decoded: {decoded}")
        else:
            print_error("Invalid option")
    except Exception as e:
        print_error(f"Error: {e}")

def file_hasher(*args):
    filepath = input("  >> Enter file path: ").strip()
    if not filepath:
        print_error("No file path entered")
        return
    if not os.path.exists(filepath):
        print_error("File not found")
        return
    
    print_info("Calculating hashes...")
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        print_info(f"File: {os.path.basename(filepath)}")
        print_info(f"Size: {os.path.getsize(filepath):,} bytes")
        print_info(f"MD5: {hashlib.md5(data).hexdigest()}")
        print_info(f"SHA1: {hashlib.sha1(data).hexdigest()}")
        print_info(f"SHA256: {hashlib.sha256(data).hexdigest()}")
    except Exception as e:
        print_error(f"Error: {e}")

def qr_generator(*args):
    if not HAS_QRCODE:
        print_error("qrcode module not installed. Run: pip install qrcode pillow")
        return
    data = input("  >> Enter text or URL: ").strip()
    if not data:
        print_error("No input provided")
        return
    filename = input("  >> Filename (default: qr_code.png): ").strip()
    if not filename:
        filename = "qr_code.png"
    if not filename.endswith('.png'):
        filename += '.png'
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print_success(f"QR Code saved to {filename}")
        print_info(f"Scan the QR code to access: {data}")
    except Exception as e:
        print_error(f"Error generating QR code: {e}")

def ascii_art(*args):
    if not HAS_PYFIGLET:
        print_error("pyfiglet module not installed. Run: pip install pyfiglet")
        return
    text = input("  >> Enter text to convert: ").strip()
    if not text:
        print_error("No text entered")
        return
    fonts = ['standard', 'slant', 'bubble', 'digital', 'block', 'script', 'cyberlarge']
    print_info(f"Available fonts: {', '.join(fonts)}")
    font = input("  >> Font (default: standard): ").strip()
    if not font: font = 'standard'
    if font not in fonts: font = 'standard'
    try:
        figlet = pyfiglet.Figlet(font=font)
        ascii_art = figlet.renderText(text)
        print(f"\n{ascii_art}")
    except Exception as e:
        print_error(f"Error generating ASCII art: {e}")

def unit_converter(*args):
    def convert_length(value, from_unit, to_unit):
        units = {'mm':0.001,'cm':0.01,'m':1.0,'km':1000.0,'in':0.0254,'ft':0.3048,'yd':0.9144,'mi':1609.344}
        if from_unit not in units or to_unit not in units: return None
        meters = value * units[from_unit]
        return meters / units[to_unit]

    def convert_weight(value, from_unit, to_unit):
        units = {'mg':0.000001,'g':0.001,'kg':1.0,'t':1000.0,'oz':0.0283495,'lb':0.453592}
        if from_unit not in units or to_unit not in units: return None
        kg = value * units[from_unit]
        return kg / units[to_unit]

    def convert_temperature(value, from_unit, to_unit):
        if from_unit == to_unit: return value
        if from_unit == 'C': celsius = value
        elif from_unit == 'F': celsius = (value - 32) * 5 / 9
        elif from_unit == 'K': celsius = value - 273.15
        else: return None
        if to_unit == 'C': return celsius
        elif to_unit == 'F': return celsius * 9 / 5 + 32
        elif to_unit == 'K': return celsius + 273.15
        return None

    def convert_volume(value, from_unit, to_unit):
        units = {'ml':0.001,'l':1.0,'gal':3.78541,'qt':0.946353,'pt':0.473176,'cup':0.236588,'floz':0.0295735}
        if from_unit not in units or to_unit not in units: return None
        liters = value * units[from_unit]
        return liters / units[to_unit]
    
    print_info("1. Length (mm, cm, m, km, in, ft, yd, mi)")
    print_info("2. Weight (mg, g, kg, t, oz, lb)")
    print_info("3. Temperature (C, F, K)")
    print_info("4. Volume (ml, l, gal, qt, pt, cup, floz)")
    category = input("  >> Select category (1-4): ").strip()
    
    if category == '1':
        units = ['mm','cm','m','km','in','ft','yd','mi']
        converter = convert_length
        unit_name = "Length"
    elif category == '2':
        units = ['mg','g','kg','t','oz','lb']
        converter = convert_weight
        unit_name = "Weight"
    elif category == '3':
        units = ['C','F','K']
        converter = convert_temperature
        unit_name = "Temperature"
    elif category == '4':
        units = ['ml','l','gal','qt','pt','cup','floz']
        converter = convert_volume
        unit_name = "Volume"
    else:
        print_error("Invalid category")
        return
    
    print_info(f"Available {unit_name} units: {', '.join(units)}")
    from_unit = input("  >> From unit: ").strip().lower()
    if from_unit not in units:
        print_error("Invalid unit")
        return
    to_unit = input("  >> To unit: ").strip().lower()
    if to_unit not in units:
        print_error("Invalid unit")
        return
    value_input = input("  >> Enter value to convert: ").strip()
    try:
        value = float(value_input)
    except:
        print_error("Invalid number")
        return
    result = converter(value, from_unit, to_unit)
    if result is None:
        print_error("Conversion failed")
    else:
        print_success(f"{value} {from_unit} = {result:.6f} {to_unit}")

def ai_image_generator(*args):
    prompt = input("  >> Enter image description/prompt: ").strip()
    if not prompt:
        print_error("No prompt entered")
        return
    width = input("  >> Width (default 512): ").strip()
    width = int(width) if width.isdigit() else 512
    height = input("  >> Height (default 512): ").strip()
    height = int(height) if height.isdigit() else 512
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
    print_info("Generating image...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filename = input("  >> Filename (default: ai_image.png): ").strip()
            if not filename: filename = "ai_image.png"
            if not filename.endswith(('.png','.jpg','.jpeg')): filename += '.png'
            with open(filename, 'wb') as f:
                f.write(response.content)
            print_success(f"Image saved to {filename}")
            print_info(f"Prompt: {prompt}")
            print_info(f"Size: {width}x{height}")
        else:
            print_error(f"Failed to generate image. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Error: {e}")

def ping_traceroute(*args):
    print_info("1. Ping")
    print_info("2. Traceroute")
    choice = input("  >> Select option (1-2): ").strip()
    if choice not in ['1', '2']:
        print_error("Invalid option")
        return
    target = input("  >> Enter IP or domain: ").strip()
    if not target:
        print_error("No target entered")
        return
    if choice == '1':
        print_info(f"Pinging {target}...")
        param = '-n' if os.name == 'nt' else '-c'
        cmd = ['ping', param, '4', target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            print(result.stdout)
            if result.stderr:
                print_error(result.stderr)
        except subprocess.TimeoutExpired:
            print_error("Ping timed out")
        except Exception as e:
            print_error(f"Error: {e}")
    else:
        print_info(f"Tracing route to {target}...")
        cmd = ['tracert' if os.name == 'nt' else 'traceroute', target]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            print(result.stdout)
            if result.stderr:
                print_error(result.stderr)
        except subprocess.TimeoutExpired:
            print_error("Traceroute timed out")
        except Exception as e:
            print_error(f"Error: {e}")

def download_manager(*args):
    url = input("  >> Enter file URL: ").strip()
    if not url:
        print_error("No URL entered")
        return
    filename = input("  >> Save as (default: downloaded_file): ").strip()
    if not filename:
        filename = "downloaded_file"
    print_info("Downloading...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        total_size = int(response.headers.get('content-length', 0))
        with open(filename, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        progress_bar(int(percent), 100, prefix="Downloading")
        print(f"\n\n")
        print_success(f"Downloaded: {filename}")
        print_info(f"Size: {downloaded:,} bytes")
    except Exception as e:
        print_error(f"Error: {e}")

def system_optimizer(*args):
    print_warning("This will clear system caches")
    print_info("Optimizations:")
    print_info("  - Clear DNS cache")
    print_info("  - Clear Windows Temp")
    print_info("  - Clear Windows Prefetch")
    print_info("  - Clear System Logs")
    confirm = input("  >> Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Operation cancelled")
        return
    print_info("Optimizing system...")
    if os.name == 'nt':
        subprocess.run('ipconfig /flushdns', shell=True, capture_output=True)
        print_success("DNS cache cleared")
        os.system('del /f /s /q "%TEMP%\\*.*" >nul 2>&1')
        os.system('del /f /s /q "%WINDIR%\\Temp\\*.*" >nul 2>&1')
        print_success("Temp files cleared")
        os.system('del /f /s /q "%WINDIR%\\Prefetch\\*.*" >nul 2>&1')
        print_success("Prefetch cleared")
    else:
        subprocess.run('sudo dscacheutil -flushcache', shell=True, capture_output=True)
        print_success("DNS cache cleared")
    print_success("System optimization complete!")

def disk_analyzer(*args):
    try:
        import psutil
        HAS_PSUTIL = True
    except ImportError:
        HAS_PSUTIL = False
    
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    
    path = input("  >> Enter directory path (default: C:\\ or /): ").strip()
    if not path:
        path = 'C:\\' if os.name == 'nt' else '/'
    if not os.path.exists(path):
        print_error("Path not found")
        return
    print_info(f"Analyzing {path}...")
    try:
        usage = psutil.disk_usage(path)
        total = usage.total
        used = usage.used
        free = usage.free
        percent = usage.percent
        print_info(f"Total Space: {total / (1024**3):.2f} GB")
        print_info(f"Used Space: {used / (1024**3):.2f} GB ({percent}%)")
        print_info(f"Free Space: {free / (1024**3):.2f} GB")
        print_info("Top 10 largest folders:")
        folders = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                try:
                    size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(item_path) for filename in filenames)
                    folders.append((item, size))
                except:
                    pass
        folders.sort(key=lambda x: x[1], reverse=True)
        for i, (name, size) in enumerate(folders[:10], 1):
            if size > 0:
                print_info(f"  {i}. {name} - {size / (1024**2):.2f} MB")
    except Exception as e:
        print_error(f"Error: {e}")

def process_manager(*args):
    try:
        import psutil
        HAS_PSUTIL = True
    except ImportError:
        HAS_PSUTIL = False
    
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    
    print_info("1. List all processes")
    print_info("2. Kill a process")
    print_info("3. Check system resources")
    choice = input("  >> Select option (1-3): ").strip()
    if choice == '1':
        print_info("PID  Name                            CPU%  Memory (MB)")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'][:30]
                cpu = proc.info['cpu_percent']
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                print(f"  {pid:<8} {name:<30} {cpu:<8.1f} {mem:<.1f}")
            except:
                pass
    elif choice == '2':
        pid = input("  >> Enter PID to kill: ").strip()
        if not pid:
            print_error("No PID entered")
            return
        try:
            proc = psutil.Process(int(pid))
            confirm = input(f"  >> Kill {proc.name()} (PID: {pid})? (y/n): ").strip().lower()
            if confirm == 'y':
                proc.kill()
                print_success("Process killed")
        except Exception as e:
            print_error(f"Error: {e}")
    elif choice == '3':
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        print_info(f"CPU Usage: {cpu_percent}%")
        print_info(f"RAM Usage: {mem.percent}% ({mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB)")
    else:
        print_error("Invalid option")

def network_scanner(*args):
    try:
        import psutil
        HAS_PSUTIL = True
    except ImportError:
        HAS_PSUTIL = False
    
    print_info("Scanning local network for active devices...")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
        print_info(f"Local IP: {local_ip}")
        print_info(f"Network: {network}.0/24")
        found_devices = []
        for i in range(1, 255):
            ip = f"{network}.{i}"
            try:
                param = '-n' if os.name == 'nt' else '-c'
                cmd = ['ping', param, '1', '-w', '1000', ip]
                result = subprocess.run(cmd, capture_output=True, timeout=2)
                if result.returncode == 0:
                    try:
                        host = socket.gethostbyaddr(ip)[0]
                    except:
                        host = "Unknown"
                    found_devices.append((ip, host))
                    print_success(f"{ip} - {host}")
            except:
                pass
            if i % 10 == 0:
                progress_bar(i, 254, prefix="Scanning")
        print(f"\n")
        print_success(f"Found {len(found_devices)} active devices")
    except Exception as e:
        print_error(f"Error: {e}")

def progress_bar(current, total, width=25, prefix=""):
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r  {prefix:<10} [{bar}] {percentage:5.1f}%  {current}/{total}", end="", flush=True)
    if current == total:
        print()

commands = {
    "password_generator": {"func": password_generator, "description": "Generate strong random passwords", "usage": "password_generator [length]"},
    "url_shortener": {"func": url_shortener, "description": "Shorten a URL", "usage": "url_shortener <url>"},
    "base64_tool": {"func": base64_tool, "description": "Encode or decode Base64 strings", "usage": "base64_tool"},
    "file_hasher": {"func": file_hasher, "description": "Calculate file hashes (MD5, SHA1, SHA256)", "usage": "file_hasher"},
    "qr_generator": {"func": qr_generator, "description": "Generate QR code from text or URL", "usage": "qr_generator"},
    "ascii_art": {"func": ascii_art, "description": "Convert text to ASCII art", "usage": "ascii_art"},
    "unit_converter": {"func": unit_converter, "description": "Convert between different units", "usage": "unit_converter"},
    "ai_image_generator": {"func": ai_image_generator, "description": "Generate AI images from text prompts", "usage": "ai_image_generator"},
    "ping_traceroute": {"func": ping_traceroute, "description": "Ping or traceroute to a target", "usage": "ping_traceroute"},
    "download_manager": {"func": download_manager, "description": "Download files with progress bar", "usage": "download_manager"},
    "system_optimizer": {"func": system_optimizer, "description": "Clear system caches and optimize", "usage": "system_optimizer"},
    "disk_analyzer": {"func": disk_analyzer, "description": "Analyze disk usage by folder", "usage": "disk_analyzer"},
    "process_manager": {"func": process_manager, "description": "View and manage running processes", "usage": "process_manager"},
    "network_scanner": {"func": network_scanner, "description": "Scan local network for active devices", "usage": "network_scanner"}
}