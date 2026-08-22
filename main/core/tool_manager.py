from main.core.event_bus import event_bus


class ToolManager:

    TOOLS = {
        "weather": ("Weather", "🌦"),
        "google_search": ("Google Search", "🔎"),
        "analyze_screen": ("Analyze Screen", "🖥"),
        "volume": ("Volume", "🔊"),
        "brightness": ("Brightness", "💡"),
        "folder_file": ("File Manager", "📁"),
        "play_file": ("Media Player", "🎵"),
        "keyboard": ("Keyboard", "⌨"),
        "mouse": ("Mouse", "🖱"),
    }

    @classmethod
    def start(cls, tool):

        name, icon = cls.TOOLS.get(
            tool,
            (tool, "⚙")
        )

        event_bus.tool_changed.emit(name)
        event_bus.tool_icon_changed.emit(icon)
        event_bus.tool_status_changed.emit("Running")

    @classmethod
    def finish(cls):

        event_bus.tool_status_changed.emit("Finished")