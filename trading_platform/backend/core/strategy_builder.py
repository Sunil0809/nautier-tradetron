from typing import Any, Dict, List


def compile_graph_to_logic(graph: Dict[str, Any]) -> Dict[str, Any]:
    """Convert node graph payload into execution-ready representation."""
    nodes: List[Dict[str, Any]] = graph.get('nodes', [])
    edges = graph.get('edges', [])
    compiled = {'indicators': [], 'conditions': [], 'risk': [], 'actions': [], 'edges': edges}
    for node in nodes:
        kind = node.get('type')
        if kind == 'indicator':
            compiled['indicators'].append(node)
        elif kind in {'condition', 'logic'}:
            compiled['conditions'].append(node)
        elif kind == 'risk':
            compiled['risk'].append(node)
        elif kind in {'entry', 'exit', 'execution'}:
            compiled['actions'].append(node)
    return compiled
