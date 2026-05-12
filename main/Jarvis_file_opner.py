import os
import subprocess
import sys
import logging
from fuzzywuzzy import process
from livekit.agents import function_tool
import asyncio
try:
    import pygetwindow as gw
except ImportError:
    gw = None

sys.stdout.reconfigure(encoding='utf-8')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def focus_window(title_keyword: str) -> bool:
    if not gw:
        logger.warning("⚠ pygetwindow")
        return False

    await asyncio.sleep(1.5)
    title_keyword = title_keyword.lower().strip()

    for window in gw.getAllWindows():
        if title_keyword in window.title.lower():

            if window.isMinimized:
                window.restore()
            window.activate()
            logger.info(f"🪟 window focus में है: {window.title}")
            return True
    logger.warning("⚠ Focus करने के लिए window नहीं मिली।")
    return False

async def index_files(base_dirs):
    file_index = []
    for base_dir in base_dirs:
        for root, _, files in os.walk(base_dir):
            for f in files:
                file_index.append({
                    "name": f,
                    "path": os.path.join(root, f),
                    "type": "file"
                })
    logger.info(f"✅ {base_dirs} से कुल {len(file_index)} files को index किया गया।")
    return file_index

async def search_file(query, index):
    choices = [item["name"] for item in index]
    if not choices:
        logger.warning("⚠ Match करने के लिए कोई files नहीं हैं।")
        return None

    best_match, score = process.extractOne(query, choices)
    logger.info(f"🔍 Matched '{query}' to '{best_match}' (Score: {score})")
    if score > 70:
        for item in index:
            if item["name"] == best_match:
                return item
    return None

async def open_file(item):
    try:
        logger.info(f"📂 File खोल रहे हैं: {item['path']}")
        if os.name == 'nt':
            os.startfile(item["path"])
        else:
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', item["path"]])
        await focus_window(item["name"])  # 👈 Focus window after opening
        return f"✅ File open हो गई।: {item['name']}"
    except Exception as e:
        logger.error(f"❌ File open करने में error आया।: {e}")
        return f"❌ File open करने में विफल रहा। {e}"

async def handle_command(command, index):
    item = await search_file(command, index)
    if item:
        return await open_file(item)
    else:
        logger.warning("❌ File नहीं मिली।")
        return "❌ File नहीं मिली।"

@function_tool
async def Play_file(name: str) -> str:
    folders_to_index = ["D:/"]
    index = await index_files(folders_to_index)
    command = name.strip()
    return await handle_command(command, index)








# import os
# import subprocess
# import sys
# import logging
# from fuzzywuzzy import process
# from livekit.agents import function_tool
# import asyncio
# try:
#     import pygetwindow as gw
# except ImportError:
#     gw = None

# sys.stdout.reconfigure(encoding='utf-8')

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # ------------------------
# # Focus a window
# # ------------------------
# async def focus_window(title_keyword: str) -> bool:
#     if not gw:
#         logger.warning("⚠ pygetwindow module missing")
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

# # ------------------------
# # Index files, folders, apps
# # ------------------------
# async def index_items(base_dirs):
#     item_index = []
#     for base_dir in base_dirs:
#         for root, _, files in os.walk(base_dir):
#             for f in files:
#                 full_path = os.path.join(root, f)
#                 item_index.append({
#                     "name": f,
#                     "path": full_path,
#                     "type": "file"
#                 })
#         # Include folders themselves
#         for root, dirs, _ in os.walk(base_dir):
#             for d in dirs:
#                 full_path = os.path.join(root, d)
#                 item_index.append({
#                     "name": d,
#                     "path": full_path,
#                     "type": "folder"
#                 })

#     # Add common apps from Start Menu
#     start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
#     for root, _, files in os.walk(start_menu):
#         for f in files:
#             if f.endswith(".lnk") or f.endswith(".exe"):
#                 item_index.append({
#                     "name": f,
#                     "path": os.path.join(root, f),
#                     "type": "app"
#                 })

#     logger.info(f"✅ Indexed {len(item_index)} items from {base_dirs} + Start Menu apps")
#     return item_index

# # ------------------------
# # Search logic
# # ------------------------
# async def search_item(query, index):
#     choices = [item["name"] for item in index]
#     if not choices:
#         logger.warning("⚠ Match करने के लिए कोई item नहीं हैं।")
#         return None

#     best_match, score = process.extractOne(query, choices)
#     logger.info(f"🔍 Matched '{query}' to '{best_match}' (Score: {score})")
#     if score > 70:
#         for item in index:
#             if item["name"] == best_match:
#                 return item
#     return None

# # ------------------------
# # Open file / folder / app
# # ------------------------
# async def open_item(item):
#     try:
#         logger.info(f"📂 Opening: {item['path']}")
#         if os.name == 'nt':  # Windows
#             if item['type'] in ["file", "folder"]:
#                 os.startfile(item["path"])
#             elif item['type'] == "app":
#                 # Use shell to run exe or shortcut
#                 subprocess.Popen(item["path"], shell=True)
#         else:
#             subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', item["path"]])

#         # Try to focus window if possible
#         await focus_window(item["name"])
#         return f"✅ Open हो गया: {item['name']}"
#     except Exception as e:
#         logger.error(f"❌ Open failed: {e}")
#         return f"❌ Open करने में विफल: {e}"

# # ------------------------
# # Handle command
# # ------------------------
# async def handle_command(command, index):
#     item = await search_item(command, index)
#     if item:
#         return await open_item(item)
#     else:
#         logger.warning("❌ Item नहीं मिली।")
#         return "❌ Item नहीं मिली।"

# # ------------------------
# # LiveKit function
# # ------------------------
# @function_tool
# async def Play_file(name: str) -> str:
#     # Include Desktop, Downloads, Documents + D: drive (if exists)
#     user_profile = os.environ.get("USERPROFILE", "")
#     folders_to_index = [
#         os.path.join(user_profile, "Desktop"),
#         os.path.join(user_profile, "Downloads"),
#         os.path.join(user_profile, "Documents"),
#         "D:/"
#     ]
#     index = await index_items(folders_to_index)
#     command = name.strip()
#     return await handle_command(command, index)