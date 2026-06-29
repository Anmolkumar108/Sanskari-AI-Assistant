# import pyautogui
# import asyncio
# import time
# from datetime import datetime
# from pynput.keyboard import Key, Controller as KeyboardController
# from pynput.mouse import Button, Controller as MouseController
# from typing import List
# from livekit.agents import function_tool

# # ---------------------
# # SafeController Class
# # ---------------------
# class SafeController:
#     def __init__(self):
#         self.active = False
#         self.activation_time = None
#         self.keyboard = KeyboardController()
#         self.mouse = MouseController()
#         self.valid_keys = set("abcdefghijklmnopqrstuvwxyz1234567890")
#         self.special_keys = {
#             "enter": Key.enter, "space": Key.space, "tab": Key.tab,
#             "shift": Key.shift, "ctrl": Key.ctrl, "alt": Key.alt,
#             "esc": Key.esc, "backspace": Key.backspace, "delete": Key.delete,
#             "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right,
#             "caps_lock": Key.caps_lock, "cmd": Key.cmd, "win": Key.cmd,
#             "home": Key.home, "end": Key.end,
#             "page_up": Key.page_up, "page_down": Key.page_down
#         }

#     def resolve_key(self, key):
#         return self.special_keys.get(key.lower(), key)

#     def log(self, action: str):
#         with open("control_log.txt", "a") as f:
#             f.write(f"{datetime.now()}: {action}\n")

#     def activate(self, token=None):
#         if token != "my_secret_token":
#             self.log("Activation attempt failed.")
#             return
#         self.active = True
#         self.activation_time = time.time()
#         self.log("Controller auto-activated.")

#     def deactivate(self):
#         self.active = False
#         self.log("Controller auto-deactivated.")

#     def is_active(self):
#         return self.active

#     async def move_cursor(self, direction: str, distance: int = 100):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         x, y = self.mouse.position
#         if direction == "left": self.mouse.position = (x - distance, y)
#         elif direction == "right": self.mouse.position = (x + distance, y)
#         elif direction == "up": self.mouse.position = (x, y - distance)
#         elif direction == "down": self.mouse.position = (x, y + distance)
#         await asyncio.sleep(0.2)
#         self.log(f"Mouse moved {direction}")
#         return f"🖱️ Moved mouse {direction}."

#     async def mouse_click(self, button: str = "left"):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         if button == "left": self.mouse.click(Button.left, 1)
#         elif button == "right": self.mouse.click(Button.right, 1)
#         elif button == "double": self.mouse.click(Button.left, 2)
#         await asyncio.sleep(0.2)
#         self.log(f"Mouse clicked: {button}")
#         return f"🖱️ {button.capitalize()} click."

#     async def scroll_cursor(self, direction: str, amount: int = 10):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         try:
#             if direction == "up": self.mouse.scroll(0, amount)
#             elif direction == "down": self.mouse.scroll(0, -amount)
#         except:
#             pyautogui.scroll(amount * 100)
#         await asyncio.sleep(0.2)
#         self.log(f"Mouse scrolled {direction}")
#         return f"🖱️ Scrolled {direction}"

#     async def type_text(self, text: str):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         for char in text:
#             if not char.isprintable():
#                 continue
#             try:
#                 self.keyboard.press(char)
#                 self.keyboard.release(char)
#                 await asyncio.sleep(0.05)
#             except Exception:
#                 continue
#         self.log(f"Typed text: {text}")
#         return f"⌨️ Typed: {text}"

#     async def press_key(self, key: str):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         if key.lower() not in self.special_keys and key.lower() not in self.valid_keys:
#             return f"❌ Invalid key: {key}"
#         k = self.resolve_key(key)
#         try:
#             self.keyboard.press(k)
#             self.keyboard.release(k)
#         except Exception as e:
#             return f"❌ Failed key: {key} — {e}"
#         await asyncio.sleep(0.2)
#         self.log(f"Pressed key: {key}")
#         return f"⌨️ Key '{key}' pressed."

#     async def press_hotkey(self, keys: List[str]):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         resolved = []
#         for k in keys:
#             if k.lower() not in self.special_keys and k.lower() not in self.valid_keys:
#                 return f"❌ Invalid key in hotkey: {k}"
#             resolved.append(self.resolve_key(k))

#         for k in resolved: self.keyboard.press(k)
#         for k in reversed(resolved): self.keyboard.release(k)
#         await asyncio.sleep(0.3)
#         self.log(f"Pressed hotkey: {' + '.join(keys)}")
#         return f"⌨️ Hotkey {' + '.join(keys)} pressed."

