"""Useful functions to customize the streamlit app"""


def change_delta_color(delta: int) -> str:
    """Change the color of the delta in the metric component

    Args:
        delta (int): The delta value

    Returns:
        str: The color mode of the delta
    """
    if delta > 0:
        return "normal"
    elif delta < 0:
        return "inverse"
    else:
        return "off"


if __name__ == "__main__":
    change_delta_color()
