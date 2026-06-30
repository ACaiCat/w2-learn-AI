from typing import Any

import json_repair
from pydantic import ValidationError
from zai import ZhipuAiClient
from zai.core import StreamResponse

from .config import get_settings
from .partner import Partner
from .position import PosList

config = get_settings()

PROCESS_INTEL_PROMPT = f"""
你是一个蓝色星原的情报处理模型，你现在要把输入的情报转为角色JSON对象，直接输出JSON

请按照以下 JSON Schema 格式返回结果：
{Partner.model_json_schema()}
"""


def process_intel(intel: str) -> Partner:
    client = ZhipuAiClient(api_key=config.API_KEY)
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": PROCESS_INTEL_PROMPT,
        },
        {
            "content": intel,
            "role": "user"
        }
    ]
    attempt = 0
    while attempt < 10:
        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                thinking={
                    "type": "disabled"
                },
                response_format={"type": "json_object"},
                stream=True
            )
            assert isinstance(response, StreamResponse)
            result = ""
            for chunk in response:
                result += chunk.choices[0].delta.content
            partner = Partner.model_validate(json_repair.loads(result))
            return partner
        except ValidationError as e:
            errors = e.json()
            print("\n\n解析失败: ", errors)
            messages.append({
                "content": "解析失败，错误信息: " + errors +
                           "，完整输出，不要突然截断，请重新输出符合 JSON Schema 的结果，"
                           "我对你的期望很高，如果你下一次不能完整输出，那么我将会非常失望",
                "role": "user"
            })
            attempt += 1
        except Exception:
            raise

    raise Exception("解析失败超过最大重试次数")


EXTRACT_POS_PROMPT = f"""你是一个蓝色星原的情报处理模型，你现在要在遗迹JSON数据中提取所有火元素波奇的坐标
请按照以下 JSON Schema 格式返回结果：
{PosList.model_json_schema()}
"""

def extract_pos(ruin_intel: str) -> PosList:
    client = ZhipuAiClient(api_key=config.API_KEY)
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": EXTRACT_POS_PROMPT ,
        },
        {
            "content": ruin_intel,
            "role": "user"
        }
    ]
    attempt = 0
    while attempt < 10:
        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                thinking={
                    "type": "disabled"
                },
                response_format={"type": "json_object"},
                stream=True
            )
            assert isinstance(response, StreamResponse)
            result = ""
            for chunk in response:
                result += chunk.choices[0].delta.content
            partner = PosList.model_validate(json_repair.loads(result))
            return partner
        except ValidationError as e:
            errors = e.json()
            print("\n\n解析失败: ", errors)
            messages.append({
                "content": "解析失败，错误信息: " + errors +
                           "，完整输出，不要突然截断，请重新输出符合 JSON Schema 的结果，"
                           "我对你的期望很高，如果你下一次不能完整输出，那么我将会非常失望",
                "role": "user"
            })
            attempt += 1
        except Exception:
            raise

    raise Exception("解析失败超过最大重试次数")
