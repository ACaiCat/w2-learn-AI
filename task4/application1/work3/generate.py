import json
from concurrent.futures import ThreadPoolExecutor

import intel_to_json

def main():
    with open("data/gen_intel_data.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    with open("data/kibots_data.jsonl", "w", encoding="utf-8") as f:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(intel_to_json.process_intel, intel) for intel in data]
            for future in futures:
                result = future.result()
                print(result)
                f.write(json.dumps(result.model_dump(mode="json"), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
