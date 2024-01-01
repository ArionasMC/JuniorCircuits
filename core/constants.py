EMPTY_ID = 0
SOURCE_ID = 1
RESISTANCE_ID = 2
AMPEROMETER_ID = 3
VOLTOMETER_ID = 4
LINE_ID = 5
SWITCH_ID = 6
LED_ID = 7

ORIENTED_COMPONENT_IDS = [RESISTANCE_ID, AMPEROMETER_ID, VOLTOMETER_ID, SWITCH_ID, LED_ID]

DEFAULT_VOLTAGE = 5
DEFAULT_RESISTANCE = 10

POINT_SIZE = 20
POINT_COLOR = (161, 238, 189)
DELETE_COLOR = (215, 19, 19)

COMPONENT_SIZE = 48

LINE_THICKNESS = 4

VERTICAL_ROTATION = 90

# Pygame defaults
LEFT_CLICK = 1
RIGHT_CLICK = 3

def get_id_from_component(com):
    path = com.path
    if "source" in path:
        return SOURCE_ID
    elif "resistance" in path:
        return RESISTANCE_ID
    elif "amperometer" in path:
        return AMPEROMETER_ID
    elif "voltometer" in path:
        return VOLTOMETER_ID
    elif "switch" in path:
        return SWITCH_ID
    elif "led" in path:
        return LED_ID
    else:
        return EMPTY_ID