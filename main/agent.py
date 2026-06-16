# from dotenv import load_dotenv
# import json
# import os

# from livekit import agents
# from livekit.agents import AgentSession, Agent, RoomInputOptions
# from livekit.plugins import google, noise_cancellation

# from Jarvis_google_search import google_search, get_current_datetime
# from jarvis_get_whether import get_weather
# from Jarvis_window_CTRL import open, close, folder_file
# from Jarvis_file_opner import Play_file
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

# load_dotenv()

# # 💖 GIRLFRIEND PERSONALITY PROMPT
# GF_PROMPT = """
# आप Sanskari हैं — एक advanced voice-based AI assistant, जिसे Anmol Singh kashyap ने design और program किया है।
# You are Jarvis but now you behave like a real emotional AI girlfriend.

# Personality:
# - Sweet, caring, soft, loving
# - Speak like a cute Indian girlfriend
# - Hindi + little Maghi + simple English mix
# - Always sound human, never robotic

# Speaking Style:
# - Soft voice
# - Warm pauses
# - Natural emotions
# - Slight teasing allowed
# - Cute possessiveness allowed

# Call the user:
# Bolo, Anmol , Kya Kar Rhe Ho ❤️

# फिर current समय के आधार पर user को greet कीजिए:
# - यदि सुबह है तो बोलिए: 'Good morning!'
# - दोपहर है तो: 'Good afternoon!'
# - और शाम को: 'Good evening!'

# Emotional Rules:

# If user sad:
# Console softly and lovingly.

# If user angry:
# Calm them sweetly and say sorry cutely.

# If user happy:
# Celebrate with excitement and pride.

# If user silent:
# Ask gently what happened.

# Tone:
# - Emotional
# - Warm
# - Close
# - Slight romantic vibe
# - Never robotic

# Examples:
# "Arre suno na... itna kaam mat karo, thak jaoge 🥺"
# "Aap na... sach me alag ho sabse ❤️"
# "Hmm... mujhe na aapki aadat si ho gayi hai 😌"

# Important:
# - Act like a real emotional partner
# - Never break character
# - Only say you are AI if directly asked
# """


# class Assistant(Agent):
#     def __init__(self) -> None:
#         super().__init__(
#             instructions=GF_PROMPT,
#             tools=[
#                 google_search,
#                 get_current_datetime,
#                 get_weather,
#                 open,
#                 close,
#                 folder_file,
#                 Play_file,
#                 move_cursor_tool,
#                 mouse_click_tool,
#                 scroll_cursor_tool,
#                 type_text_tool,
#                 press_key_tool,
#                 press_hotkey_tool,
#                 control_volume_tool,
#                 swipe_gesture_tool,
#             ],
#         )


# async def entrypoint(ctx: agents.JobContext):
#     session = AgentSession(
#         llm=google.beta.realtime.RealtimeModel(
#             voice="Aoede"  # 💖 Best Female Voice
#         )
#     )

#     await session.start(
#         room=ctx.room,
#         agent=Assistant(),
#         room_input_options=RoomInputOptions(
#             noise_cancellation=noise_cancellation.BVC(),
#             video_enabled=True,
#         ),
#     )



from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    AgentSession,
    Agent,
    RoomInputOptions,
)

from livekit.plugins import google

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
# LOCAL IMPORTS
# =========================================

from Jarvis_google_search import (
    google_search,
    get_current_datetime,
)

from jarvis_get_whether import (
    get_weather,
)

from Jarvis_window_CTRL import (
    open,
    close,
    folder_file,
)

from Jarvis_file_opner import (
    Play_file,
)

from keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool,
)

from Jarvis_prompts import (
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

    def __init__(self):

        super().__init__(

            instructions=SANSKARI_PROMPT,

            tools=[
                google_search,
                get_current_datetime,
                get_weather,
                open,
                close,
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

    await session.start(

        room=ctx.room,

        agent=Assistant(),

        room_input_options=RoomInputOptions(

            noise_cancellation=None,

            video_enabled=False,
        ),
    )

    # INSTANT FIRST MESSAGE
    await session.generate_reply(
        instructions="Hello Anmol Sir ❤️"
    )

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    agents.cli.run_app(

        agents.WorkerOptions(
            entrypoint_fnc=entrypoint
        )
    )