#     async def control_volume(self, action: str):
#         if not self.is_active(): return "🛑 Controller is inactive."
#         if action == "up": pyautogui.press("volumeup")
#         elif action == "down": pyautogui.press("volumedown")
#         elif action == "mute": pyautogui.press("volumemute")
#         await asyncio.sleep(0.2)
#         self.log(f"Volume control: {action}")
#         return f"🔊 Volume {action}."






import pyautogui
import asyncio
import time
from datetime import datetime
from typing import List
from livekit.agents import function_tool

# Safe Fail-Safe: Agar mouse ko screen ke bilkul corner (0,0) pe le jaoge, to script turant ruk jayegi (Safety ke liye)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05  # Har command ke beech halka sa delay taaki system freeze na ho

# ---------------------
# SafeController Class
# ---------------------
class SafeController:
    def __init__(self):
        self.active = False
        self.activation_time = None
        
        # PyAutoGUI standard keys mappings for validation
        self.valid_pyautogui_keys = set(pyautogui.KEYBOARD_KEYS)

    def log(self, action: str):
        # 🌟 UnicodeEncodeError Fix: utf-8 encoding lagayi hai taaki Hindi/Special characters safely log ho sakein
        with open("control_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {action}\n")

    def activate(self, token=None):
        if token != "my_secret_token":
            self.log("Activation attempt failed.")
            return
        self.active = True
        self.activation_time = time.time()
        self.log("Controller auto-activated.")

    def deactivate(self):
        self.active = False
        self.log("Controller auto-deactivated.")

    def is_active(self):
        return self.active

    # --- MOUSE CONTROLS ---
    async def move_cursor(self, direction: str, distance: int = 100):
        if not self.is_active(): return "🛑 Controller is inactive."
        x, y = pyautogui.position()
        if direction == "left": pyautogui.moveTo(x - distance, y, duration=0.1)
        elif direction == "right": pyautogui.moveTo(x + distance, y, duration=0.1)
        elif direction == "up": pyautogui.moveTo(x, y - distance, duration=0.1)
        elif direction == "down": pyautogui.moveTo(x, y + distance, duration=0.1)
        self.log(f"Mouse moved {direction}")
        return f"🖱️ Moved mouse {direction}."

    async def mouse_click(self, button: str = "left"):
        if not self.is_active(): return "🛑 Controller is inactive."
        if button == "left": pyautogui.click()
        elif button == "right": pyautogui.rightClick()
        elif button == "double": pyautogui.doubleClick()
        self.log(f"Mouse clicked: {button}")
        return f"🖱️ {button.capitalize()} click done."

    async def scroll_cursor(self, direction: str, amount: int = 10):
        if not self.is_active(): return "🛑 Controller is inactive."
        clicks = amount * 100
        if direction == "up": pyautogui.scroll(clicks)
        elif direction == "down": pyautogui.scroll(-clicks)
        self.log(f"Mouse scrolled {direction}")
        return f"🖱️ Scrolled {direction}"

    # --- FULL KEYBOARD CONTROLS ---
    async def type_text(self, text: str):
        """Pure text document ya search bar me likhne ke liye"""
        if not self.is_active(): return "🛑 Controller is inactive."
        
        # 🌟 Hindi text validation: Copy-Paste logic se Hindi text OS templates par perfect chalta hai
        try:
            import pyperclip
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
        except Exception:
            # Clipboard fail hone par standard typing manual execution
            pyautogui.write(text, interval=0.01)
            
        self.log(f"Typed text: {text}")
        return f"⌨️ Typed: {text}"

    async def press_key(self, key: str):
        """Single key press karne ke liye (e.g., 'enter', 'tab', 'space', 'backspace', 'f5')"""
        if not self.is_active(): return "🛑 Controller is inactive."
        
        k_lower = key.lower().strip()
        # standardizing names for LLM
        if k_lower in ["win", "cmd", "command"]: k_lower = "win"
        elif k_lower in ["ctrl", "control"]: k_lower = "ctrl"
        
        if k_lower not in self.valid_pyautogui_keys:
            return f"❌ Key '{key}' system support nahi karta."
            
        pyautogui.press(k_lower)
        self.log(f"Pressed key: {k_lower}")
        return f"⌨️ Key '{k_lower}' pressed successfully."

    async def press_hotkey(self, keys: List[str]):
        """Saare VIP shortcuts chalane ke liye (e.g., ['ctrl', 'c'], ['alt', 'tab'], ['win', 'r'])"""
        if not self.is_active(): return "🛑 Controller is inactive."
        
        cleaned_keys = []
        for k in keys:
            k_clean = k.lower().strip()
            if k_clean in ["win", "cmd", "command"]: k_clean = "win"
            elif k_clean in ["ctrl", "control"]: k_clean = "ctrl"
            
            if k_clean not in self.valid_pyautogui_keys:
                return f"❌ Shortcut me '{k}' key invalid hai."
            cleaned_keys.append(k_clean)
            
        pyautogui.hotkey(*cleaned_keys)
        self.log(f"Pressed hotkey: {' + '.join(cleaned_keys)}")
        return f"⌨️ Hotkey {' + '.join(cleaned_keys)} executed."

    async def hold_and_press(self, hold_key: str, press_key: str, times: int = 1):
        """Ek key ko daba kar doosri key ko baar baar press karna (e.g., Alt hold karke Tab dabana navigation ke liye)"""
        if not self.is_active(): return "🛑 Controller is inactive."
        
        h_key = hold_key.lower().strip()
        p_key = press_key.lower().strip()
        
        with pyautogui.hold(h_key):
            for _ in range(times):
                pyautogui.press(p_key)
                await asyncio.sleep(0.1)
                
        return f"⌨️ Held '{hold_key}' and pressed '{press_key}' {times} times."

    # --- ADVANCED OS CONTROLS ---
    async def control_volume(self, action: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        if action == "up": pyautogui.press("volumeup")
        elif action == "down": pyautogui.press("volumedown")
        elif action == "mute": pyautogui.press("volumemute")
        return f"🔊 Volume {action}."

    async def swipe_gesture(self, direction: str):
        if not self.is_active(): return "🛑 Controller is inactive."
        w, h = pyautogui.size()
        x, y = w // 2, h // 2
        if direction == "up": pyautogui.moveTo(x, y + 200); pyautogui.dragTo(x, y - 200, duration=0.3)
        elif direction == "down": pyautogui.moveTo(x, y - 200); pyautogui.dragTo(x, y + 200, duration=0.3)
        elif direction == "left": pyautogui.moveTo(x + 200, y); pyautogui.dragTo(x - 200, y, duration=0.3)
        elif direction == "right": pyautogui.moveTo(x - 200, y); pyautogui.dragTo(x + 200, y, duration=0.3)
        return f"🖱️ Swipe {direction} done."

# ------------------------------
# LiveKit Tool Wrappers Section
# ------------------------------

controller = SafeController()

async def with_temporary_activation(fn, *args, **kwargs):
    print(f"🔍 EXECUTION: {fn.__name__} | args: {args}")
    controller.activate("my_secret_token")
    
    # OS level par command register hone ke liye 100ms ka delay
    await asyncio.sleep(0.1) 
    result = await fn(*args, **kwargs)
    
    # Action complete hone ke baad deactivation se pehle buffer time
    await asyncio.sleep(0.5)
    controller.deactivate()
    return result

@function_tool
async def move_cursor_tool(direction: str, distance: int = 100):
    """Moves the mouse cursor (left, right, up, down)."""
    return await with_temporary_activation(controller.move_cursor, direction, distance)

@function_tool
async def mouse_click_tool(button: str = "left"):
    """Clicks mouse (left, right, double)."""
    return await with_temporary_activation(controller.mouse_click, button)

@function_tool
async def scroll_cursor_tool(direction: str, amount: int = 10):
    """Scrolls the screen up or down."""
    return await with_temporary_activation(controller.scroll_cursor, direction, amount)

@function_tool
async def type_text_tool(text: str):
    """Types standard sentences or texts strings sequentially."""
    return await with_temporary_activation(controller.type_text, text)

@function_tool
async def press_key_tool(key: str):
    """Presses any single keyboard key including special keys like 'enter', 'tab', 'space', 'backspace', 'escape' etc."""
    return await with_temporary_activation(controller.press_key, key)

@function_tool
async def press_hotkey_tool(keys: List[str]):
    """Executes key combinations/shortcuts like ['ctrl', 'alt', 'delete'] or ['win', 'r'] or ['ctrl', 't']."""
    return await with_temporary_activation(controller.press_hotkey, keys)

@function_tool
async def hold_and_press_tool(hold_key: str, press_key: str, times: int = 1):
    """Holds down one key (like 'alt') and presses another key multiple times (like 'tab') to navigate menus."""
    return await with_temporary_activation(controller.hold_and_press, hold_key, press_key, times)

@function_tool
async def control_volume_tool(action: str):
    """Controls system audio (up, down, mute)."""
    return await with_temporary_activation(controller.control_volume, action)

@function_tool
async def swipe_gesture_tool(direction: str):
    """Performs a drag/swipe gesture on screen."""
    return await with_temporary_activation(controller.swipe_gesture, direction)