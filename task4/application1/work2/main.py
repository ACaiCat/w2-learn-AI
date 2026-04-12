import classifier
from classifier.message import Message

def main():
    result = classifier.classify_mood(
        messages=[
            Message(text="今天草到男娘了！"),
            Message(img_path="data/1.jpg")
        ]
    )
    print(result)
    img = result.get_meme()
    img.show()

if __name__ == "__main__":
    main()
