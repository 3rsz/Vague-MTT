import requests
import json
import socket
import dns.resolver
import whois
import ssl
import re
import time
import hashlib
import urllib.parse
from datetime import datetime

def print_success(text):
    print(f"  >> {text}")

def print_error(text):
    print(f"  >> {text}")

def print_info(text):
    print(f"  >> {text}")

def run_name_gen(*args):
    import random
    import string
    from collections import defaultdict
    
    def check_platform(username, platform, timeout=5):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        try:
            if platform == "TikTok":
                url = f"https://www.tiktok.com/@{username}"
                r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
                return r.status_code == 404
            elif platform == "YouTube":
                url = f"https://www.youtube.com/@{username}"
                r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
                if "This channel does not exist" in r.text:
                    return True
                if "/@" in r.url:
                    return False
                return True
            elif platform == "Instagram":
                url = f"https://www.instagram.com/{username}/"
                r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
                if r.status_code == 404:
                    return True
                if "Sorry, this page isn't available" in r.text:
                    return True
                return False
        except:
            return None
        return None

    def generate_username(length, char_set):
        if char_set == "letters":
            chars = string.ascii_lowercase
        elif char_set == "numbers":
            chars = string.digits
        else:
            chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_and_check(length, count_per_type, type_choice):
        type_map = {"n": "numbers", "l": "letters", "m": "mixed"}
        type_name_map = {"n": "Numbers", "l": "Letters", "m": "Mixed"}
        char_set = type_map.get(type_choice, "mixed")
        display_name = type_name_map.get(type_choice, "Mixed")
        results = []
        print_info(f"Generating {count_per_type} {display_name} usernames of length {length}...")
        for i in range(count_per_type):
            uname = generate_username(length, char_set)
            platforms = ["TikTok", "YouTube", "Instagram"]
            for plat in platforms:
                available = check_platform(uname, plat)
                status = "Available" if available else ("Taken" if available is False else "Error")
                results.append({"username": uname, "type": display_name, "platform": plat, "status": status})
            progress_bar(i + 1, count_per_type, prefix=display_name)
        print()
        return results

    def display_results_dashboard(results):
        total = len(results)
        available = sum(1 for r in results if r['status'] == "Available")
        taken = sum(1 for r in results if r['status'] == "Taken")
        error = sum(1 for r in results if r['status'] == "Error")
        
        grouped = defaultdict(dict)
        for r in results:
            grouped[r['username']][r['platform']] = r['status']
        
        print_info(f"Generated: {total}  Available: {available}  Taken: {taken}  Error: {error}")
        print_info("Username\t\tTikTok\tYouTube\tInstagram")
        for username, platforms in grouped.items():
            tiktok_status = platforms.get("TikTok", "Error")
            youtube_status = platforms.get("YouTube", "Error")
            instagram_status = platforms.get("Instagram", "Error")
            tiktok_icon = "✅" if tiktok_status == "Available" else ("❌" if tiktok_status == "Taken" else "⚠️")
            youtube_icon = "✅" if youtube_status == "Available" else ("❌" if youtube_status == "Taken" else "⚠️")
            instagram_icon = "✅" if instagram_status == "Available" else ("❌" if instagram_status == "Taken" else "⚠️")
            print_info(f"{username}\t\t{tiktok_icon}\t{youtube_icon}\t{instagram_icon}")
        return available

    length_input = input("  >> Enter username length (3-20): ")
    try:
        length = int(length_input)
        if length < 3: length = 3
        if length > 20: length = 20
    except:
        length = 8
    
    print_info("Select username type:")
    print_info("  [N] Numbers only (0-9)")
    print_info("  [L] Letters only (a-z)")
    print_info("  [M] Mixed (letters + numbers)")
    type_choice = input("  >> Enter choice (N/L/M): ").strip().lower()
    valid_types = ["n", "l", "m"]
    if type_choice not in valid_types:
        print_error("Invalid choice. Defaulting to Mixed.")
        type_choice = "m"
    
    count_input = input("  >> Number of usernames to generate (default 10): ")
    try:
        count = int(count_input)
        if count < 1: count = 10
        if count > 100: count = 100
    except:
        count = 10
    
    results = generate_and_check(length, count, type_choice)
    available = display_results_dashboard(results)
    print_success(f"Total Available: {available}")
    
    export_choice = input("  >> Export to .txt file? (y/n): ").strip().lower()
    if export_choice == 'y':
        filename = input("  >> Enter filename (default: usernames.txt): ").strip()
        if not filename: filename = "usernames.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Username,Type,Platform,Status\n")
            for r in results:
                f.write(f"{r['username']},{r['type']},{r['platform']},{r['status']}\n")
        print_success(f"Exported to {filename}")

