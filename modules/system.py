import os
import platform
import socket
import subprocess
import time
import sys

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def print_success(text):
    print(f"  >> {text}")

def print_error(text):
    print(f"  >> {text}")

def print_info(text):
    print(f"  >> {text}")

def system_info(*args):
    print_info(f"System: {platform.system()} {platform.release()}")
    print_info(f"Version: {platform.version()}")
    print_info(f"Machine: {platform.machine()}")
    print_info(f"Processor: {platform.processor()}")
    print_info(f"Hostname: {socket.gethostname()}")
    print_info(f"Python Version: {platform.python_version()}")
    if HAS_PSUTIL:
        print_info(f"CPU Cores: {psutil.cpu_count(logical=True)} logical, {psutil.cpu_count(logical=False)} physical")
        print_info(f"CPU Usage: {psutil.cpu_percent(interval=0.5)}%")
        mem = psutil.virtual_memory()
        print_info(f"RAM: {mem.total / (1024**3):.2f} GB total, {mem.used / (1024**3):.2f} GB used ({mem.percent}%)")
        disk = psutil.disk_usage('/')
        print_info(f"Disk: {disk.total / (1024**3):.2f} GB total, {disk.used / (1024**3):.2f} GB used ({disk.percent}%)")
    else:
        print_warning("Install 'psutil' for more detailed system info: pip install psutil")

