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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                """
                Screen ko analyze karo.

                Batao:
                1. User kya kar raha hai
                2. Kaunsi application open hai
                3. Koi error hai ya nahi
                4. Next step kya hona chahiye

                Hindi me jawab do.
                """,
                img,
            ],
        )

        return response.text

    except Exception as e:

        return f"Vision Error: {str(e)}"