def ip_geolocation(*args):
    if not args:
        ip = input("  >> Enter IP address (or press Enter for your public IP): ").strip()
    else:
        ip = args[0]
    
    if not ip:
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                ip = response.json().get('ip')
                print_info(f"Your public IP: {ip}")
            else:
                print_error("Could not determine your public IP")
                return
        except:
            print_error("Could not determine your public IP")
            return
    
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success':
                print_info(f"IP Address: {data.get('query', 'N/A')}")
                print_info(f"Country: {data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})")
                print_info(f"Region: {data.get('regionName', 'N/A')} ({data.get('region', 'N/A')})")
                print_info(f"City: {data.get('city', 'N/A')}")
                print_info(f"ZIP Code: {data.get('zip', 'N/A')}")
                print_info(f"Latitude: {data.get('lat', 'N/A')}")
                print_info(f"Longitude: {data.get('lon', 'N/A')}")
                print_info(f"Timezone: {data.get('timezone', 'N/A')}")
                print_info(f"ISP: {data.get('isp', 'N/A')}")
                print_info(f"Organization: {data.get('org', 'N/A')}")
                print_info(f"AS: {data.get('as', 'N/A')}")
                lat = data.get('lat')
                lon = data.get('lon')
                if lat and lon:
                    print_info(f"Google Maps: https://www.google.com/maps?q={lat},{lon}")
            else:
                print_error(f"Error: {data.get('message', 'Unknown error')}")
        else:
            print_error(f"Failed to connect to ip-api.com. Status: {r.status_code}")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except requests.exceptions.ConnectionError:
        print_error("Connection error")
    except Exception as e:
        print_error(f"Error: {e}")