def process_manager(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    sub_cmd = args[0].lower() if args else ""
    if sub_cmd == "list":
        print_info("Running processes (PID, Name, CPU%, Memory%):")
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                print(f"  {info['pid']:<8} {info['name']:<25} {info['cpu_percent']:>5}% {info['memory_percent']:>5}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    elif sub_cmd == "kill":
        if len(args) < 2:
            print_error("Usage: process_manager kill <PID>")
            return
        try:
            pid = int(args[1])
            proc = psutil.Process(pid)
            proc.terminate()
            print_success(f"Terminated process {pid}")
        except Exception as e:
            print_error(f"Failed to kill process: {e}")
    else:
        print_info("Usage: process_manager [list | kill <PID>]")

def network_scanner(*args):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ip_parts = local_ip.split('.')
    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"
    print_info(f"Scanning network {network}.0/24...")
    found = []
    for i in range(1, 255):
        ip = f"{network}.{i}"
        try:
            param = '-n' if os.name == 'nt' else '-c'
            subprocess.run(['ping', param, '1', '-w', '1000', ip], capture_output=True, timeout=2)
            try:
                host = socket.gethostbyaddr(ip)[0]
            except:
                host = "Unknown"
            found.append((ip, host))
            print_success(f"{ip} - {host}")
        except:
            pass
    print_info(f"Found {len(found)} active devices")

def disk_analyzer(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    path = input("  >> Enter directory path (default: /): ").strip()
    if not path:
        path = '/' if os.name != 'nt' else 'C:\\'
    if not os.path.exists(path):
        print_error("Path not found")
        return
    try:
        usage = psutil.disk_usage(path)
        print_info(f"Path: {path}")
        print_info(f"Total: {usage.total / (1024**3):.2f} GB")
        print_info(f"Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
        print_info(f"Free: {usage.free / (1024**3):.2f} GB")
        
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                try:
                    size = sum(os.path.getsize(os.path.join(dirpath, f)) for dirpath, _, files in os.walk(item_path) for f in files)
                    items.append((item, size))
                except:
                    pass
        items.sort(key=lambda x: x[1], reverse=True)
        print_info("Top 10 largest folders:")
        for i, (name, size) in enumerate(items[:10], 1):
            if size > 0:
                print_info(f"  {i}. {name} - {size / (1024**2):.2f} MB")
    except Exception as e:
        print_error(f"Error: {e}")

def resource_monitor(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    print_info("Press Ctrl+C to stop monitoring")
    try:
        while True:
            clear = '\033[2J\033[H' if os.name != 'nt' else ''
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            print(f"{clear}  >> CPU: {cpu}%")
            print(f"  >> RAM: {mem.percent}% ({mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB)")
            print(f"  >> Disk: {disk.percent}% ({disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB)")
            print(f"  >> Processes: {len(psutil.pids())}")
            time.sleep(1)
    except KeyboardInterrupt:
        print_info("Monitoring stopped")

def clear_temp(*args):
    confirm = input("  >> Clear temporary files? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Aborted")
        return
    if os.name == 'nt':
        os.system('del /f /s /q "%TEMP%\\*.*" >nul 2>&1')
        os.system('del /f /s /q "%WINDIR%\\Temp\\*.*" >nul 2>&1')
        print_success("Temporary files cleared")
    else:
        os.system('sudo rm -rf /tmp/* 2>/dev/null')
        print_success("Temporary files cleared")

def battery_info(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    if not hasattr(psutil, 'sensors_battery'):
        print_error("Battery info not available on this system")
        return
    battery = psutil.sensors_battery()
    if battery:
        print_info(f"Charge: {battery.percent}%")
        print_info(f"Charging: {battery.power_plugged}")
        print_info(f"Time left: {battery.secsleft} seconds")
    else:
        print_error("No battery detected")

def network_info(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for interface, addr_list in addrs.items():
        print_info(f"{interface}:")
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                print_info(f"  IPv4: {addr.address}")
            elif addr.family == socket.AF_INET6:
                print_info(f"  IPv6: {addr.address}")
        if interface in stats:
            print_info(f"  Speed: {stats[interface].speed} Mbps")
            print_info(f"  MTU: {stats[interface].mtu}")
            print_info(f"  Up: {stats[interface].isup}")

def boot_time(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    boot = psutil.boot_time()
    dt = time.gmtime(boot)
    print_info(f"Boot time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', dt)}")
    uptime = time.time() - boot
    days = int(uptime // 86400)
    hours = int((uptime % 86400) // 3600)
    minutes = int((uptime % 3600) // 60)
    print_info(f"Uptime: {days}d {hours}h {minutes}m")

def cpu_info(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    print_info(f"CPU: {platform.processor()}")
    print_info(f"Cores: {psutil.cpu_count(logical=True)} logical, {psutil.cpu_count(logical=False)} physical")
    print_info(f"Frequency: {psutil.cpu_freq().current:.2f} MHz")
    print_info(f"Usage: {psutil.cpu_percent(interval=1)}%")
    print_info("Per core usage:")
    for i, perc in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        print_info(f"  Core {i}: {perc}%")

def memory_info(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    print_info(f"RAM Total: {mem.total / (1024**3):.2f} GB")
    print_info(f"RAM Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    print_info(f"RAM Available: {mem.available / (1024**3):.2f} GB")
    print_info(f"Swap Total: {swap.total / (1024**3):.2f} GB")
    print_info(f"Swap Used: {swap.used / (1024**3):.2f} GB ({swap.percent}%)")

def disk_info(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print_info(f"{partition.device} ({partition.mountpoint}):")
            print_info(f"  Total: {usage.total / (1024**3):.2f} GB")
            print_info(f"  Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
            print_info(f"  Free: {usage.free / (1024**3):.2f} GB")
        except:
            pass

def kill_process_by_name(*args):
    if not HAS_PSUTIL:
        print_error("psutil module not installed. Run: pip install psutil")
        return
    name = input("  >> Enter process name: ").strip()
    if not name:
        print_error("No name provided")
        return
    killed = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == name.lower():
                proc.terminate()
                killed += 1
                print_success(f"Killed {proc.info['name']} (PID: {proc.info['pid']})")
        except:
            pass
    print_info(f"Killed {killed} processes")

def file_info(*args):
    filepath = input("  >> Enter file path: ").strip()
    if not os.path.exists(filepath):
        print_error("File not found")
        return
    stat = os.stat(filepath)
    print_info(f"Name: {os.path.basename(filepath)}")
    print_info(f"Size: {stat.st_size} bytes")
    print_info(f"Modified: {time.ctime(stat.st_mtime)}")
    print_info(f"Created: {time.ctime(stat.st_ctime)}")
    print_info(f"Permissions: {oct(stat.st_mode)[-3:]}")

def directory_size(*args):
    path = input("  >> Enter directory path: ").strip()
    if not os.path.exists(path):
        print_error("Path not found")
        return
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    print_info(f"Total size: {total / (1024**2):.2f} MB")

def find_large_files(*args):
    path = input("  >> Enter directory path: ").strip()
    if not os.path.exists(path):
        print_error("Path not found")
        return
    size_limit = input("  >> Size limit (MB): ").strip()
    try:
        size_limit = int(size_limit) * 1024 * 1024
    except:
        size_limit = 100 * 1024 * 1024
    found = []
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                size = os.path.getsize(fp)
                if size > size_limit:
                    found.append((fp, size))
    found.sort(key=lambda x: x[1], reverse=True)
    print_info(f"Files larger than {size_limit / (1024**2):.0f} MB:")
    for f, size in found[:20]:
        print_info(f"  {f} - {size / (1024**2):.2f} MB")

commands = {
    "system_info": {"func": system_info, "description": "Display system hardware and resource info", "usage": "system_info"},
    "process_manager": {"func": process_manager, "description": "List or kill running processes", "usage": "process_manager [list | kill <PID>]"},
    "network_scanner": {"func": network_scanner, "description": "Scan local network for active devices", "usage": "network_scanner"},
    "disk_analyzer": {"func": disk_analyzer, "description": "Analyze disk usage by folder", "usage": "disk_analyzer"},
    "resource_monitor": {"func": resource_monitor, "description": "Monitor system resources in real-time", "usage": "resource_monitor"},
    "clear_temp": {"func": clear_temp, "description": "Clear temporary system files", "usage": "clear_temp"},
    "battery_info": {"func": battery_info, "description": "Display battery status and info", "usage": "battery_info"},
    "network_info": {"func": network_info, "description": "Display network interface information", "usage": "network_info"},
    "boot_time": {"func": boot_time, "description": "Show system boot time and uptime", "usage": "boot_time"},
    "cpu_info": {"func": cpu_info, "description": "Display detailed CPU information", "usage": "cpu_info"},
    "memory_info": {"func": memory_info, "description": "Display detailed memory information", "usage": "memory_info"},
    "disk_info": {"func": disk_info, "description": "Display all disk partitions and usage", "usage": "disk_info"},
    "kill_process_by_name": {"func": kill_process_by_name, "description": "Kill all processes with a specific name", "usage": "kill_process_by_name"},
    "file_info": {"func": file_info, "description": "Get detailed information about a file", "usage": "file_info"},
    "directory_size": {"func": directory_size, "description": "Calculate total size of a directory", "usage": "directory_size"},
    "find_large_files": {"func": find_large_files, "description": "Find large files in a directory", "usage": "find_large_files"}
}
