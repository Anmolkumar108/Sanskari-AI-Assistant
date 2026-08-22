import asyncio
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    AgentSession,
    Agent,
    RoomInputOptions,
)

from livekit.plugins import google

# Step 68: Import IPCClient
from main.core.ipc.ipc_client import IPCClient

# Some installations of `livekit` may not provide the `noise_cancellation`
# plugin. Import it defensively and provide a simple fallback so the
# rest of the script can run without raising ImportError.
try:
    from livekit.plugins import noise_cancellation
except Exception:
    class _NoiseCancellationStub:
        def BVC(self):
            # Return a harmless placeholder that `RoomInputOptions` can accept.
            return None

    noise_cancellation = _NoiseCancellationStub()

# =========================================
# LOCAL IMPORTS (Updated with main module prefix)
# =========================================

from main.vision_tool import analyze_screen

from main.Jarvis_google_search import (
    google_search,
    get_current_datetime,
)

from main.jarvis_get_whether import (
    get_weather,
)

from main.Jarvis_window_CTRL import (
    open,
    close,
    folder_file,
)

from main.Jarvis_file_opner import (
    Play_file,
)

from main.keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool,
)

from main.Jarvis_prompts import (
    SANSKARI_PROMPT,
)

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

# =========================================
# ASSISTANT
# =========================================

class Assistant(Agent):

    def __init__(self, ipc_client: IPCClient = None):

        self.ipc_client = ipc_client

        super().__init__(

            instructions=SANSKARI_PROMPT,

            tools=[
                # Search
                google_search,
                get_current_datetime,
                get_weather,

                # Window / App Control
                open,
                close,

                # File & Folder Control
                folder_file,
                Play_file,

                # Vision
                analyze_screen,

                # Mouse
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                swipe_gesture_tool,

                # Keyboard
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,

                # System
                control_volume_tool,
            ],
        )

# =========================================
# MAIN FUNCTION
# =========================================

async def entrypoint(ctx: agents.JobContext):

    print("💖 Sanskari AI Starting...")

    session = AgentSession(

        llm=google.beta.realtime.RealtimeModel(
            voice="Aoede",
            temperature=0.7,
        )
    )

    await ctx.connect()

    print("✅ Sanskari Connected Successfully!")

    # IPC Client Initialization & Status Broadcast
    client = IPCClient()
    client.send("log", "Agent Connected")
    client.send("agent", "online")
    client.send("connection", "Connected")
    client.send("state", "IDLE")
    client.send("internet", "Connected")
    client.send("mic", "Idle")
    client.send("tool", "None")

    try:
        await session.start(

            room=ctx.room,

            agent=Assistant(ipc_client=client),

            room_input_options=RoomInputOptions(

                noise_cancellation=None,

                video_enabled=False,
            ),
        )

        # =========================================
        # SESSION EVENTS & IPC INTEGRATION
        # =========================================
        @session.on("user_state_changed")
        def on_user_state(ev):
            print("🎤", ev)
            client.send("log", f"USER : {ev.new_state}")
            
            # Listening / Speaking status update
            if str(ev.new_state).lower() == "speaking":
                client.send("mic", "Listening")
            else:
                client.send("mic", "Idle")

        @session.on("agent_state_changed")
        def on_agent_state(ev):
            print("🤖", ev)
            state_str = str(ev.new_state).upper()
            client.send("state", state_str)

            if "LISTENING" in state_str:
                client.send("mic", "Listening")
            elif "THINKING" in state_str or "SPEAKING" in state_str:
                client.send("mic", "Speaking")
            else:
                client.send("mic", "Idle")

        @session.on("user_input_transcribed")
        def on_transcribed(ev):
            # Clean transcript extraction
            transcribed_text = getattr(ev, "transcript", "")

            print("=" * 60)
            print("TRANSCRIPT =", repr(transcribed_text))
            print("=" * 60)

            if transcribed_text:
                client.send("chat", transcribed_text)
                client.send("command", transcribed_text)

            if hasattr(ev, "transcript") and ev.transcript:
                client.send("user_message", ev.transcript)

        @session.on("speech_created")
        def on_speech(ev):
            client.send("log", "Assistant Speaking...")
            client.send("response", "Assistant Speaking...")

        @session.on("metrics_collected")
        def on_metrics(ev):
            pass

        # =========================================
        # NEW FUNCTION TOOLS EXECUTED EVENT
        # =========================================
        @session.on("function_tools_executed")
        def on_function_tools_executed(ev):

            print("========== FUNCTION TOOLS EXECUTED ==========")

            for call, output in ev.zipped():

                print("TOOL:", call.name)
                print("OUTPUT:", output)

                client.send("tool", "None")

                if call.name == "get_weather":

                    if output is not None:

                        weather = str(output.output)

                        print("WEATHER =", weather)

                        client.send("weather", weather)

        @session.on("agent_response_created")
        def on_response(ev):
            print("========== AGENT RESPONSE ==========")
            print(ev)
            print(vars(ev) if hasattr(ev, "__dict__") else "No __dict__")
            print("===================================")

            if hasattr(ev, "text") and ev.text:
                client.send("response", str(ev.text))
                client.send("assistant_message", str(ev.text))

        @session.on("error")
        def on_error(ev):
            print("❌ ERROR:", ev)
            client.send("log", f"ERROR: {str(ev)}")

        # INSTANT FIRST MESSAGE
        initial_msg = "Hello Anmol Sir ❤️"
        client.send("response", initial_msg)
        client.send("assistant_message", initial_msg)
        await session.generate_reply(
            instructions=initial_msg
        )

        while True:
            await asyncio.sleep(1)

    finally:
        # Agent disconnected / closed status update
        client.send("agent", "offline")
        client.send("connection", "Disconnected")

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    agents.cli.run_app(

        agents.WorkerOptions(
            entrypoint_fnc=entrypoint
        )
    )




