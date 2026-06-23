# import os
# import subprocess
# import logging
# import sys
# import asyncio
# import webbrowser
# try:
#     from fuzzywuzzy import process
# except Exception:
#     try:
#         from rapidfuzz import process
#     except Exception:
#         import difflib

#         class _SimpleProcess:
#             @staticmethod
#             def extractOne(query, choices):
#                 if not choices:
#                     return (None, 0)
#                 # Use difflib to find the closest match
#                 match = difflib.get_close_matches(query, choices, n=1, cutoff=0.0)
#                 if not match:
#                     return (None, 0)
#                 best = match[0]
#                 score = int(difflib.SequenceMatcher(None, query, best).ratio() * 100)
#                 return (best, score)

#         process = _SimpleProcess

# try:
#     from livekit.agents import function_tool
# except ImportError:
#     def function_tool(func): 
#         return func

# try:
#     import win32gui
#     import win32con
# except ImportError:
#     win32gui = None
#     win32con = None

# try:
#     import pygetwindow as gw
# except ImportError:
#     gw = None

# # Setup
# sys.stdout.reconfigure(encoding='utf-8')
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # App mappings (important apps ke liye)
# APP_MAPPINGS = {
#     "notepad": "notepad.exe",
#     "calculator": "calc.exe",
#     "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#     "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
#     "command prompt": "cmd.exe",
#     "paint": "mspaint.exe",
#     "control panel": "control.exe",
#     "WhatsApp": "Whatsapp.exe",
# }

# # -------------------------
# # Focus window
# # -------------------------
# async def focus_window(title_keyword: str) -> bool:
#     if not gw:
#         return False

#     await asyncio.sleep(1)
#     title_keyword = title_keyword.lower()

#     for window in gw.getAllWindows():
#         if title_keyword in window.title.lower():
#             if window.isMinimized:
#                 window.restore()
#             window.activate()
#             return True
#     return False

# # -------------------------
# # FILE SYSTEM
# # -------------------------
# async def index_items(base_dirs):
#     item_index = []
#     for base_dir in base_dirs:
#         for root, dirs, files in os.walk(base_dir):
#             for d in dirs:
#                 item_index.append({"name": d, "path": os.path.join(root, d), "type": "folder"})
#             for f in files:
#                 item_index.append({"name": f, "path": os.path.join(root, f), "type": "file"})
#     return item_index

# async def search_item(query, index, item_type):
#     filtered = [item for item in index if item["type"] == item_type]
#     choices = [item["name"] for item in filtered]

#     if not choices:
#         return None

#     best_match, score = process.extractOne(query, choices)

#     if score > 70:
#         for item in filtered:
#             if item["name"] == best_match:
#                 return item
#     return None

# async def open_folder(path):
#     try:
#         os.startfile(path)
#     except Exception as e:
#         return f"❌ Error: {e}"

# async def play_file(path):
#     try:
#         os.startfile(path)
#     except Exception as e:
#         return f"❌ Error: {e}"

# async def create_folder(path):
#     try:
#         os.makedirs(path, exist_ok=True)
#         return f"✅ Folder created: {path}"
#     except Exception as e:
#         return f"❌ Error: {e}"

# async def rename_item(old_path, new_path):
#     try:
#         os.rename(old_path, new_path)
#         return f"✅ Renamed to: {new_path}"
#     except Exception as e:
#         return f"❌ Error: {e}"

# async def delete_item(path):
#     try:
#         if os.path.isdir(path):
#             os.rmdir(path)
#         else:
#             os.remove(path)
#         return f"🗑️ Deleted: {path}"
#     except Exception as e:
#         return f"❌ Error: {e}"

# # -------------------------
# # 🔥 SMART APP OPEN
# # -------------------------
# @function_tool
# async def open(app_title: str) -> str:
#     app_title = app_title.lower().strip()

#     try:
#         # 1️⃣ Mapping
#         if app_title in APP_MAPPINGS:
#             os.startfile(APP_MAPPINGS[app_title])
#             return f"🚀 {app_title} open ho gaya (mapped)"

#         # 2️⃣ Direct open
#         try:
#             os.startfile(app_title)
#             return f"🚀 {app_title} open ho gaya"
#         except:
#             pass

#         # 3️⃣ Try .exe
#         try:
#             os.startfile(app_title + ".exe")
#             return f"🚀 {app_title}.exe open ho gaya"
#         except:
#             pass

#         # 4️⃣ Website open
#         if "." in app_title:
#             url = app_title if app_title.startswith("http") else "https://" + app_title
#             webbrowser.open(url)
#             return f"🌐 Website open: {url}"
#         else:
#             webbrowser.open(f"https://www.google.com/search?q={app_title}")
#             return f"🌐 {app_title} Google me open kiya"

#     except Exception as e:
#         return f"❌ Error: {e}"

# # -------------------------
# # CLOSE APP
# # -------------------------
# @function_tool
# async def close(window_title: str) -> str:
#     if not win32gui:
#         return "❌ win32gui not available"

#     def handler(hwnd, _):
#         if win32gui.IsWindowVisible(hwnd):
#             if window_title.lower() in win32gui.GetWindowText(hwnd).lower():
#                 win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

#     win32gui.EnumWindows(handler, None)
#     return f"❌ Closed: {window_title}"

# # -------------------------
# # COMMAND HANDLER
# # -------------------------
# @function_tool
# async def folder_file(command: str) -> str:
#     index = await index_items(["D:/"])
#     command_lower = command.lower()

#     if "create folder" in command_lower:
#         name = command.replace("create folder", "").strip()
#         return await create_folder(os.path.join("D:/", name))

#     if "rename" in command_lower:
#         parts = command_lower.replace("rename", "").split("to")
#         if len(parts) == 2:
#             old = parts[0].strip()
#             new = parts[1].strip()

#             item = await search_item(old, index, "folder")
#             if item:
#                 new_path = os.path.join(os.path.dirname(item["path"]), new)
#                 return await rename_item(item["path"], new_path)

#     if "delete" in command_lower:
#         item = await search_item(command, index, "folder") or await search_item(command, index, "file")
#         if item:
#             return await delete_item(item["path"])

#     if "open folder" in command_lower:
#         item = await search_item(command, index, "folder")
#         if item:
#             await open_folder(item["path"])
#             return f"📂 Folder opened: {item['name']}"

#     item = await search_item(command, index, "file")
#     if item:
#         await play_file(item["path"])
#         return f"📄 File opened: {item['name']}"

#     return "⚠ Kuch match nahi hua"




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

# 📂 Windows ke core profiles mapping list (From Code 1)
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

# 🎯 APP MAPPINGS & ALIASES (Dono codes ke keys ka dynamic fusion)
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
    """Spelling matching ke liye spaces aur symbols saaf karta hai"""
    return "".join(c for c in s.lower() if c.isalnum())

