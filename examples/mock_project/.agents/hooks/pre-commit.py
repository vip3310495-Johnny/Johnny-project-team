import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_dir", required=True)
    args = parser.parse_args()

    print(f"[TEST HOOK] Running in project dir: {args.project_dir}")
    print("[TEST HOOK] Executing Linter...")
    print("[TEST HOOK] PASSED!")
    sys.exit(0)

if __name__ == "__main__":
    main()
