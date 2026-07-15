import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Poka-Yoke (Mistake-Proofing) Form Validator")
    parser.add_argument('--form_schema', type=str, required=True, help='JSON schema of form fields: [{"name": "email", "required": true, "has_validation": true, "has_error_msg": true}]')
    
    args = parser.parse_args()
    try:
        fields = json.loads(args.form_schema)
        violations = []
        
        for field in fields:
            if field.get('required') and not field.get('has_validation'):
                violations.append(f"Field '{field['name']}' is required but lacks validation logic.")
            if field.get('required') and not field.get('has_error_msg'):
                violations.append(f"Field '{field['name']}' is required but lacks an error message.")
                
        is_poka_yoke = len(violations) == 0
        
        print(json.dumps({
            "fields_analyzed": len(fields),
            "is_poka_yoke_compliant": is_poka_yoke,
            "violations": violations,
            "recommendation": "Ready for implementation." if is_poka_yoke else "Poka-Yoke failure. Fix form schema before rendering."
        }, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
