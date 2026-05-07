
class HB_TextPresetSwitch:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "BOOLEAN")
    RETURN_NAMES = ("string", "integer", "boolean")

    FUNCTION = "run"
    CATEGORY = "HB"

    def run(self, preset):

        # =========================
        # STRING
        # =========================
        string_value = str(preset)

        # =========================
        # INTEGER
        # =========================
        try:
            int_value = int(float(preset))
        except:
            int_value = 0

        # =========================
        # BOOLEAN
        # =========================
        bool_value = bool(int_value)

        return (
            string_value,
            int_value,
            bool_value
        )