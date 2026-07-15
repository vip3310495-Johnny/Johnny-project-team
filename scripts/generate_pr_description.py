import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate standard PR description for DQA.")
    parser.add_argument("--output", default="pr_description.md", help="Output file name")
    args = parser.parse_args()

    content = """# Pull Request / Handoff

## 1. Design Decisions
- (Explain briefly what was done and why)
- [ ] Architecture Guardianship: No anti-patterns introduced.
- [ ] Dependencies: No unnecessary packages added.
- [ ] Big-O Complexity: Optimal time/space complexity used.

## 2. Impact Radius
- [ ] Regression Check: Ensured existing logic is not broken.
- [ ] Critical Path: Is this a critical feature? (Yes/No)
- [ ] DB Migration / Schema Change: Is there a schema change? If yes, provide Rollback SQL below.
- **Rollback Plan:** (If deployment fails, how do we revert? e.g., git revert, specific commands)
- Known side effects: 

## 3. Self-Test & How to Run
- [ ] TDD/BDD verified against Spec.
- [ ] Coverage Check: PASS / FAIL
- [ ] Security Scan: PASS / FAIL
- **How to Run for DQA:** 
  1. (E.g., npm install)
  2. (E.g., Setup environment variables)
  3. (E.g., npm run dev)

## 4. Test Cases Suggestions for DQA
> 🚨 Suggestions for QA focus areas:
- Edge Case 1: (E.g., empty inputs, negative numbers)
- Edge Case 2: (E.g., network timeout)
"""
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ PR Description template generated at {args.output}")
    print("🎯 Please fill out this template and pass it to the DQA Agent.")

if __name__ == "__main__":
    main()
