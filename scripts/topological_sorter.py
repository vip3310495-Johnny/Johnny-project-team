import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
import argparse
import json
from collections import defaultdict, deque

def topological_sort(vertices, edges):
    in_degree = {u: 0 for u in vertices}
    graph = defaultdict(list)
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
        
    queue = deque([u for u in vertices if in_degree[u] == 0])
    order = []
    
    while queue:
        u = queue.popleft()
        order.append(u)
        
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    if len(order) != len(vertices):
        return None # Cycle detected
    return order

def main():
    parser = argparse.ArgumentParser(description="Topological Sort for Dependencies")
    parser.add_argument('--nodes', type=str, required=True, help='JSON array of nodes: ["A", "B", "C"]')
    parser.add_argument('--edges', type=str, required=True, help='JSON array of directed edges (from, to): [["A", "B"], ["A", "C"]]')
    
    args = parser.parse_args()
    
    nodes = json.loads(args.nodes)
    edges = json.loads(args.edges)
    
    result = topological_sort(nodes, edges)
    
    if result is None:
        print(json.dumps({"error": "Cycle detected in dependencies. Cannot resolve order."}))
    else:
        print(json.dumps({"execution_order": result}, indent=2))

if __name__ == "__main__":
    main()
