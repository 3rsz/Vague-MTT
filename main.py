#!/usr/bin/env python3
"""
Vague 2.0 – Multi‑Tool Suite
Categories: Discord Tools, OSINT Tools, General Utilities, System Tools
"""

import importlib
import sys
import os
import json
import time
import threading
import shutil
from datetime import datetime
import random
import getpass

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        RESET = '\033[0m'
    class Back:
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'
        WHITE = '\033[47m'
        RESET = '\033[0m'
    class Style:
        BRIGHT = '\033[1m'
        DIM = '\033[2m'
        NORMAL = '\033[22m'
        RESET_ALL = '\033[0m'

CONFIG_FILE = "config.json"
CURRENT_THEME = "cyber"
MAIN_BANNER = ""
USERNAME = getpass.getuser()

def get_terminal_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def center_text(text, width=None):
    if width is None:
        width = get_terminal_width()
    if isinstance(text, str):
        import re
        clean_text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        padding = width - len(clean_text)
        left_padding = padding // 2
        return ' ' * left_padding + text
    return text

def load_config():
    """Load saved configuration"""
    global CURRENT_THEME
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                if 'theme' in config and config['theme'] in THEMES:
                    CURRENT_THEME = config['theme']
                    return True
    except:
        pass
    return False

def save_config():
    """Save current configuration"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'theme': CURRENT_THEME}, f)
        return True
    except:
        return False

def load_themes():
    """Load themes from modules/themes.py"""
    try:
        mod = importlib.import_module("modules.themes")
        if hasattr(mod, "THEMES"):
            return mod.THEMES
    except Exception as e:
        print(f"Warning: Could not load themes: {e}")
    return None

THEMES = load_themes()
if THEMES is None:
    THEMES = {
        "cyber": {
            "name": "Cyber",
            "primary": Fore.CYAN,
            "secondary": Fore.CYAN,
            "accent": Fore.CYAN + Style.BRIGHT,
            "success": Fore.CYAN,
            "error": Fore.CYAN,
            "warning": Fore.CYAN,
            "info": Fore.CYAN,
            "dim": Fore.CYAN + Style.DIM,
            "bright": Style.BRIGHT,
            "reset": Fore.RESET,
            "bg": Back.BLACK,
        }
    }

def get_theme():
    return THEMES[CURRENT_THEME]

def set_theme(theme_name):
    global CURRENT_THEME
    if theme_name in THEMES:
        CURRENT_THEME = theme_name
        save_config()
        return True
    return False

def get_theme_names():
    return list(THEMES.keys())

def glow_text(text, color=Fore.CYAN, intensity=0.5):
    """Create glowing text effect by adding bright/dim layers"""
    C = get_theme()
    glow_chars = []
    for char in text:
        if char == ' ':
            glow_chars.append(' ')
        elif random.random() < intensity:
            glow_chars.append(f"{C['accent']}{char}{C['reset']}")
        else:
            glow_chars.append(f"{C['dim']}{char}{C['reset']}")
    return ''.join(glow_chars)

def spinning_loader(text="Loading", duration=3):
    """Display a spinning loader animation with text"""
    C = get_theme()
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        clear_current_line()
        print(f"  {C['accent']}{spinners[i % len(spinners)]} {text} {C['reset']}", end='', flush=True)
        time.sleep(0.08)
        i += 1
    clear_current_line()

def clear_current_line():
    """Clear the current terminal line"""
    sys.stdout.write('\033[2K\033[G')
    sys.stdout.flush()

def progress_bar(current, total, prefix="Progress", width=40):
    """Display an animated progress bar with ETA"""
    C = get_theme()
    if total == 0:
        return
    
    percent = (current / total) * 100
    filled = int(width * current // total)
    bar = '█' * filled + '░' * (width - filled)
    
    elapsed = time.time() - progress_bar.start_time if hasattr(progress_bar, 'start_time') else 0
    if current > 0 and elapsed > 0:
        eta = (elapsed / current) * (total - current)
        eta_str = f"ETA: {int(eta//60)}m {int(eta%60)}s"
    else:
        eta_str = "ETA: Calculating..."
    
    print(f"\r  {C['secondary']}{prefix:<10}{C['reset']} {C['accent']}[{bar}]{C['reset']} {C['primary']}{percent:5.1f}%{C['reset']} {C['dim']}{current}/{total} {eta_str}{C['reset']}", end='', flush=True)

def fade_text(text, color=Fore.CYAN, delay=0.02):
    """Fade in and out text effect"""
    C = get_theme()
    chars = list(text)
    result = []
    
    for i in range(len(chars)):
        result.append(f"{color}{chars[i]}{C['reset']}")
        print(f"  {''.join(result)}", end='\r')
        time.sleep(delay)
    print()
    
    for i in range(len(chars) - 1, -1, -1):
        result.pop()
        print(f"  {''.join(result)}", end='\r')
        time.sleep(delay)
    print(' ' * 20, end='\r')

def rebuild_banner():
    global MAIN_BANNER
    C = get_theme()
    width = get_terminal_width()
    
    banner_lines = [
        "",
        "",
        "",
        f"{C['primary']}{Style.BRIGHT}██ ██  ▀▀█▄ ▄████ ██ ██ ▄█▀█▄",
        f"{C['primary']}{Style.BRIGHT}██▄██ ▄█▀██ ██ ██ ██ ██ ██▄█▀",
        f"{C['primary']}{Style.BRIGHT} ▀█▀  ▀█▄██ ▀████ ▀██▀█ ▀█▄▄▄",
        f"{C['primary']}{Style.BRIGHT}               ██",
        f"{C['primary']}{Style.BRIGHT}             ▀▀▀",
        "",
        f"{C['dim']}{'═' * 50}",
        f"{C['accent']}>>  Multi-Tool Suite  •  v2.0  •  Made with <3 by @iwwww__  <<",
        f"{C['dim']}{'═' * 50}",
    ]
    
    centered_lines = []
    for line in banner_lines:
        if line:
            centered_lines.append(center_text(line, width))
        else:
            centered_lines.append("")
    
    MAIN_BANNER = "\n".join(centered_lines)

def print_simple_header():
    """Print a simple header with the username"""
    C = get_theme()
    width = get_terminal_width()
    username_glow = glow_text(USERNAME.upper(), C['accent'], 0.5)
    
    header_lines = [
        "",
        f"{C['dim']}{'═' * 50}",
        f"{C['accent']}>>  {username_glow}  •  v2.0  •  Made with <3 by @iwwww__  <<",
        f"{C['dim']}{'═' * 50}",
    ]
    
    for line in header_lines:
        if line:
            print(center_text(line, width))
        else:
            print()

VERSION = "2.0"
PROJECT = "Vague"

CATEGORIES = {
    "1": {
        "id": "1", 
        "name": "DISCORD", 
        "module": "discord", 
        "symbol": ">>",
    },
    "2": {
        "id": "2", 
        "name": "OSINT", 
        "module": "osint", 
        "symbol": ">>",
    },
    "3": {
        "id": "3", 
        "name": "GENERAL", 
        "module": "general", 
        "symbol": ">>",
    },
    "4": {
        "id": "4", 
        "name": "SYSTEM", 
        "module": "system", 
        "symbol": ">>",
    }
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def separator(char='─', length=50):
    C = get_theme()
    width = get_terminal_width()
    msg = f"{C['dim']}{char * length}{C['reset']}"
    print(center_text(msg, width))

def print_success(text):
    C = get_theme()
    print(f"  {C['success']}>> {text}{C['reset']}")

def print_error(text):
    C = get_theme()
    print(f"  {C['error']}>> {text}{C['reset']}")

def print_warning(text):
    C = get_theme()
    print(f"  {C['warning']}>> {text}{C['reset']}")

def print_info(text):
    C = get_theme()
    print(f"  {C['info']}>> {text}{C['reset']}")

def print_prompt():
    C = get_theme()
    vague_glow = glow_text("vague", C['accent'], 0.5)
    print(f"\n{C['primary']}  ┌──[{vague_glow}{C['primary']}]──{C['dim']}[{C['reset']}~{C['dim']}]{C['reset']}")
    print(f"{C['primary']}  └─{C['accent']}$>{C['reset']} ", end="")

def show_themes():
    C = get_theme()
    width = get_terminal_width()
    clear()
    print_simple_header()
    separator('═', 50)
    print(center_text(f"{C['primary']}>> AVAILABLE THEMES{C['reset']}", width))
    print()
    
    theme_list = list(THEMES.keys())
    total = len(theme_list)
    cols = 2
    rows = (total + cols - 1) // cols
    
    for row in range(rows):
        line = ""
        for col in range(cols):
            idx = row + (col * rows)
            if idx < total:
                theme_name = theme_list[idx]
                theme_data = THEMES[theme_name]
                current_marker = " *" if theme_name == CURRENT_THEME else ""
                name_str = f"{theme_data['primary']}{theme_data['name']}{C['reset']}"
                if col == 0:
                    line = f"{C['primary']}[{C['accent']}{idx+1:02d}{C['primary']}]{C['reset']} {name_str}{current_marker}"
                else:
                    line += f"  {C['primary']}[{C['accent']}{idx+1:02d}{C['primary']}]{C['reset']} {name_str}{current_marker}"
            else:
                if col == 0:
                    line = " " * 34
                else:
                    line += " " * 34
        print(center_text(line, width))
    
    separator('─', 50)
    print(center_text(f"{C['dim']}Enter theme number to switch  │  [B] Back{C['reset']}", width))
    separator('═', 50)
    
    print_prompt()
    choice = input().strip().upper()
    
    if choice == 'B':
        return
    elif choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(theme_list):
            theme_name = theme_list[num-1]
            if set_theme(theme_name):
                rebuild_banner()
                spinning_loader(f"Applying {THEMES[theme_name]['name']} theme", 2)
                print_success(f"Theme changed to: {THEMES[theme_name]['name']}")
                input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        else:
            print_error("Invalid theme number")
            input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
    else:
        print_error("Invalid choice")
        input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")

def show_help(commands):
    C = get_theme()
    width = get_terminal_width()
    clear()
    print_simple_header()
    separator('═', 50)
    
    for cat_id, cat_info in CATEGORIES.items():
        cat_name = cat_info['name']
        cmds = [c for c in commands if c["category_id"] == cat_id]
        
        if cmds:
            print(center_text(f"{C['secondary']}>> {cat_name}{C['reset']}", width))
            for idx, cmd in enumerate(cmds, 1):
                desc = cmd.get('description', 'No description')
                print(center_text(f"{C['primary']}[{idx:02d}]{C['reset']} {cmd['name']}", width))
                print(center_text(f"{C['dim']}{desc}{C['reset']}", width))
            print()
    
    separator('═', 50)
    print(center_text(f"{C['dim']}Press Enter to continue...{C['reset']}", width))
    input()

def print_credits():
    C = get_theme()
    width = get_terminal_width()
    clear()
    print_simple_header()
    separator('═', 50)
    credits_lines = [
        f"{C['accent']}┌──────────────────────────────────────────────────┐",
        f"{C['accent']}│  ╔═══════════════════════════════════════════╗  │",
        f"{C['accent']}│  ║          Vague 2.0 - Credits             ║  │",
        f"{C['accent']}│  ╠═══════════════════════════════════════════╣  │",
        f"{C['accent']}│  ║  Created by  : @iwwww__                 ║  │",
        f"{C['accent']}│  ║  Project     : Vague 2.0                ║  │",
        f"{C['accent']}│  ║  Discord     : discord.gg/MNMQvREPzT    ║  │",
        f"{C['accent']}│  ║  Version     : 2.0                      ║  │",
        f"{C['accent']}│  ╚═══════════════════════════════════════════╝  │",
        f"{C['accent']}└──────────────────────────────────────────────────┘{C['reset']}"
    ]
    for line in credits_lines:
        print(center_text(line, width))
    separator('═', 50)
    print(center_text(f"{C['dim']}Press Enter to continue...{C['reset']}", width))
    input()

def print_boxed(text, color, width=50):
    C = get_theme()
    term_width = get_terminal_width()
    padding = width - len(text) - 2
    box_lines = [
        f"{color}┌{'─' * (width-2)}┐",
        f"{color}│ {text}{' ' * padding} │",
        f"{color}└{'─' * (width-2)}┘{C['reset']}"
    ]
    for line in box_lines:
        print(center_text(line, term_width))

def load_commands():
    commands = []
    
    for cat_id, cat_info in CATEGORIES.items():
        module_name = cat_info['module']
        try:
            mod = importlib.import_module(f"modules.{module_name}")
            if hasattr(mod, "commands"):
                for name, info in mod.commands.items():
                    original_func = info["func"]
                    def wrapped_func(func=original_func):
                        C = get_theme()
                        spinning_loader(f"Running {name}", 1)
                        try:
                            func()
                        except Exception as e:
                            print_error(f"Error: {e}")
                    
                    commands.append({
                        "category_id": cat_id,
                        "category_name": cat_info['name'],
                        "name": name,
                        "func": wrapped_func,
                        "description": info.get("description", ""),
                        "usage": info.get("usage", "")
                    })
        except Exception:
            pass
    
    return commands

def show_category_menu(category_id, commands):
    C = get_theme()
    width = get_terminal_width()
    cat_info = CATEGORIES.get(category_id)
    if not cat_info:
        return
    
    cat_name = cat_info['name']
    cat_symbol = cat_info['symbol']
    cmds = [c for c in commands if c["category_id"] == category_id]
    
    while True:
        clear()
        print_simple_header()
        
        if not cmds:
            print_warning("No commands available in this category")
            print(center_text(f"{C['dim']}[B] Back  |  [H] Help  |  [Q] Quit  |  [T] Themes{C['reset']}", width))
            print_prompt()
            choice = input().upper()
            if choice == 'B':
                break
            elif choice == 'H':
                show_help(commands)
            elif choice == 'Q':
                print(f"\n{C['success']}Goodbye!{C['reset']}")
                sys.exit(0)
            elif choice == 'T':
                show_themes()
            continue
        
        print(center_text(f"{C['secondary']}>> {cat_name} COMMANDS{C['reset']}", width))
        print()
        separator('─', 50)
        
        total = len(cmds)
        cols = 2
        rows = (total + cols - 1) // cols
        
        for row in range(rows):
            line = ""
            for col in range(cols):
                idx = row + (col * rows)
                if idx < total:
                    cmd = cmds[idx]
                    num = idx + 1
                    num_str = f"[{C['accent']}{num:02d}{C['primary']}]"
                    name_str = f"{C['secondary']}{cmd['name']:<25}{C['reset']}"
                    if col == 0:
                        line = f"{C['primary']}{num_str} {name_str}"
                    else:
                        line += f"  {C['primary']}{num_str} {name_str}"
                else:
                    if col == 0:
                        line = " " * 34
                    else:
                        line += " " * 34
            print(center_text(line, width))
        
        separator('─', 50)
        print(center_text(f"{C['dim']}[B] Back  │  [H] Help  │  [Q] Quit  │  [T] Themes{C['reset']}", width))
        print(center_text(f"{C['dim']}>> Total: {len(cmds)} commands available{C['reset']}", width))
        separator('═', 50)
        
        print_prompt()
        choice = input().strip().upper()
        
        if choice == 'B':
            break
        elif choice == 'H':
            show_help(commands)
        elif choice == 'Q':
            print(f"\n{C['success']}Goodbye!{C['reset']}")
            sys.exit(0)
        elif choice == 'T':
            show_themes()
        elif choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(cmds):
                cmd = cmds[num-1]
                clear()
                print_simple_header()
                print_boxed(f">> {cmd['name']}", C['secondary'])
                separator('═', 50)
                print()
                try:
                    cmd["func"]()
                except KeyboardInterrupt:
                    print(f"\n{C['warning']}Interrupted by user{C['reset']}")
                except Exception as e:
                    print_error(f"Error: {e}")
                print(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
                input()
            else:
                print_error("Invalid command number")
                input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")
        else:
            print_error("Invalid choice")
            input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")

def format_category_line(cat_id, cat_info, cmd_count, width):
    """Format a category line with proper centering and alignment"""
    C = get_theme()
    cat_name = cat_info['name']
    cat_symbol = cat_info['symbol']
    
    padded_id = f"{int(cat_id):02d}"
    
    clean_line = f"[{padded_id}] {cat_symbol} {cat_name} ({cmd_count} commands)"
    clean_len = len(clean_line)
    
    padding = (width - clean_len) // 2
    if padding < 0:
        padding = 0
    
    colored_line = f"{' ' * padding}{C['primary']}[{C['accent']}{padded_id}{C['primary']}]{C['reset']}  {cat_symbol}  {C['secondary']}{cat_name}{C['reset']}  {C['dim']}({cmd_count} commands){C['reset']}"
    return colored_line

def main():
    global MAIN_BANNER
    load_config()
    rebuild_banner()
    commands = load_commands()
    
    while True:
        C = get_theme()
        width = get_terminal_width()
        clear()
        print(MAIN_BANNER)
        
        print()
        for cat_id, cat_info in CATEGORIES.items():
            cmd_count = len([c for c in commands if c["category_id"] == cat_id])
            line = format_category_line(cat_id, cat_info, cmd_count, width)
            print(line)
        
        print()
        separator('─', 50)
        print(center_text(f"{C['dim']}[H] Help  │  [C] Credits  │  [Q] Quit  │  [T] Themes{C['reset']}", width))
        print(center_text(f"{C['dim']}>> Current Theme: {THEMES[CURRENT_THEME]['name']}{C['reset']}", width))
        separator('═', 50)
        
        print_prompt()
        choice = input().strip().upper()
        
        if choice == 'Q':
            print(f"\n{C['success']}Goodbye! Thanks for using Vague!{C['reset']}")
            sys.exit(0)
        elif choice == 'C':
            print_credits()
        elif choice == 'H':
            show_help(commands)
        elif choice == 'T':
            show_themes()
        elif choice in CATEGORIES:
            show_category_menu(choice, commands)
        else:
            print_error("Invalid choice. Please enter 1-4, H, C, T, or Q")
            input(f"\n  {C['dim']}Press Enter to continue...{C['reset']}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        C = get_theme()
        print(f"\n{C['success']}Goodbye!{C['reset']}")
        sys.exit(0)
    except Exception as e:
        C = get_theme()
        print_error(f"Fatal Error: {e}")
        sys.exit(1)