def username_check(*args):
    if not args:
        username = input("  >> Enter username to check: ").strip()
    else:
        username = args[0]
    
    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "YouTube": f"https://www.youtube.com/@{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Tumblr": f"https://{username}.tumblr.com",
        "Twitch": f"https://www.twitch.tv/{username}",
        "Spotify": f"https://open.spotify.com/user/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Vimeo": f"https://vimeo.com/{username}",
        "DeviantArt": f"https://www.deviantart.com/{username}",
        "Flickr": f"https://www.flickr.com/people/{username}/"
    }
    
    results = {}
    print_info(f"Checking username '{username}' across {len(platforms)} platforms...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for platform, url in platforms.items():
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                not_found_indicators = [
                    "not found", "doesn't exist", "page not found",
                    "sorry, this page isn't available", "this channel does not exist"
                ]
                page_text = response.text.lower()
                is_taken = True
                for indicator in not_found_indicators:
                    if indicator in page_text:
                        is_taken = False
                        break
                results[platform] = is_taken
            elif response.status_code == 404:
                results[platform] = False
            else:
                results[platform] = True
        except:
            results[platform] = None
    
    available = sum(1 for r in results.values() if r is True)
    taken = sum(1 for r in results.values() if r is False)
    errors = sum(1 for r in results.values() if r is None)
    print_info(f"Available: {available}  Taken: {taken}  Errors: {errors}")
    sorted_results = sorted(results.items(), key=lambda x: (x[1] is not True, x[0]))
    for platform, available in sorted_results:
        if available is True:
            status = "✅ AVAILABLE"
        elif available is False:
            status = "❌ TAKEN"
        else:
            status = "⚠️ ERROR"
        print_info(f"{platform:<15} {status}")

def phone_lookup(*args):
    if not args:
        phone = input("  >> Enter phone number (e.g., +14155552671): ").strip()
    else:
        phone = args[0]
    
    phone_api_key = "3c043e09c3054fb1b580ac478450398a"
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    print_info(f"Looking up phone number: {phone}")
    
    try:
        url = f'https://phonevalidation.abstractapi.com/v1/?api_key={phone_api_key}&phone={cleaned}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print_info(f"Phone Number: {data.get('phone', 'N/A')}")
                print_success("Valid: Yes")
                print_info(f"Country: {data.get('country', 'N/A')}")
                print_info(f"Location: {data.get('location', 'N/A')}")
                print_info(f"Carrier: {data.get('carrier', 'N/A')}")
                print_info(f"Line Type: {data.get('line_type', 'N/A')}")
            else:
                print_error("Invalid phone number")
        elif response.status_code == 401:
            print_error("API Key is invalid or not activated")
        else:
            print_error(f"Failed to connect. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Error: {e}")

def leaked_password_check(*args):
    if not args:
        password = input("  >> Enter password to check: ").strip()
    else:
        password = args[0]
    
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    print_info(f"Checking password against HaveIBeenPwned database...")
    print_info(f"Hash prefix: {prefix}")
    
    try:
        url = f'https://api.pwnedpasswords.com/range/{prefix}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            found_suffixes = []
            for line in response.text.splitlines():
                parts = line.split(':')
                if len(parts) == 2:
                    found_suffixes.append((parts[0], int(parts[1])))
            for s, count in found_suffixes:
                if s == suffix:
                    print_error(f"PASSWORD LEAKED! Found in {count} data breaches!")
                    print_error("It is NOT safe to use this password.")
                    return
            print_success("PASSWORD NOT LEAKED! Not found in any known breaches.")
        else:
            print_error(f"Failed to check password. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        print_error("Request timed out")
    except Exception as e:
        print_error(f"Error: {e}")

def domain_whois(*args):
    if not args:
        domain = input("  >> Enter domain: ").strip()
    else:
        domain = args[0]
    
    try:
        w = whois.whois(domain)
        print_info(f"Domain: {w.domain_name}")
        print_info(f"Registrar: {w.registrar}")
        print_info(f"Creation Date: {w.creation_date}")
        print_info(f"Expiration Date: {w.expiration_date}")
        print_info(f"Last Updated: {w.last_updated}")
        print_info(f"Name Servers: {w.name_servers}")
        if w.registrant:
            print_info(f"Registrant: {w.registrant}")
        if w.admin:
            print_info(f"Admin: {w.admin}")
        if w.tech:
            print_info(f"Tech: {w.tech}")
    except Exception as e:
        print_error(f"Error: {e}")

def email_lookup(*args):
    if not args:
        email = input("  >> Enter email address: ").strip()
    else:
        email = args[0]
    
    print_info(f"Checking email: {email}")
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            print_success(f"Domain {domain} has valid MX records")
            print_info("MX Records:")
            for mx in mx_records:
                print_info(f"  - {mx.exchange} (Priority: {mx.preference})")
        else:
            print_error(f"No MX records found for {domain}")
    except:
        print_error(f"Could not verify mail server for {domain}")
    
    try:
        url = f"https://api.hunter.io/v2/email-verifier?email={email}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data', {}).get('status') == 'valid':
                print_success("Email appears to be valid")
            else:
                print_warning("Email may be invalid or not verified")
    except:
        pass

def subdomain_scanner(*args):
    if not args:
        domain = input("  >> Enter domain: ").strip()
    else:
        domain = args[0]
    
    subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'download', 'dns', 'piwik', 'stats', 'dashboard', 'portal', 'manage', 'start', 'info', 'apps', 'video', 'sip', 'dns2', 'api', 'cdn', 'live', 'help', 'chat', 'cloud', 'vps', 'ns4', 'ns5', 'server', 'cms', 'stage']
    
    found = []
    total = len(subdomains)
    print_info(f"Scanning for subdomains...")
    for i, sub in enumerate(subdomains):
        try:
            target = f"{sub}.{domain}"
            socket.gethostbyname(target)
            found.append(target)
            print_success(f"Found: {target}")
        except:
            pass
        progress_bar(i + 1, total, prefix="Scanning")
    print_info(f"Found {len(found)} subdomains")

def website_info(*args):
    if not args:
        url = input("  >> Enter URL: ").strip()
    else:
        url = args[0]
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        print_info(f"URL: {response.url}")
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Server: {response.headers.get('Server', 'Unknown')}")
        print_info(f"Content Type: {response.headers.get('Content-Type', 'Unknown')}")
        print_info(f"Content Length: {response.headers.get('Content-Length', 'Unknown')}")
        print_info(f"Last Modified: {response.headers.get('Last-Modified', 'Unknown')}")
        print_info(f"IP Address: {socket.gethostbyname(urllib.parse.urlparse(response.url).netloc)}")
        print_info("Headers:")
        for key, value in response.headers.items():
            print_info(f"  {key}: {value}")
    except Exception as e:
        print_error(f"Error: {e}")

def dns_lookup(*args):
    if not args:
        domain = input("  >> Enter domain: ").strip()
    else:
        domain = args[0]
    
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
    print_info(f"Performing DNS lookups for {domain}...")
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print_info(f"{record_type}:")
            for rdata in answers:
                print_info(f"  {rdata}")
        except:
            print_error(f"{record_type}: No records found")

def port_scanner(*args):
    if not args:
        target = input("  >> Enter IP or domain: ").strip()
    else:
        target = args[0]
    
    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
        80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 3306: 'MySQL',
        3389: 'RDP', 5432: 'PostgreSQL', 6379: 'Redis', 27017: 'MongoDB'
    }
    
    try:
        ip = socket.gethostbyname(target)
        print_info(f"IP Address: {ip}")
        print_info(f"Scanning {target}...")
        open_ports = []
        total = len(common_ports)
        i = 0
        
        for port, service in common_ports.items():
            i += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append((port, service))
                print_success(f"Port {port} ({service}) - OPEN")
            else:
                print_error(f"Port {port} ({service}) - CLOSED")
            sock.close()
            progress_bar(i, total, prefix="Scanning")
        
        if open_ports:
            print_success(f"Open ports found: {len(open_ports)}")
        else:
            print_warning("No open ports found")
    except Exception as e:
        print_error(f"Error: {e}")

