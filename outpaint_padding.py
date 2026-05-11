print("HB_OutpaintPadding loaded")


class HB_OutpaintPadding:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {

                "image": ("IMAGE",),

                "target_width": (
                    "INT",
                    {
                        "default": 1920,
                        "min": 1,
                        "max": 16384,
                        "step": 1
                    }
                ),

                "target_height": (
                    "INT",
                    {
                        "default": 1080,
                        "min": 1,
                        "max": 16384,
                        "step": 1
                    }
                ),
            }
        }

    RETURN_TYPES = (
        "INT",
        "INT",
        "INT",
        "INT"
    )

    RETURN_NAMES = (
        "left",
        "right",
        "top",
        "bottom"
    )

    FUNCTION = "calculate"

    CATEGORY = "HB"

    def calculate(
        self,
        image,
        target_width,
        target_height
    ):

        height = image.shape[1]
        width = image.shape[2]

        current_ratio = width / height
        target_ratio = target_width / target_height

        left = 0
        right = 0
        top = 0
        bottom = 0

        # Expand width
        if current_ratio < target_ratio:

            new_width = round(
                height * target_ratio
            )

            total_padding = (
                new_width - width
            )

            left = total_padding // 2

            right = (
                total_padding - left
            )

        # Expand height
        elif current_ratio > target_ratio:

            new_height = round(
                width / target_ratio
            )

            total_padding = (
                new_height - height
            )

            top = total_padding // 2

            bottom = (
                total_padding - top
            )

        return (
            int(left),
            int(right),
            int(top),
            int(bottom)
        )