import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Progressive Disclosure Evaluator")
    parser.add_argument('--view_schema', type=str, required=True, help='JSON representation of fields in a single view: {"view_name": "Settings", "visible_fields": 12}')
    
    args = parser.parse_args()
    try:
        view = json.loads(args.view_schema)
        visible_fields = view.get('visible_fields', 0)
        
        is_overloaded = visible_fields > 7
        
        print(json.dumps({
            "view_name": view.get('view_name', 'Unknown'),
            "visible_fields": visible_fields,
            "is_overloaded": is_overloaded,
            "recommendation": "Fields exceed cognitive limit. Move advanced settings to an 'Advanced' accordion or split into a multi-step Wizard." if is_overloaded else "Field count is acceptable."
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