def link_grabber(*args):
    if not args:
        url = input("  >> Enter URL: ").strip()
    else:
        url = args[0]
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        links = re.findall(r'href=[\'"]?([^\'" >]+)', html)
        unique_links = set()
        for link in links:
            if link and not link.startswith('#') and not link.startswith('javascript:'):
                if link.startswith('/'):
                    parsed = urllib.parse.urlparse(url)
                    link = f"{parsed.scheme}://{parsed.netloc}{link}"
                unique_links.add(link)
        print_info(f"Total Links Found: {len(unique_links)}")
        for link in sorted(unique_links):
            print_info(f"  {link}")
    except Exception as e:
        print_error(f"Error: {e}")

def mac_lookup(*args):
    if not args:
        mac = input("  >> Enter MAC address (e.g., 00:11:22:33:44:55): ").strip()
    else:
        mac = args[0]
    
    mac_clean = re.sub(r'[^a-fA-F0-9]', '', mac).upper()
    if len(mac_clean) < 6:
        print_error("Invalid MAC address")
        return
    oui = mac_clean[:6]
    print_info(f"Looking up MAC: {mac}")
    try:
        response = requests.get(f"https://api.macvendors.com/{oui}", timeout=10)
        if response.status_code == 200:
            manufacturer = response.text.strip()
            print_info(f"OUI Prefix: {oui}")
            print_success(f"Manufacturer: {manufacturer}")
        else:
            print_error("Manufacturer not found")
    except Exception as e:
        print_error(f"Error: {e}")

def ssl_checker(*args):
    if not args:
        domain = input("  >> Enter domain: ").strip()
    else:
        domain = args[0]
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                print_info(f"Domain: {domain}")
                print_info(f"Subject: {cert.get('subject', [])}")
                print_info(f"Issuer: {cert.get('issuer', [])}")
                print_info(f"Not Before: {cert.get('notBefore', 'N/A')}")
                print_info(f"Not After: {cert.get('notAfter', 'N/A')}")
                print_info(f"Serial Number: {cert.get('serialNumber', 'N/A')}")
                expire_date = datetime.strptime(cert.get('notAfter'), '%b %d %H:%M:%S %Y %Z')
                days_left = (expire_date - datetime.now()).days
                if days_left < 0:
                    print_error(f"Certificate EXPIRED! ({abs(days_left)} days ago)")
                elif days_left < 30:
                    print_warning(f"Certificate expires in {days_left} days!")
                else:
                    print_success(f"Certificate valid for {days_left} more days")
    except Exception as e:
        print_error(f"Error: {e}")

