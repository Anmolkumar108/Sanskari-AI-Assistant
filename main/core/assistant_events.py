from main.core.ai_bridge import AIBridge


bridge = None


def initialize(ai_bridge):
    global bridge
    bridge = ai_bridge


def listening():
    if bridge:
        bridge.on_listening()


def thinking():
    if bridge:
        bridge.on_thinking()


def speaking():
    if bridge:
        bridge.on_speaking()


def idle():
    if bridge:
        bridge.on_idle()


def error(msg):
    if bridge:
        bridge.on_error(msg)