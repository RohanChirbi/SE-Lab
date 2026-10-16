"""Manage smart home devices and save their current state as JSON."""

from copy import deepcopy
import json
import math

HUB_HOST = "127.0.0.1"
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
DEVICES = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Add a supported device with its own independent settings."""
    if kind not in POWER_USAGE:
        raise ValueError(f"Unsupported device type: {kind}")
    if settings is not None and not isinstance(settings, dict):
        raise TypeError("Settings must be a dictionary or None.")

    DEVICES[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": deepcopy(settings) if settings is not None else {},
    }


def toggle_device(device_name):
    """Toggle a device, returning its new state or None if missing."""
    if device_name not in DEVICES:
        print(f"Device not found: {device_name}")
        return None

    device = DEVICES[device_name]
    device["on"] = not device["on"]
    return device["on"]


def set_temperature(device_name, value):
    """Set a thermostat temperature, clamped to 16–30 degrees."""
    if device_name not in DEVICES:
        print(f"Device not found: {device_name}")
        return False

    device = DEVICES[device_name]
    if device["kind"] != "thermostat":
        print(f"{device_name} is not a thermostat")
        return False

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        print("Temperature must be a number.")
        return False

    if isinstance(value, float) and not math.isfinite(value):
        print("Temperature must be finite.")
        return False

    device["settings"]["temperature"] = min(max(value, 16), 30)
    return True


def devices_in_room(room):
    """Return the names of devices assigned to a room."""
    return [
        name for name, info in DEVICES.items()
        if info["room"] == room
    ]


def power_usage():
    """Return total power consumption in watts for active devices."""
    return sum(
        POWER_USAGE[info["kind"]]
        for info in DEVICES.values()
        if info["on"]
    )


def save_state(file_name="home_state.json"):
    """Save device state as UTF-8 JSON; propagate write errors."""
    with open(file_name, "w", encoding="utf-8") as state_file:
        json.dump(DEVICES, state_file, indent=2)


def hub_address():
    """Return the configured local hub address."""
    return f"{HUB_HOST}:{HUB_PORT}"


def main():
    """Demonstrate device control, room listing, and persistence."""
    DEVICES.clear()
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")

    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)

    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())
    print("Light settings:", DEVICES["Ceiling Light"]["settings"])
    print(
        "Devices on:",
        [name for name, info in DEVICES.items() if info["on"]],
    )
    save_state()


if __name__ == "__main__":
    main()
