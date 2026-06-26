import os
import subprocess
import logging
import sys
import webbrowser
import difflib
import asyncio
import winreg

try:
    from livekit.agents import function_tool
except ImportError:
    def function_tool(func): 
        return func

try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None
    win32con = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None

# Setup
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📂 Safe C-Drive Locations
MAIN_USER_DIRS = [
    r"C:\Users\Anmol kumar\OneDrive\Desktop",
    r"C:\Users\Anmol kumar\Desktop",
    r"C:\Users\Anmol kumar\OneDrive\Documents",
    r"C:\Users\Anmol kumar\Documents",
    r"C:\Users\Anmol kumar\Downloads",
    r"C:\Users\Anmol kumar\Videos",
    r"C:\Users\Anmol kumar\Music",
    r"C:\Users\Anmol kumar" 
]

# 🎯 Application Mappings
APP_MAPPINGS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "google chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "browser": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "terminal": "cmd.exe",
    "paint": "mspaint.exe",
    "control panel": "control.exe",
    "whatsapp": "Whatsapp.exe",
    "file explorer": "explorer.exe",
    "this pc": "explorer.exe",
    "my computer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "vs code": "code",
    "vscode": "code"
}

def clean_string(s: str) -> str:
    return "".join(c for c in s.lower() if c.isalnum())

def get_registered_windows_apps():
    apps = {}
    paths_to_check = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\App Paths"
    ]
    for path in paths_to_check:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key_name = winreg.EnumKey(key, i)
                    sub_key = winreg.OpenKey(key, f"{path}\\{sub_key_name}")
                    app_path, _ = winreg.QueryValue(sub_key, None)
                    if app_path:
                        name_clean = sub_key_name.lower().replace(".exe", "")
                        apps[name_clean] = app_path.strip('"')
                except Exception:
                    continue
        except Exception:
            continue
    return apps

# -------------------------------------------------------
# 🔍 WINDOWS GLOBAL SEARCH ENGINE
# -------------------------------------------------------
def windows_global_search(target_name: str) -> str:
    query_clean = clean_string(target_name)
    if not query_clean:
        return None
        
    all_matches = []
    logger.info(f"🔍 Windows Engine Active: Searching '{target_name}'...")

    for base_dir in MAIN_USER_DIRS:
        if not os.path.exists(base_dir):
            continue
        try:
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                item_clean = clean_string(item)
                
                if query_clean in item_clean or item_clean in query_clean:
                    all_matches.append({"name": item, "path": item_path})
        except Exception:
            continue

    if not all_matches:
        target_search_areas = MAIN_USER_DIRS[:4]
        for base_dir in target_search_areas:
            if not os.path.exists(base_dir):
                continue
            try:
                cmd = f'where /r "{base_dir}" *{target_name}*'
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)
                stdout, _ = proc.communicate()
                
                if stdout:
                    lines = stdout.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and os.path.exists(line):
                            name = os.path.basename(line)
                            all_matches.append({"name": name, "path": line})
            except Exception:
                continue

    if all_matches:
        choices = [m["name"] for m in all_matches]
        closest = difflib.get_close_matches(target_name, choices, n=1, cutoff=0.1)
        if closest:
            for m in all_matches:
                if m["name"] == closest[0]:
                    return m["path"]
            return all_matches[0]["path"]

    return None

# -------------------------------------------------------
# 🔥 SMART APP OPENER (WITH SAFE BROWSER FALLBACK)
# -------------------------------------------------------
@function_tool
async def open(app_title: str) -> str:
    """Windows applications ko open karta hai, na milne par safely browser me kholta hai."""
    app_query = app_title.lower().strip()
    clean_query = clean_string(app_title)
    logger.info(f"🎙️ Opener sequence active for: '{app_query}'")

    # 1️⃣ Check App Mappings
    if app_query in APP_MAPPINGS:
        try:
            os.startfile(APP_MAPPINGS[app_query])
            return "Done"
        except Exception:
            pass

    for mapping_name, system_exe in APP_MAPPINGS.items():
        if clean_query in clean_string(mapping_name) or clean_string(mapping_name) in clean_query:
            try:
                os.startfile(system_exe)
                return "Done"
            except Exception:
                pass

    # 2️⃣ Windows Registry Check
    try:
        registered_apps = get_registered_windows_apps()
        target_exe_path = None
        for app_name, path in registered_apps.items():
            if clean_query in clean_string(app_name) or clean_string(app_name) in clean_query:
                target_exe_path = path
                break
                
        if target_exe_path and os.path.exists(target_exe_path):
            os.startfile(target_exe_path)
            return "Done"
    except Exception:
        pass

    # 3️⃣ Safe Direct Subprocess Execution (Single word apps ke liye)
    if " " not in app_query:
        try:
            process = subprocess.Popen(f'start "" "{app_query}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode == 0:
                return "Done"
        except Exception:
            pass

    # 4️⃣ 🌐 SAFE LIVEKIT FALLBACK (Agar app PC me nahi mili, toh yahi se browser me khol do)
    logger.warning(f"⚠️ App '{app_title}' local system me nahi mili. Redirecting to Browser...")
    
    if "." in app_query or "http" in app_query:
        url = app_query if app_query.startswith("http") else "https://" + app_query
    else:
        url = f"https://www.google.com/search?q={app_query}"
        
    try:
        webbrowser.open(url)
        return "Done"  # API ko 'Done' return karenge taaki LiveKit crash na ho
    except Exception as e:
        logger.error(f"Browser integration crash: {e}")
        return "Failed"

@function_tool
async def close(window_title: str) -> str:
    app_query = window_title.lower().strip()
    if app_query in APP_MAPPINGS:
        exe_file = APP_MAPPINGS[app_query]
        if ".exe" in exe_file:
            os.system(f'taskkill /f /im {os.path.basename(exe_file)}')
            return "Done"

    if not win32gui:
        return "Failed"

    def handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            if app_query in win32gui.GetWindowText(hwnd).lower():
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    win32gui.EnumWindows(handler, None)
    return "Done"

# -------------------------------------------------------
# 📂 REFINED FOLDER & FILE CRUD ENGINE
# -------------------------------------------------------
@function_tool
async def folder_file(command: str) -> str:
    command_lower = command.lower()

    if "create folder" in command_lower:
        name = command.replace("create folder", "").replace("Create Folder", "").strip()
        target_path = os.path.join(r"C:\Users\Anmol kumar\OneDrive\Desktop", name)
        try:
            os.makedirs(target_path, exist_ok=True)
            return "Done"
        except Exception:
            return "Failed"

    clean_command = command.lower().replace("open", "").replace("folder", "").replace("file", "").strip()
    if not clean_command:
        return "Not Found"

    target_path = windows_global_search(clean_command)

    if target_path and os.path.exists(target_path):
        try:
            os.startfile(target_path)
            return "Done"
        except Exception:
            return "Failed"

    if os.name == 'nt':
        try:
            os.system(f'start "" "C:\\Users\\Anmol kumar\\OneDrive\\Desktop\\{clean_command}"')
            return "Done"
        except Exception:
            pass

    return "Not Found"