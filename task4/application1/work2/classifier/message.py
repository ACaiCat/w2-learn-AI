import base64
from pathlib import Path

from pydantic import BaseModel


class Message(BaseModel):
    text: str = ""
    img_path: str = ""

    def to_content(self):
        if self.img_path:
            path = Path(self.img_path)
            base64_img = base64.b64encode(path.read_bytes()).decode("utf-8")
            return {
                "type": "image_url",
                "image_url": {
                    "url": base64_img
                }
            }
        else:
            return {
                "type": "text",
                "text": self.text
            }
