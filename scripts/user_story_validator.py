import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import re
import json

def main():
    parser = argparse.ArgumentParser(description="User Story Format Validator")
    parser.add_argument('--story', type=str, required=True, help='The user story text')
    
    args = parser.parse_args()
    
    en_pattern = r"(?i)As a (.+?), I want (?:to )?(.+?) so that (.+)"
    zh_pattern = r"頨怎(銝?銝???(.+?)嚗??唾?(.+?)嚗誑靘踵(.+)"
    
    en_match = re.search(en_pattern, args.story)
    zh_match = re.search(zh_pattern, args.story)
    
    is_valid = bool(en_match or zh_match)
    
    if en_match:
        role, action, benefit = en_match.groups()
    elif zh_match:
        _, role, action, benefit = zh_match.groups()
    else:
        role, action, benefit = None, None, None

    print(json.dumps({
        "story": args.story,
        "is_valid_format": is_valid,
        "role": role.strip() if role else None,
        "action": action.strip() if action else None,
        "benefit": benefit.strip() if benefit else None,
        "recommendation": "OK" if is_valid else "Invalid User Story format. Must follow 'As a... I want to... So that...' or '頨怎...?閬?..隞乩噶??..'"
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
