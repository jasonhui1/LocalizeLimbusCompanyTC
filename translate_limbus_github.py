import os
import json
from opencc import OpenCC

# Initialize the converter (Simplified to Traditional Chinese)
# 's2t.json' means Simplified Chinese to Traditional Chinese (Taiwan standard)
# You can also use 's2hk.json' for Hong Kong standard or 's2twp.json' for Taiwan standard with phrases
converter = OpenCC('s2t')

def translate_value(value):
    """
    Recursively translates string values in a nested structure (dict or list).
    """
    if isinstance(value, str):
        # Only translate non-empty strings
        if value.strip():
            return converter.convert(value)
        return value
    elif isinstance(value, dict):
        return {k: translate_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [translate_value(item) for item in value]
    else:
        return value

def process_json_file(file_path):
    """
    Opens, translates, and saves a JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Skipping non-JSON or corrupted file: {file_path}")
        return
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    translated_data = translate_value(data)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            # ensure_ascii=False to keep CJK characters as is, not as \uXXXX escapes
            # indent=2 for pretty printing, matching the sample's style
            json.dump(translated_data, f, ensure_ascii=False, indent=2)
        print(f"Processed and translated: {file_path}")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")

def main():
    """
    Main function to get folder input and start processing.
    """
    # while True:
    #     folder_path = input("Enter the path to the folder containing JSON files: ")
    #     if os.path.isdir(folder_path):
    #         break
    #     else:
    #         print("Invalid folder path. Please enter a valid path.")

    folder_path = 'LLC_zh-CN'
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.json'):
                file_path = os.path.join(root, filename)
                process_json_file(file_path)

    print("\nTranslation process completed.")

if __name__ == "__main__":
    main()