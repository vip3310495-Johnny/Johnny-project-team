import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(r, g, b):
    a = [v / 255 for v in [r, g, b]]
    a = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in a]
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def get_contrast_ratio(color1, color2):
    l1 = get_luminance(*hex_to_rgb(color1))
    l2 = get_luminance(*hex_to_rgb(color2))
    
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def main():
    parser = argparse.ArgumentParser(description="Visual Saliency & Contrast Checker for CTA Buttons")
    parser.add_argument('--button_color', type=str, required=True, help="Hex color of the button (e.g., #FF5733)")
    parser.add_argument('--bg_color', type=str, required=True, help="Hex color of the background (e.g., #FFFFFF)")
    parser.add_argument('--threshold', type=float, default=4.5, help="Minimum contrast ratio (WCAG AA is 4.5)")
    
    args = parser.parse_args()
    
    try:
        ratio = get_contrast_ratio(args.button_color, args.bg_color)
        is_salient = ratio >= args.threshold
        
        print(json.dumps({
            "button_color": args.button_color,
            "background_color": args.bg_color,
            "contrast_ratio": round(ratio, 2),
            "is_salient": is_salient,
            "recommendation": "OK" if is_salient else "Contrast too low. Please increase color difference or add whitespace."
        }, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
