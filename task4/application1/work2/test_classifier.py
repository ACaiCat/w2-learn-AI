from dataclasses import dataclass

import classifier
from classifier.ai import Message, Mood
from pathlib import Path
    

def test_classify_mood():
    @dataclass
    class TestCase:
        messages: str
        img_path: Path
        expected_mood: Mood

    test_cases = [
            TestCase("今天草到男娘了！", Path("data/happy.jpg"), Mood.HAPPY),
            TestCase("气死了喵", Path("data/angry.jpg"), Mood.ANGRY),
            TestCase("今天上早八", Path("data/sad.png"), Mood.SAD),
    ]
    for case in test_cases:
        result = classifier.classify_mood(
            messages=[Message(text=case.messages), Message(img_path=str(case.img_path))],
        )
        assert result == case.expected_mood, f"Expected {case.expected_mood}, but got {result}"
