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
    