import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Jakob's Law UI Convention Checker")
    parser.add_argument('--ui_terms', type=str, required=True, help='JSON array of UI terms: ["Homepage", "Shopping Basket", "Log out"]')
    
    args = parser.parse_args()
    try:
        terms = json.loads(args.ui_terms)
        
        conventions = {
            "start": "home",
            "homepage": "home",
            "basket": "cart",
            "shopping basket": "cart",
            "log off": "log out",
            "sign off": "log out",
            "help me": "help",
            "contact us": "contact",
            "擐?": "擐?",
            "銝駁???: "擐?",
            "鞈潛蝐?: "鞈潛頠?,
            "?餃蝟餌絞": "?餃"
        }
        
        violations = []
        for term in terms:
            normalized = term.lower().strip()
            if normalized in conventions and conventions[normalized] != normalized:
                violations.append({"term": term, "suggested": conventions[normalized].title()})
                
        print(json.dumps({
            "terms_checked": len(terms),
            "violations_found": len(violations),
            "details": violations,
            "recommendation": "OK" if not violations else "Jakob's Law violation. Users expect standard UI terms. Please rename to standard conventions."
        }, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
