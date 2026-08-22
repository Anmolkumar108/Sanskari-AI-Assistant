from main.core.event_bus import event_bus


def update_weather(weather_text):
    event_bus.weather_changed.emit(weather_text)