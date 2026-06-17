from dotenv import load_dotenv
import os
from mss import mss
from PIL import Image
from google import genai
from livekit.agents import function_tool

load_dotenv()

@function_tool
async def analyze_screen() -> str:

    try:

        api_key = os.getenv("GOOGLE_API_KEY")

        client = genai.Client(
            api_key=api_key
        )

        with mss() as sct:

            monitor = sct.monitors[1]

            shot = sct.grab(monitor)

            img = Image.frombytes(
                "RGB",
                shot.size,
                shot.rgb
            )

        