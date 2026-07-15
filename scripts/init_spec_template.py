import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a Requirement-to-Spec template.")
    parser.add_argument("--output", default="tech_spec_checklist.md", help="Output file name")
    args = parser.parse_args()

    content = """# Tech Spec Checklist

## 1. Vibe to Spec
- [ ] Requirements clarified: Did we convert the PM's vibe into solid logic?
- [ ] Edge cases defined: What happens during network failure, invalid input?

## 2. Defensive Architecture
- [ ] Dependencies check: Do we really need to add a new package?
- [ ] Security boundaries: No hardcoded API keys or Secrets.
- [ ] Critical Path analysis: Is this a core feature like payment or login? If so, mark as [CRITICAL].

## 3. Implementation Todo
- [ ] Step 1:
- [ ] Step 2:

## 4. Verification
- [ ] Automated Tests (Coverage > 80%)
- [ ] Error Handling and Sanitization tested
- [ ] Test Case Suggestions for DQA:"""
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Spec template generated at {args.output}")

if __name__ == "__main__":
    main()
