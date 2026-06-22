# import os
# import subprocess
# import sys
# import logging
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
#                 match = difflib.get_close_matches(query, choices, n=1, cutoff=0.0)
#                 if not match:
#                     return (None, 0)
#                 best = match[0]
#                 score = int(difflib.SequenceMatcher(None, query, best).ratio() * 100)
#                 return (best, score)

#         process = _SimpleProcess
# from livekit.agents import function_tool
# import asyncio
# try:
#     import pygetwindow as gw
# except ImportError:
#     gw = None

# sys.stdout.reconfigure(encoding='utf-8')


# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# async def focus_window(title_keyword: str) -> bool:
#     if not gw:
#         logger.warning("⚠ pygetwindow")
#         return False

#     await asyncio.sleep(1.5)
#     title_keyword = title_keyword.lower().strip()

#     for window in gw.getAllWindows():
#         if title_keyword in window.title.lower():

#             if window.isMinimized:
#                 window.restore()
#             window.activate()
#             logger.info(f"🪟 window focus में है: {window.title}")
#             return True
#     logger.warning("⚠ Focus करने के लिए window नहीं मिली।")
#     return False

# async def index_files(base_dirs):
#     file_index = []
#     for base_dir in base_dirs:
#         for root, _, files in os.walk(base_dir):
#             for f in files:
#                 file_index.append({
#                     "name": f,
#                     "path": os.path.join(root, f),
#                     "type": "file"
#                 })
#     logger.info(f"✅ {base_dirs} से कुल {len(file_index)} files को index किया गया।")
#     return file_index

# async def search_file(query, index):
#     choices = [item["name"] for item in index]
#     if not choices:
#         logger.warning("⚠ Match करने के लिए कोई files नहीं हैं।")
#         return None

#     best_match, score = process.extractOne(query, choices)
#     logger.info(f"🔍 Matched '{query}' to '{best_match}' (Score: {score})")
#     if score > 70:
#         for item in index:
#             if item["name"] == best_match:
#                 return item
#     return None

# async def open_file(item):
#     try:
#         logger.info(f"📂 File खोल रहे हैं: {item['path']}")
#         if os.name == 'nt':
#             os.startfile(item["path"])
#         else:
#             subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', item["path"]])
#         await focus_window(item["name"])  # 👈 Focus window after opening
#         return f"✅ File open हो गई।: {item['name']}"
#     except Exception as e:
#         logger.error(f"❌ File open करने में error आया।: {e}")
#         return f"❌ File open करने में विफल रहा। {e}"

# async def handle_command(command, index):
#     item = await search_file(command, index)
#     if item:
#         return await open_file(item)
#     else:
#         logger.warning("❌ File नहीं मिली।")
#         return "❌ File नहीं मिली।"

# @function_tool
# async def Play_file(name: str) -> str:
#     folders_to_index = ["D:/"]
#     index = await index_files(folders_to_index)
#     command = name.strip()
#     return await handle_command(command, index)








import os
import subprocess
import sys
import logging
import asyncio
import difflib

try:
    import pygetwindow as gw
except ImportError:
    gw = None

from livekit.agents import function_tool

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========================================================
# SUPER FAST RECURSIVE SEARCH (Seemit depth ke sath)
# ========================================================
def clean_string(s: str) -> str:
    """Spaces aur special characters hata kar string ko saaf karta hai"""
    return "".join(c for c in s.lower() if c.isalnum())

async def fast_find_item(base_dirs, target_name):
    """Poori drive scan karne ke bajaye targeted folder search karega"""
    target_clean = clean_string(target_name)
    matched_items = []

    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
        try:
            # Sirf 2 ya 3 level andar tak check karega taaki network loop block na ho
            for entry in os.scandir(base_dir):
                entry_clean = clean_string(entry.name)
                
                # Agar user ka bola naam folder/file ke naam ke andar match hota hai
                if target_clean in entry_clean or entry_clean in target_clean:
                    matched_items.append({
                        "name": entry.name,
                        "path": entry.path,
                        "is_dir": entry.is_dir()
                    })
                
                # Agar folder hai 