import intel_to_json


def main():
    with open("data/ruin_data.json", "rt", encoding='utf-8') as f:
        data = f.read()

    pos = intel_to_json.extract_pos(data)

    with open("data/positions.json", "w", encoding="utf-8") as f:
        f.write(pos.model_dump_json())


if __name__ == "__main__":
    main()
