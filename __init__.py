import os
__version__ = "1.0.0"

from .wildcard_processor import HB_WildcardProcessor
from .tidy_string import HB_TidyString
from .text_preset_switch import HB_TextPresetSwitch

NODE_CLASS_MAPPINGS = {
    "HB_Wildcard Processor": HB_WildcardProcessor,
    "HB_TidyString": HB_TidyString,
    "HB_TextPresetSwitch": HB_TextPresetSwitch,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "HB_Wildcard Processor": "HB Wildcard Processor",
    "HB_TidyString": "HB Tidy String",
    "HB_TextPresetSwitch": "HB Text Preset Switch",
}

WEB_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    "web"
)