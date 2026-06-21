import os
import requests
import logging
import geocoder  # 🌟 Live location track karne ke liye naya package
from dotenv import load_dotenv
from livekit.agents import function_tool

load_dotenv()

