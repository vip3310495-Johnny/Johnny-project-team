import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Z-Pattern Layout Validator for Dashboards/Landing Pages")
    parser.add_argument('--layout', type=str, required=True, help='JSON of elements and grid coords: {"logo": [0,0], "nav": [2,0], "hero": [1,1], "cta": [2,2]}')
    
    args = parser.parse_args()
    try:
        layout = json.loads(args.layout)
        
        points = []
        if "logo" in layout: points.append((layout["logo"], [0,0]))
        if "nav" in layout or "status" in layout: points.append((layout.get("nav", layout.get("status")), [2,0]))
        if "hero" in layout or "content" in layout: points.append((layout.get("hero", layout.get("content")), [1,1]))
        if "cta" in layout or "action" in layout: points.append((layout.get("cta", layout.get("action")), [2,2]))
        
        deviation = 0
        for actual, ideal in points:
            if actual:
                deviation += abs(actual[0] - ideal[0]) + abs(actual[1] - ideal[1])
                
        is_z_pattern = deviation <= 2
        
        print(json.dumps({
            "layout": layout,
            "z_pattern_deviation": deviation,
            "is_compliant": is_z_pattern,
            "recommendation": "OK" if is_z_pattern else "Layout violates Z-pattern natural eye movement. Move Logo to top-left [0,0], and final CTA to bottom-right [2,2]."
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
