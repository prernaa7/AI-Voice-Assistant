import enum
from typing import Annotated
from livekit.agents import llm
import logging

# Setting up logger for home control
logger = logging.getLogger("home-control")
logger.setLevel(logging.INFO)

class Zone(enum.Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"

class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        # Initializing the state for music and lights functionalities
        self.lights = {
            Zone.LIVING_ROOM: False,
            Zone.BEDROOM: False,
            Zone.KITCHEN: False,
            Zone.BATHROOM: False,
            Zone.OFFICE: False,
        }

        self.music_playing = {
            Zone.LIVING_ROOM: False,
            Zone.BEDROOM: False,
            Zone.KITCHEN: False,
            Zone.BATHROOM: False,
            Zone.OFFICE: False,
        }

    # Light Control Functions
    @llm.ai_callable(description="Turn on or off the light in a specific room")
    def control_lights(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")], status: Annotated[bool, llm.TypeInfo(description="True to turn on, False to turn off")]):
        logger.info("Control lights - zone %s, status: %s", zone, status)
        self.lights[zone] = status  # Directly using the zone as it's already of type Zone
        action = "on" if status else "off"
        return f"The light in the {zone.value} is now {action}."

    # Music Control Functions
    @llm.ai_callable(description="Play or pause music in a specific room")
    def control_music(self, zone: Annotated[Zone, llm.TypeInfo(description="The specific zone")], action: Annotated[str, llm.TypeInfo(description="play or pause")]):
        if action.lower() == "play":
            self.music_playing[zone] = True
            logger.info("Music started in zone: %s", zone)
            return f"Music is now playing in the {zone.value}."
        elif action.lower() == "pause":
            self.music_playing[zone] = False
            logger.info("Music paused in zone: %s", zone)
            return f"Music is paused in the {zone.value}."
        else:
            logger.warning("Invalid action: %s for zone: %s", action, zone)
            return "Invalid action. Please say 'play' or 'pause'."
