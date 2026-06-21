import os
import requests
import logging
import geocoder  # 🌟 Live location track karne ke liye naya package
from dotenv import load_dotenv
from livekit.agents import function_tool

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exact_live_location() -> str:
    """Yeh function user ki actual live GPS/Wi-Fi location track karega"""
    try:
        logger.info("📡 Live GPS/Wi-Fi location track karne ki koshish ki ja rahi hai...")
        
        # 'me' ka matlab hai ki yeh machine ki current live location nikaalega
        g = geocoder.ip('me') 
        
        if g.ok and g.city:
            logger.info(f"📍 Live Location se mila shahar: {g.city}, {g.state}, {g.country}")
            return g.city
        else:
            logger.warning("⚠️ Live location fail hui, IP API ka use kiya ja raha hai.")
            return detect_city_by_ip()  # Backup agar geocoder fail ho jaye
    except Exception as e:
        logger.error(f"❌ Live location nikalne me error: {e}")
        return detect_city_by_ip()

def detect_city_by_ip() -> str:
    """Backup IP-based city detection"""
    try:
        logger.info("🌐 IP ke zariye shahar detect kiya ja raha hai...")
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city")
        if city:
            logger.info(f"IP se shahar mila: {city}")
            return city
        else:
            logger.warning("City detect karne me viphal, default 'Delhi' istemal ho raha hai.")
            return "Delhi"
    except Exception as e:
        logger.error(f"IP se city detect karne me error aya: {e}")
        return "Delhi"

@function_tool
async def get_weather(city: str = "") -> str:
    """
    Fetches the current weather. 
    If a city name is given, it fetches weather for that city.
    If no city name is given, it automatically tracks your live location and shows the weather.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    