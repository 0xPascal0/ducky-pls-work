import os
import re
import time

C = "\033[96m"
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
W = "\033[0m"

VALID_CMDS = [
    "REM", "DEFAULT_DELAY", "DEFAULTDELAY", "DELAY", "STRING", 
    "WINDOWS", "GUI", "ENTER", "CTRL", "CONTROL", "ALT", "SHIFT", 
    "TAB", "SPACE", "UP", "DOWN", "LEFT", "RIGHT", "CAPSLOCK", "ESC"
]

APP_MAP = {
    ("notepad", "editor", "text edit"): ("notepad", 600),
    ("calculator", "calc"): ("calc", 500),
    ("paint", "draw"): ("mspaint", 700),
    ("cmd", "terminal", "command prompt"): ("cmd", 600),
    ("powershell", "ps"): ("powershell -NoP", 800),
    ("task manager", "taskmgr"): ("taskmgr", 800),
    ("control panel", "settings"): ("control", 700),
    ("device manager",): ("devmgmt.msc", 800),
    ("disk management",): ("diskmgmt.msc", 800),
    ("registry", "regedit"): ("regedit", 900),
    ("services",): ("services.msc", 800),
    ("event viewer",): ("eventvwr", 800),
    ("file explorer", "explorer", "files"): ("explorer", 700),
    ("spotify",): ("spotify", 1200),
    ("discord",): ("discord", 1200),
    ("steam",): ("steam", 1200),
    ("vlc", "media player"): ("vlc", 1000),
    ("chrome",): ("chrome", 1000),
    ("firefox",): ("firefox", 1000),
    ("edge",): ("msedge", 1000),
    ("code", "vscode", "vs code"): ("code", 1200),
}

SITE_MAP = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "twitch": "https://www.twitch.tv",
    "wikipedia": "https://www.wikipedia.org",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "duckduckgo": "https://duckduckgo.com",
    "chatgpt": "https://chatgpt.com",
}

def print_banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(f"""{C}
 ▄▄▄▄▄▄▄   ▄▄   ▄▄  ▄▄▄▄▄▄▄  ▄▄▄   ▄  ▄   ▄ 
█      █  █  █ █  ██       ██   █ █ ██  █ █ █
█  ▄   █  █  █ █  ██       ██   █▄█ █ █▄█ █
█ █▄█  █  █  █▄█  ██      ▄██      ▄█       █
█      █  █       ██     █▄ █     █▄▄▄   ▄▄▄█
█  ▄   █  █       ██      ███    ▄  █ █ █   
█▄█ █▄▄█  █▄▄▄▄▄▄▄█ █▄▄▄▄▄███▄▄▄█ █▄█ █▄█ 
{W}""")

def parse_intent_to_ducky(prompt: str) -> str:
    p = prompt.strip().lower()

    if any(k in p for k in ["rickroll", "never gonna give you up"]):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING https://www.youtube.com/watch?v=dQw4w9WgXcQ\nENTER\n"

    if any(k in p for k in ["fake update", "fake windows update"]):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING https://fakeupdate.net/win10ue/\nENTER\nDELAY 2000\nF11\n"

    if any(k in p for k in ["bsod", "blue screen"]):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING https://geekprank.com/blue-death/\nENTER\nDELAY 2000\nF11\n"

    if any(k in p for k in ["lock screen", "lock pc", "lock computer"]):
        return "DELAY 1000\nGUI l\n"

    if any(k in p for k in ["minimize all", "show desktop"]):
        return "DELAY 1000\nGUI d\n"

    if any(k in p for k in ["shutdown", "turn off pc"]):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING shutdown /s /t 60\nENTER\n"

    if any(k in p for k in ["restart pc", "reboot"]):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING shutdown /r /t 60\nENTER\n"

    if any(k in p for k in ["volume up", "increase volume"]):
        return "DELAY 500\n" + ("VOLUMEUP\nDELAY 100\n" * 5)

    if any(k in p for k in ["volume down", "decrease volume"]):
        return "DELAY 500\n" + ("VOLUMEDOWN\nDELAY 100\n" * 5)

    if any(k in p for k in ["mute", "silence"]):
        return "DELAY 500\nMUTE\n"

    if "wifi pass" in p or "wifi password" in p:
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING cmd /k netsh wlan show profiles\nENTER\n"

    if "ip" in p and ("show" in p or "get" in p or "what is" in p):
        return "DELAY 1000\nGUI r\nDELAY 500\nSTRING cmd /k ipconfig /all\nENTER\n"

    if "search" in p:
        m = re.search(r'search\s+(?:for\s+)?(.+?)(?:\s+on|\s+in|\s*$)', p)
        query = m.group(1).strip() if m else p.replace("search", "").strip()
        target = "google"
        for site in SITE_MAP:
            if site in p:
                target = site
                break
        if target == "youtube":
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        else:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return f"DELAY 1000\nGUI r\nDELAY 500\nSTRING {url}\nENTER\n"

    for site_key, base_url in SITE_MAP.items():
        if site_key in p:
            return f"DELAY 1000\nGUI r\nDELAY 500\nSTRING {base_url}\nENTER\n"

    url_match = re.search(r'(https?://\S+|www\.\S+|\b[a-zA-Z0-9.-]+\.(?:com|org|net|io|it|ch|de|fr)\b)', p)
    if url_match:
        url = url_match.group(1)
        if not url.startswith("http"):
            url = "https://" + url
        return f"DELAY 1000\nGUI r\nDELAY 500\nSTRING {url}\nENTER\n"

    if any(k in p for k in ["type ", "write ", "say "]):
        for prefix in ["type ", "write ", "say "]:
            if p.startswith(prefix):
                content = prompt.strip()[len(prefix):]
                return f"DELAY 1000\nSTRING {content}\nENTER\n"

    for aliases, (bin_name, delay_time) in APP_MAP.items():
        if any(alias in p for alias in aliases):
            remainder = p
            for alias in aliases:
                remainder = re.sub(rf'\b{alias}\b', '', remainder)
            remainder = remainder.replace("open", "").replace("run", "").replace("and", "").strip()
            
            payload = f"DELAY 1000\nGUI r\nDELAY 500\nSTRING {bin_name}\nENTER\nDELAY {delay_time}\n"
            if remainder:
                payload += f"STRING {remainder}\nENTER\n"
            return payload

    clean_cmd = p.replace("open ", "").replace("run ", "").replace("execute ", "").strip()
    return f"DELAY 1000\nGUI r\nDELAY 500\nSTRING {clean_cmd}\nENTER\n"