def social_search(*args):
    if not args:
        username = input("  >> Enter username to search: ").strip()
    else:
        username = args[0]
    
    platforms = {
        'Twitter': f"https://twitter.com/{username}",
        'Instagram': f"https://www.instagram.com/{username}/",
        'Facebook': f"https://www.facebook.com/{username}",
        'YouTube': f"https://www.youtube.com/@{username}",
        'TikTok': f"https://www.tiktok.com/@{username}",
        'Reddit': f"https://www.reddit.com/user/{username}",
        'GitHub': f"https://github.com/{username}",
        'Pinterest': f"https://www.pinterest.com/{username}/",
        'Tumblr': f"https://{username}.tumblr.com",
        'Snapchat': f"https://www.snapchat.com/add/{username}",
        'Twitch': f"https://www.twitch.tv/{username}",
        'SoundCloud': f"https://soundcloud.com/{username}",
        'Spotify': f"https://open.spotify.com/user/{username}",
        'Vimeo': f"https://vimeo.com/{username}",
        'DeviantArt': f"https://www.deviantart.com/{username}",
        'Flickr': f"https://www.flickr.com/people/{username}/"
    }
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    found = []
    print_info(f"Searching for {username} across {len(platforms)} platforms...")
    for platform, url in platforms.items():
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                not_found_indicators = ['not found', 'doesn\'t exist', 'page not found', 'sorry, this page isn\'t available']
                page_text = response.text.lower()
                is_real = True
                for indicator in not_found_indicators:
                    if indicator in page_text:
                        is_real = False
                        break
                if is_real:
                    found.append((platform, url))
                    print_success(f"{platform}: Found")
                else:
                    print_error(f"{platform}: Not found")
            elif response.status_code == 404:
                print_error(f"{platform}: Not found")
            else:
                print_warning(f"{platform}: Could not verify")
        except:
            print_warning(f"{platform}: Error checking")
    print_success(f"Found on {len(found)} platforms")

