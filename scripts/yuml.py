import networkx as nx
import matplotlib.pyplot as plt


def parse_yuml(yuml_content):
    """Parse yUML content and return a list of edges."""
    lines = yuml_content.strip().split('\n')
    edges = []

    for line in lines:
        parts = line.split('-')
        if len(parts) == 3:
            edges.append((parts[0].strip('[]'), parts[2].strip('[]')))
        elif len(parts) == 2:
            edges.append((parts[0].strip('[]'), parts[1].strip('[]')))

    return edges


def visualize_yuml(yuml_content):
    """Visualize the yUML content."""
    edges = parse_yuml(yuml_content)
    G = nx.DiGraph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue')
    plt.show()


if __name__ == "__main__":
    with open('../yuml/yuml_persoon.yuml', 'r') as f:
        yuml_content = f.read()

    visualize_yuml(yuml_content)