# import os
# import logging
# from dotenv import load_dotenv

# from livekit import agents
# from vision_tool import analyze_screen
# from livekit.agents import (
#     AgentSession,
#     Agent,
#     RoomInputOptions,
# )

# # LiveKit real-time Gemini module support
# from livekit.plugins import google

# # Some installations of `livekit` may not provide the `noise_cancellation`
# # plugin. Import it defensively and provide a simple fallback so the
# # rest of the script can run without raising ImportError.
# try:
#     from livekit.plugins import noise_cancellation
# except Exception:
#     class _NoiseCancellationStub:
#         def BVC(self):
#             # Return a harmless placeholder that `RoomInputOptions` can accept.
#             return None

#     noise_cancellation = _NoiseCancellationStub()

# # =========================================
# # LOCAL IMPORTS
# # =========================================

# # Cleaned up imports with exact name matching for DuckDuckGo tool
# from Jarvis_google_search import (
#     google_search,
#     get_current_datetime,
# )

# from jarvis_get_whether import (
#     get_weather,
# )

# from Jarvis_window_CTRL import (
#     open,
#     close,
#     folder_file,
# )

# from Jarvis_file_opner import (
#     Play_file,
# )

# from keyboard_mouse_CTRL import (
#     move_cursor_tool,
#     mouse_click_tool,
#     scroll_cursor_tool,
#     type_text_tool,
#     press_key_tool,
#     swipe_gesture_tool,
#     press_hotkey_tool,
#     control_volume_tool,
# )

# from Jarvis_prompts import (
#     SANSKARI_PROMPT,
# )

# # =========================================
# # LOAD ENV
# # =========================================

# load_dotenv()

# # =========================================
# # ASSISTANT CLASS
# # =========================================

# class Assistant(Agent):

#     def __init__(self):

#         super().__init__(

#             instructions=SANSKARI_PROMPT,

#             tools=[
#                 # 🔍 Search & Environment Tools
#                 google_search,
#                 get_current_datetime,
#                 get_weather,      # Now supports auto live location check!

#                 # 🪟 Window / App Control
#                 open,
#                 close,

#                 # 📂 File & Folder Control
#                 folder_file,
#                 Play_file,

#                 # 👁️ Vision Capabilities
#                 analyze_screen,

#                 # 🖱️ Mouse Control Tools
#                 move_cursor_tool,
#                 mouse_click_tool,
#                 scroll_cursor_tool,
#                 swipe_gesture_tool,

#                 # ⌨️ Keyboard Control Tools
#                 type_text_tool,
#                 press_key_tool,
#                 press_hotkey_tool,

#                 # ⚙️ System Controls
#                 control_volume_tool,
#             ],
#         )

# # =========================================
# # MAIN ENTRYPOINT FUNCTION
# # =========================================

# async def entrypoint(ctx: agents.JobContext):

#     print("💖 Sanskari AI Starting...")

#     session = AgentSession(
#         llm=google.beta.realtime.RealtimeModel(
#             voice="Aoede",
#             temperature=0.7,
#         )
#     )

#     await ctx.connect()

#     print("✅ Sanskari Connected Successfully!")

#     await session.start(
#         room=ctx.room,
#         agent=Assistant(),
#         room_input_options=RoomInputOptions(
#             noise_cancellation=None,
#             video_enabled=False,
#         ),
#     )

#     # INSTANT FIRST WELCOME MESSAGE FOR ANMOL
#     await session.generate_reply(
#         instructions="Hello Anmol Sir ❤️"
#     )

# # =========================================
# # RUN APPLICATION WORKER
# # =========================================

# if __name__ == "__main__":

#     agents.cli.run_app(
#         agents.WorkerOptions(
#             entrypoint_fnc=entrypoint
#         )
#     )




