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
