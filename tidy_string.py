
import re

class HB_TidyString:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "tidy_enabled": (["enable", "disable"],),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tidied_text",)
    FUNCTION = "process"
    CATEGORY = "JN_Party"

    def process(self, text, tidy_enabled):
        if tidy_enabled == "disable":
            return (text,)

        # Step 1: replace newlines with comma + space
        text = re.sub(r'\n+', ', ', text)

        # Step 2: remove multiple commas and extra spaces after
        text = re.sub(r',\s*,+', ', ', text)

        # Step 3: remove any space directly before commas
        text = re.sub(r'\s+,', ',', text)

        # Step 4: ensure only one comma and space
        text = re.sub(r',+', ',', text)
        text = re.sub(r',\s*', ', ', text)

        # Step 5: collapse multiple spaces into one
        text = re.sub(r'\s{2,}', ' ', text)

        # Step 6: remove double empty quotes: ""
        text = re.sub(r'""', '', text)

        # Step 7: remove quoted underscores: "_"
        text = re.sub(r'"_"', '', text)

        # Step 8: remove standalone symbols like ! ? " if surrounded by whitespace or commas
        text = re.sub(r'(?<=\s)[!?"](?!\w)|(?<!\w)[!?"](?!\w)', '', text)

        # Step 9: remove any lingering multiple spaces again
        text = re.sub(r'\s{2,}', ' ', text)

        # Step 10: strip leading/trailing whitespace or commas
        text = text.strip(" ,\n\t")

        return (text,)