def generate_payload():
    prompt = input("\naction > ").strip()
    if not prompt:
        return
        
    payload = parse_intent_to_ducky(prompt)
    filename = "payload.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(payload)
        
    filepath = os.path.abspath(filename)
    print(f"{G}generated {filepath}{W}")
    input("\n[enter]")

def analyze_payload():
    raw_path = input("\nfile > ").strip().strip("'\"")
    filepath = os.path.abspath(os.path.expanduser(raw_path))

    if not os.path.exists(filepath):
        basename = os.path.basename(raw_path)
        found = None
        for root, _, files in os.walk(os.path.expanduser("~")):
            if basename in files:
                found = os.path.join(root, basename)
                break
        if found:
            filepath = found
        else:
            print(f"{R}file not found{W}")
            input("\n[enter]")
            return

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().splitlines()

    errors = 0
    total_delay = 0
    warnings = []

    lines = [l.strip() for l in content if l.strip()]

    if len(lines) > 0 and not lines[0].upper().startswith("DELAY") and not lines[0].upper().startswith("REM"):
        warnings.append("missing initial DELAY (add DELAY 1000 at line 1)")

    for i, line in enumerate(lines):
        parts = line.split(maxsplit=1)
        cmd = parts[0].upper()

        if cmd not in VALID_CMDS:
            print(f"{R}[line {i+1}] unknown command '{cmd}'{W}")
            errors += 1
            continue

        if cmd in ["DELAY", "DEFAULT_DELAY", "DEFAULTDELAY"]:
            if len(parts) < 2 or not parts[1].isdigit():
                print(f"{R}[line {i+1}] invalid DELAY parameter{W}")
                errors += 1
            else:
                total_delay += int(parts[1])

        if cmd in ["GUI", "WINDOWS"]:
            next_line = lines[i+1].upper() if i + 1 < len(lines) else ""
            if not next_line.startswith("DELAY"):
                warnings.append(f"line {i+1}: add DELAY >= 400ms after {cmd}")
            else:
                next_parts = next_line.split(maxsplit=1)
                if len(next_parts) > 1 and next_parts[1].isdigit():
                    val = int(next_parts[1])
                    if val < 300:
                        warnings.append(f"line {i+2}: low DELAY ({val}ms), recommend >= 400ms")

    print(f"\ntarget: {filepath}")
    print(f"lines: {len(lines)}")
    print(f"errors: {R if errors else G}{errors}{W}")
    print(f"total delay: {total_delay}ms ({total_delay/1000:.2f}s)")

    if warnings:
        print("\nsuggestions:")
        for w in warnings:
            print(f" - {w}")

    input("\n[enter]")
    
def main():
    while True:
        print_banner()
        print("1. generate")
        print("2. analyze")
        print("3. exit")
        
        choice = input(f"\n{C}krypt0n{W}:~$ ").strip()
        
        if choice == "1":
            generate_payload()
        elif choice == "2":
            analyze_payload()
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