def progress_bar(current, total, width=25, prefix=""):
    percentage = (current / total) * 100
    filled = int(width * current // total)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r  {prefix:<10} [{bar}] {percentage:5.1f}%  {current}/{total}", end="", flush=True)
    if current == total:
        print()

def leaked_check(*args):
    if not args:
        email = input("  >> Enter email address to check: ").strip()
    else:
        email = args[0]
    
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            breaches = r.json()
            print_info(f"Email '{email}' found in {len(breaches)} breach(es):")
            for b in breaches:
                print_info(f"  - {b['Name']} ({b['BreachDate']})")
        elif r.status_code == 404:
            print_success(f"Email '{email}' not found in any known breaches.")
        else:
            print_error(f"API error: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def reverse_ip_lookup(*args):
    if not args:
        ip = input("  >> Enter IP address: ").strip()
    else:
        ip = args[0]
    
    try:
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=10)
        if r.status_code == 200:
            domains = r.text.strip().split('\n')
            print_info(f"Domains hosted on {ip}:")
            for domain in domains:
                print_info(f"  - {domain}")
        else:
            print_error(f"Failed to lookup: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def geoip_lookup(*args):
    if not args:
        ip = input("  >> Enter IP address: ").strip()
    else:
        ip = args[0]
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success':
                print_info(f"IP: {data.get('query')}")
                print_info(f"Country: {data.get('country')}")
                print_info(f"Region: {data.get('regionName')}")
                print_info(f"City: {data.get('city')}")
                print_info(f"ZIP: {data.get('zip')}")
                print_info(f"Timezone: {data.get('timezone')}")
                print_info(f"ISP: {data.get('isp')}")
                print_info(f"Latitude: {data.get('lat')}")
                print_info(f"Longitude: {data.get('lon')}")
            else:
                print_error("Invalid IP address")
        else:
            print_error(f"Failed to lookup: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def dns_history(*args):
    if not args:
        domain = input("  >> Enter domain: ").strip()
    else:
        domain = args[0]
    
    try:
        r = requests.get(f"https://api.hackertarget.com/historydns/?q={domain}", timeout=10)
        if r.status_code == 200:
            records = r.text.strip().split('\n')
            print_info(f"DNS History for {domain}:")
            for record in records:
                print_info(f"  - {record}")
        else:
            print_error(f"Failed to get history: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def http_headers(*args):
    if not args:
        url = input("  >> Enter URL: ").strip()
    else:
        url = args[0]
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        r = requests.get(url, timeout=10)
        print_info(f"URL: {r.url}")
        print_info(f"Status: {r.status_code}")
        print_info("Headers:")
        for key, value in r.headers.items():
            print_info(f"  - {key}: {value}")
    except Exception as e:
        print_error(f"Error: {e}")

def ip_geolocation_lookup(*args):
    if not args:
        ip = input("  >> Enter IP address: ").strip()
    else:
        ip = args[0]
    
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            print_info(f"IP: {data.get('ip')}")
            print_info(f"City: {data.get('city')}")
            print_info(f"Region: {data.get('region')}")
            print_info(f"Country: {data.get('country')}")
            print_info(f"Location: {data.get('loc')}")
            print_info(f"Org: {data.get('org')}")
            print_info(f"Timezone: {data.get('timezone')}")
        else:
            print_error(f"Failed to lookup: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

def asn_lookup(*args):
    if not args:
        ip = input("  >> Enter IP address: ").strip()
    else:
        ip = args[0]
    
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        if r.status_code == 200:
            data = r.json()
            asn_info = data.get('org', '')
            print_info(f"IP: {data.get('ip')}")
            print_info(f"ASN/Org: {asn_info}")
            print_info(f"Country: {data.get('country')}")
        else:
            print_error(f"Failed to lookup: {r.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")

commands = {
    "name_gen": {"func": run_name_gen, "description": "Generate and check username availability", "usage": "name_gen"},
    "ip_geolocation": {"func": ip_geolocation, "description": "Get geolocation data for an IP", "usage": "ip_geolocation [ip]"},
    "username_check": {"func": username_check, "description": "Check username across multiple platforms", "usage": "username_check <username>"},
    "phone_lookup": {"func": phone_lookup, "description": "Lookup phone number information", "usage": "phone_lookup <phone>"},
    "leaked_password_check": {"func": leaked_password_check, "description": "Check if a password has been leaked", "usage": "leaked_password_check"},
    "domain_whois": {"func": domain_whois, "description": "Get WHOIS information for a domain", "usage": "domain_whois <domain>"},
    "email_lookup": {"func": email_lookup, "description": "Verify email address validity", "usage": "email_lookup <email>"},
    "subdomain_scanner": {"func": subdomain_scanner, "description": "Find subdomains of a domain", "usage": "subdomain_scanner <domain>"},
    "website_info": {"func": website_info, "description": "Get website headers and information", "usage": "website_info <url>"},
    "dns_lookup": {"func": dns_lookup, "description": "Lookup DNS records for a domain", "usage": "dns_lookup <domain>"},
    "port_scanner": {"func": port_scanner, "description": "Scan common ports on a target", "usage": "port_scanner <target>"},
    "link_grabber": {"func": link_grabber, "description": "Extract all links from a webpage", "usage": "link_grabber <url>"},
    "mac_lookup": {"func": mac_lookup, "description": "Lookup MAC address manufacturer", "usage": "mac_lookup <mac>"},
    "ssl_checker": {"func": ssl_checker, "description": "Check SSL certificate details", "usage": "ssl_checker <domain>"},
    "social_search": {"func": social_search, "description": "Search for username on social media", "usage": "social_search <username>"},
    "leaked_check": {"func": leaked_check, "description": "Check email in data breaches", "usage": "leaked_check <email>"},
    "reverse_ip_lookup": {"func": reverse_ip_lookup, "description": "Find domains hosted on an IP", "usage": "reverse_ip_lookup <ip>"},
    "geoip_lookup": {"func": geoip_lookup, "description": "Detailed geolocation for an IP", "usage": "geoip_lookup <ip>"},
    "dns_history": {"func": dns_history, "description": "View DNS history for a domain", "usage": "dns_history <domain>"},
    "http_headers": {"func": http_headers, "description": "View HTTP headers for a URL", "usage": "http_headers <url>"},
    "ip_geolocation_lookup": {"func": ip_geolocation_lookup, "description": "Geolocation data from ipinfo.io", "usage": "ip_geolocation_lookup <ip>"},
    "asn_lookup": {"func": asn_lookup, "description": "Lookup ASN for an IP address", "usage": "asn_lookup <ip>"}
}