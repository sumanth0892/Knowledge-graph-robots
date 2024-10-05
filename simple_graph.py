from py2neo import Graph, Node, Relationship

   graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

   def add_temporal_node(entity_id, attributes, timestamp):
       node = Node("TemporalEntity", entity_id=entity_id, timestamp=timestamp, **attributes)
       graph.create(node)
       return node

   def add_temporal_edge(from_node, to_node, rel_type, timestamp):
       rel = Relationship(from_node, rel_type, to_node, timestamp=timestamp)
       graph.create(rel)

   # Usage
   robot_t1 = add_temporal_node("Robot1", {"position": (10, 20), "battery": 0.9}, timestamp=1623456789)
   robot_t2 = add_temporal_node("Robot1", {"position": (15, 25), "battery": 0.85}, timestamp=1623456799)
   add_temporal_edge(robot_t1, robot_t2, "MOVED_TO", timestamp=1623456799)
