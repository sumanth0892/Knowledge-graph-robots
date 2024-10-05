import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.is_temporal = False

    def add_node(self, node_id, **attributes):
        self.graph.add_node(node_id, **attributes)

    def add_edge(self, from_node, to_node, **attributes):
        self.graph.add_edge(from_node, to_node, **attributes)

    def update_node(self, node_id, **attributes):
        for attr, value in attributes.items():
            self.graph.nodes[node_id][attr] = value

    def get_node_attributes(self, node_id):
        return self.graph.nodes[node_id]

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(12, 10))
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=10, font_weight='bold')
        
        # Add node labels with attributes
        node_labels = {node: f"{node}\n{str(attr)}" for node, attr in self.graph.nodes(data=True)}
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=8)
        
        # Add edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'relation')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        
        plt.title("Knowledge Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

class TemporalKnowledgeGraph(KnowledgeGraph):
    def __init__(self):
        super().__init__()
        self.is_temporal = True
        self.current_time = datetime.now()

    def add_node(self, node_id, timestamp=None, **attributes):
        if timestamp is None:
            timestamp = self.current_time
        super().add_node((node_id, timestamp), **attributes)

    def add_edge(self, from_node, to_node, timestamp=None, **attributes):
        if timestamp is None:
            timestamp = self.current_time
        super().add_edge((from_node, timestamp), (to_node, timestamp), **attributes)

    def update_node(self, node_id, timestamp=None, **attributes):
        if timestamp is None:
            timestamp = self.current_time
        super().add_node((node_id, timestamp), **attributes)

    def get_node_attributes(self, node_id, timestamp=None):
        if timestamp is None:
            # Get the most recent state of the node
            relevant_nodes = [n for n in self.graph.nodes if n[0] == node_id]
            if not relevant_nodes:
                return None
            latest_node = max(relevant_nodes, key=lambda x: x[1])
            return super().get_node_attributes(latest_node)
        return super().get_node_attributes((node_id, timestamp))

    def get_node_history(self, node_id):
        return {n[1]: self.graph.nodes[n] for n in self.graph.nodes if n[0] == node_id}

    def visualize(self, start_time=None, end_time=None):
        if start_time is None:
            start_time = min(n[1] for n in self.graph.nodes if isinstance(n, tuple))
        if end_time is None:
            end_time = max(n[1] for n in self.graph.nodes if isinstance(n, tuple))

        subgraph = nx.MultiDiGraph()
        for node, data in self.graph.nodes(data=True):
            if isinstance(node, tuple) and start_time <= node[1] <= end_time:
                subgraph.add_node(node[0], **data)

        for u, v, data in self.graph.edges(data=True):
            if isinstance(u, tuple) and isinstance(v, tuple) and start_time <= u[1] <= end_time and start_time <= v[1] <= end_time:
                subgraph.add_edge(u[0], v[0], **data)

        pos = nx.spring_layout(subgraph)
        plt.figure(figsize=(12, 10))
        nx.draw(subgraph, pos, with_labels=True, node_color='lightgreen', 
                node_size=2000, font_size=10, font_weight='bold')

        # Add node labels with the latest attributes
        node_labels = {}
        for node in subgraph.nodes():
            attrs = self.get_node_attributes(node)
            label = f"{node}\n"
            label += "\n".join(f"{k}: {v}" for k, v in attrs.items() if k != 'type')
            node_labels[node] = label
        nx.draw_networkx_labels(subgraph, pos, labels=node_labels, font_size=8)

        plt.title(f"Temporal Knowledge Graph\n{start_time} to {end_time}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

# Example usage
def create_warehouse_graph(temporal=False):
    if temporal:
        kg = TemporalKnowledgeGraph()
    else:
        kg = KnowledgeGraph()

    # Add nodes
    kg.add_node("Robot1", type="robot", position=(0, 0), battery=1.0)
    kg.add_node("Robot2", type="robot", position=(10, 10), battery=0.9)
    kg.add_node("Shelf1", type="shelf", inventory=50)
    kg.add_node("Shelf2", type="shelf", inventory=30)
    kg.add_node("ChargingStation", type="station")

    # Add edges
    kg.add_edge("Robot1", "Shelf1", relation="can_access")
    kg.add_edge("Robot1", "Shelf2", relation="can_access")
    kg.add_edge("Robot2", "Shelf1", relation="can_access")
    kg.add_edge("Robot1", "ChargingStation", relation="can_charge")
    kg.add_edge("Robot2", "ChargingStation", relation="can_charge")

    return kg

# Demonstrate static graph
static_graph = create_warehouse_graph()
static_graph.visualize()

# Demonstrate temporal graph
temporal_graph = create_warehouse_graph(temporal=True)

# Simulate some temporal changes
temporal_graph.current_time += timedelta(minutes=30)
temporal_graph.update_node("Robot1", position=(5, 5), battery=0.8)
temporal_graph.update_node("Shelf1", inventory=45)

temporal_graph.current_time += timedelta(minutes=30)
temporal_graph.update_node("Robot2", position=(15, 15), battery=0.7)
temporal_graph.update_node("Shelf2", inventory=25)

temporal_graph.visualize()

# Show history of a node
robot1_history = temporal_graph.get_node_history("Robot1")
for timestamp, attributes in robot1_history.items():
    print(f"Robot1 at {timestamp}: {attributes}")
