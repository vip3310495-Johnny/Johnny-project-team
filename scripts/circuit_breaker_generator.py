import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json

def get_circuit_breaker_template(language):
    templates = {
        "python": '''
# Python 蝪⊥???函???import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED" # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF_OPEN"
            else:
                return {"error": "Circuit Breaker OPEN - using local mock data", "mock": True}
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            self.state = "CLOSED"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            raise e
''',
        "javascript": '''
// JavaScript/TypeScript 蝪⊥???函???class CircuitBreaker {
    constructor(failureThreshold = 5, resetTimeout = 60000) {
        this.failureThreshold = failureThreshold;
        this.resetTimeout = resetTimeout;
        this.failures = 0;
        this.lastFailureTime = null;
        this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    }

    async call(apiFunction) {
        if (this.state === 'OPEN') {
            if (Date.now() - this.lastFailureTime > this.resetTimeout) {
                this.state = 'HALF_OPEN';
            } else {
                return { error: 'Circuit Breaker OPEN - using local mock data', mock: true };
            }
        }
        
        try {
            const result = await apiFunction();
            this.failures = 0;
            this.state = 'CLOSED';
            return result;
        } catch (error) {
            this.failures++;
            this.lastFailureTime = Date.now();
            if (this.failures >= this.failureThreshold) {
                this.state = 'OPEN';
            }
            throw error;
        }
    }
}
'''
    }
    return templates.get(language.lower(), "Language not supported yet.")

def main():
    parser = argparse.ArgumentParser(description="Generate a Circuit Breaker implementation template")
    parser.add_argument('--language', type=str, required=True, choices=['python', 'javascript'], help="Target programming language")
    
    args = parser.parse_args()
    template = get_circuit_breaker_template(args.language)
    
    print(json.dumps({
        "language": args.language,
        "template_code": template,
        "instruction": "Inject this code when implementing external API calls to prevent system cascading failures."
    }, indent=2))

if __name__ == "__main__":
    main()
