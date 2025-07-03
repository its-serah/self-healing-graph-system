import csv
import networkx as nx
import json
import sys
import os
sys.path.append("src")
from detector import load_triples, detect_infections
from healer import heal

# Create a network visualization
def create_graph_visualization(triples, output_file, title, infection_info=None):
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Define node and edge attributes
    node_types = {}
    edge_attrs = {}
    
    # First pass: collect node types
    for triple in triples:
        s, p, o = triple["s"], triple["p"], triple["o"]
        conf = float(triple.get("confidence", 1.0))
        
        # Determine node types
        if s.startswith("Person"):
            node_types[s] = "person"
        elif s.startswith("Company"):
            node_types[s] = "company"
        
        if o.startswith("Person"):
            node_types[o] = "person"
        elif o.startswith("Company"):
            node_types[o] = "company"
        elif o.startswith("City") or o.startswith("Country"):
            node_types[o] = "location"
        elif p == "birthDate":
            node_types[o] = "date"
        else:
            node_types[o] = "other"
    
    # Second pass: build edges with attributes
    for triple in triples:
        s, p, o = triple["s"], triple["p"], triple["o"]
        conf = float(triple.get("confidence", 1.0))
        
        G.add_node(s, type=node_types.get(s, "other"))
        G.add_node(o, type=node_types.get(o, "other"))
        
        # Check if this is an infected triple
        infection_type = None
        if infection_info:
            for inf_triple, rule in infection_info:
                if inf_triple == triple:
                    infection_type = rule
                    break
        
        G.add_edge(s, o, predicate=p, confidence=conf, infection=infection_type)
    
    # Convert to JSON for visualization
    nodes = []
    for node, attrs in G.nodes(data=True):
        node_type = attrs.get('type', 'other')
        color = get_node_color(node_type)
        nodes.append({
            "id": node,
            "label": node,
            "color": color,
            "title": f"Type: {node_type}"
        })
    
    edges = []
    for s, o, attrs in G.edges(data=True):
        predicate = attrs.get('predicate', '')
        confidence = attrs.get('confidence', 1.0)
        infection = attrs.get('infection')
        
        # Set edge color based on infection
        color = "#000000"  # Default black
        if infection:
            color = get_rule_color(infection)
        
        # Set edge width based on confidence
        width = max(1, confidence * 5)
        
        edges.append({
            "from": s,
            "to": o,
            "label": predicate,
            "color": color,
            "width": width,
            "title": f"{predicate} (confidence: {confidence})"
        })
    
    # Create HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css">
        <style type="text/css">
            #mynetwork {{
                height: 750px;
                width: 100%;
                border: 1px solid lightgray;
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div id="mynetwork"></div>
        <script type="text/javascript">
            // Create nodes and edges
            var nodes = new vis.DataSet({json.dumps(nodes)});
            var edges = new vis.DataSet({json.dumps(edges)});
            
            // Create network
            var container = document.getElementById('mynetwork');
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            var options = {{
                physics: {{
                    forceAtlas2Based: {{
                        gravitationalConstant: -50,
                        centralGravity: 0.01,
                        springLength: 100,
                        springConstant: 0.08
                    }},
                    maxVelocity: 50,
                    solver: "forceAtlas2Based",
                    timestep: 0.35,
                    stabilization: {{iterations: 150}}
                }},
                edges: {{
                    smooth: {{type: "continuous"}},
                    font: {{
                        size: 12,
                        face: "arial",
                        align: "middle"
                    }},
                    arrows: {{
                        to: {{enabled: true, scaleFactor: 0.5}}
                    }}
                }},
                nodes: {{
                    shape: "dot",
                    size: 16,
                    font: {{
                        size: 14,
                        face: "arial"
                    }},
                    margin: 10
                }},
                interaction: {{
                    hover: true,
                    navigationButtons: true,
                    keyboard: true
                }}
            }};
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)

# Get color for node type
def get_node_color(node_type):
    colors = {
        "person": "#3498db",    # Blue
        "company": "#e74c3c",   # Red
        "location": "#2ecc71",  # Green
        "date": "#f39c12",      # Orange
        "other": "#95a5a6"      # Gray
    }
    return colors.get(node_type, colors["other"])

# Get color for infection rule
def get_rule_color(rule):
    colors = {
        "R1": "#e74c3c",  # Red for low confidence
        "R2": "#9b59b6",  # Purple for duplicate functional predicates
        "R3": "#f39c12"   # Orange for schema violations
    }
    return colors.get(rule, "#000000")

def main():
    # Load original triples
    original_triples = load_triples("data/mini_static.csv")
    
    # Detect infections
    infections = detect_infections(original_triples)
    
    # Process healing
    cleaned_triples = []
    
    for triple in original_triples:
        # Check if this triple is infected
        is_infected = False
        rule_tag = None
        
        for inf_triple, rule in infections:
            if inf_triple == triple:
                is_infected = True
                rule_tag = rule
                break
        
        if is_infected:
            # Try to heal the triple
            healed_triple = heal(triple, rule_tag)
            if healed_triple:  # Successfully healed or quarantined
                cleaned_triples.append(healed_triple)
        else:  # Not infected, keep as is
            cleaned_triples.append(triple)
    
    # Create visualizations
    create_graph_visualization(original_triples, 'original_graph.html', 
                              "Original Knowledge Graph (with infections highlighted)", 
                              infections)
    create_graph_visualization(cleaned_triples, 'cleaned_graph.html', 
                              "Cleaned Knowledge Graph (after healing)")
    
    # Save summary information
    summary = {
        "original_count": len(original_triples),
        "cleaned_count": len(cleaned_triples),
        "infections": len(infections),
        "infection_types": {
            "R1": sum(1 for _, rule in infections if rule == "R1"),
            "R2": sum(1 for _, rule in infections if rule == "R2"),
            "R3": sum(1 for _, rule in infections if rule == "R3")
        }
    }
    
    with open('results/visualization_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nVisualizations created:")
    print("- original_graph.html (Original graph with infections highlighted)")
    print("- cleaned_graph.html (Cleaned graph after healing process)")
    print("\nOpen view_graphs.html in your web browser to see both visualizations side by side.")

if __name__ == "__main__":
    main()
