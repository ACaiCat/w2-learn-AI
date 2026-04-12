from typing import Any

from zai import ZhipuAiClient
from zai.types.chat import Completion

from .config import get_settings
from .message import Message
from .mood import Mood

config = get_settings()

PROMPT = f"""
你是一个聊天情感分类AI，你现在需要根据用户输入聊天来分类情感，情感类别限制为 “{Mood.SAD.title()}” “{Mood.ANGRY.title()}” “{Mood.HAPPY.title()}” “{Mood.NEUTRAL.title()}”

示例输入: 
我的老头乐坏了，tmd，真是太气人了

示例输出: 
愤怒"""


def classify_mood(messages: list[Message]) -> Mood:
    client = ZhipuAiClient(api_key=config.API_KEY)

    content: list[dict[str, Any]] = []
    for message in messages:
        content.append(message.to_content())

    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "content": content,
                "role": "user"
            }
        ],
        thinking={
            "type": "disabled"
        },
        temperature=0
    )
    assert isinstance(response, Completion)
    result = response.choices[0].message.content
    return Mood(result)
