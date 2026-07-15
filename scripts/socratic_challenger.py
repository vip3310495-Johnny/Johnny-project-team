import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Socratic Questioning Generator for Architecture Proposals")
    parser.add_argument('--proposal', type=str, required=True, help="The architecture or design proposal")
    
    args = parser.parse_args()
    
    proposal = args.proposal.lower()
    questions = []
    
    if "always" in proposal or "never" in proposal or "all" in proposal:
        questions.append("You used an absolute term. What is the edge case where this assumption completely fails?")
    
    if "faster" in proposal or "better" in proposal or "easier" in proposal:
        questions.append("You claim this is 'better/faster'. What is the exact quantitative metric we are using to prove this, and what is the baseline?")
        
    if "microservices" in proposal or "kubernetes" in proposal or "kafka" in proposal:
        questions.append("This introduces significant infrastructure complexity. Could we achieve 80% of the value with a simple monolith and a Postgres database?")
        
    if not questions:
        questions.append("If this solution is implemented perfectly, what is the most likely reason it will fail in production 6 months from now?")
        questions.append("What is the underlying assumption we are making about the user's behavior here, and how can we test it before writing code?")

    print(json.dumps({
        "status": "Challenged",
        "socratic_questions": questions,
        "instruction": "Do not proceed until the Dev/DQA agent provides a logical defense to these questions."
    }, indent=2))

if __name__ == "__main__":
    main()
