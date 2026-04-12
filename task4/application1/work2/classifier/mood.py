import random
from enum import StrEnum
from pathlib import Path

from PIL import Image


class Mood(StrEnum):
    HAPPY = "开心"
    SAD = "难过"
    ANGRY = "愤怒"
    NEUTRAL = "中性"

    def get_meme(self) -> Image.Image:
        module_folder = Path(__file__).parent

        def get_random_image(folder_name: str) -> Image.Image:
            folder = module_folder/ "memes" / folder_name
            images = list(folder.glob("*"))
            image = random.choice(images)
            return Image.open(image)

        match self:
            case Mood.HAPPY:
                return get_random_image("happy")
            case Mood.SAD:
                return get_random_image("sad")
            case Mood.ANGRY:
                return get_random_image("angry")
            case Mood.NEUTRAL:
                return get_random_image("neutral")
