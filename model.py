from pydantic import BaseModel, Field
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Set, Optional

# --------------------------------------KNOWLEDGE GRAPH--------------------------------------

class Knowledge_Graph:
    def __init__(self, table_names: Optional[List[str]] = None, fk_relationships: Optional[List[Tuple[str, str, str]]] = None):
        """
        Initializing a Directed graph for the knowledge graph.
        Optionally, populates it with nodes (tables) and edges (FK relationships).

        Args:
            table_names (List[str], optional): A list of table names to add as nodes.
            fk_relationships (List[Tuple[str, str, str]], optional): A list of tuples
                (source_table, target_table, fk_column_name) representing foreign key
                relationships. The edge direction is from FK table (source) to PK table (target).
        """
        self.graph = nx.DiGraph()
        self.graph.graph['name'] = 'Database Schema Knowledge Graph'

        if table_names:
            self.add_nodes_from(table_names)
        if fk_relationships:
            self._add_fk_edges(fk_relationships) # Internal method to add FKs

    def add_node(self, node: str, **attributes):
        """
        Add a node to the graph with optional attributes.

        Args:
            node (str): The name of the table to add as a node.
            **attributes: Optional attributes for the node (e.g., 'type': 'fact_table').
        """
        if not isinstance(node, str) or not node:
            print(f"Warning: Node name must be a non-empty string. Skipping node: {node}")
            return
        self.graph.add_node(node, **attributes)

    def add_nodes_from(self, nodes: List[str]):
        """
        Add multiple nodes to the graph.

        Args:
            nodes (List[str]): A list of table names to add as nodes.
        """
        for node in nodes:
            self.add_node(node)

    def add_edge(self, source: str, target: str, predicate: str, **attributes):
        """
        Add a directed edge between a source node and a target node,
        with a predicate and optional attributes.

        Args:
            source (str): The source node (e.g., table with FK).
            target (str): The target node (e.g., table with PK).
            predicate (str): The relationship type (e.g., 'references_customer_id').
            **attributes: Optional attributes for the edge (e.g., 'on_column': 'customer_id').
        """
        if not self.graph.has_node(source):
            print(f"Warning: Source node '{source}' not in graph. Adding it.")
            self.add_node(source)
        if not self.graph.has_node(target):
            print(f"Warning: Target node '{target}' not in graph. Adding it.")
            self.add_node(target)

        self.graph.add_edge(source, target, predicate=predicate, **attributes)

    def _add_fk_edges(self, fk_relationships: List[Tuple[str, str, str]]):
        """
        Internal method to add foreign key relationships as directed edges.
        Direction: FK table (source) -> PK table (target).

        Args:
            fk_relationships (List[Tuple[str, str, str]]): List of tuples
                (source_table, target_table, fk_column_name).
        """
        for source_table, target_table, fk_column_name in fk_relationships:
            # Ensure nodes exist before adding edges
            self.add_node(source_table)
            self.add_node(target_table)
            self.add_edge(source_table, target_table, f"references_{fk_column_name}", on_column=fk_column_name)

    def add_from_triplets(self, triplets: List[Tuple[str, str, str]]):
        """
        Add multiple edges from a list of (source, predicate, target) triplets.
        Note: This is more generic than _add_fk_edges and assumes the predicate
        is the third element in the triplet, and direction is source -> target.

        Args:
            triplets (List[Tuple[str, str, str]]): List of (source, predicate, target) tuples.
        """
        for source, predicate, target in triplets:
            self.add_edge(source, target, predicate=predicate) # Assumes predicate is the attribute

    def find_connected_tables(self, start_nodes: List[str], max_depth: Optional[int] = None) -> Set[str]:
        """
        Finds all nodes reachable from a set of start_nodes within a given depth,
        considering both forward (FK -> PK) and reverse (PK -> FK) directions
        to simulate undirected connectivity for filtering purposes.

        Args:
            start_nodes (List[str]): A list of starting table names.
            max_depth (Optional[int]): The maximum traversal depth. If None, traverse all.

        Returns:
            Set[str]: A set of unique connected table names.
        """
        connected_nodes = set()
        
        for start_node in start_nodes:
            if start_node not in self.graph:
                print(f"Warning: Start node '{start_node}' not found in the graph. Skipping.")
                continue
            
            # BFS in forward direction (FK to PK)
            for node in nx.bfs_tree(self.graph, start_node, depth_limit=max_depth):
                connected_nodes.add(node)
            
            # BFS in reverse direction (PK to FK) to get tables that *reference* the start_node
            for node in nx.bfs_tree(self.graph.reverse(), start_node, depth_limit=max_depth):
                connected_nodes.add(node)
                
        return connected_nodes

    
    def get_subgraph(self, nodes_list: List[str]) -> nx.DiGraph:
        """
        Returns a subgraph containing only the specified nodes and their existing edges.

        Args:
            nodes_list (List[str]): A list of table names to include in the subgraph.

        Returns:
            nx.DiGraph: The generated subgraph.
        """
        return self.graph.subgraph(nodes_list)

    def draw_graph(self, layout: Optional[str] = 'kamada_kawai', node_size: int = 1000, font_size: int = 8, with_labels: bool = True, title: Optional[str] = None):
        """
        Draws the knowledge graph for visualization.

        Args:
            layout (Optional[str]): Layout algorithm ('spring', 'circular', 'shell', 'kamada_kawai').
            node_size (int): Size of the graph nodes.
            font_size (int): Font size for labels.
            with_labels (bool): Whether to draw node labels.
            title (Optional[str]): Title for the plot.
        """
        plt.figure(figsize=(12, 8))

        if layout == 'spring':
            pos = nx.spring_layout(self.graph, k=0.8, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(self.graph)
        elif layout == 'shell':
            pos = nx.shell_layout(self.graph)
        else:
            pos = nx.kamada_kawai_layout(self.graph)

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color='skyblue', node_size=node_size, alpha=0.9)

        # Draw edges and labels (predicates)
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        # Draw edge labels (predicates)
        edge_labels = nx.get_edge_attributes(self.graph, 'predicate')
        if edge_labels:
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red', font_size=font_size-2)

        # Draw node labels
        if with_labels:
            nx.draw_networkx_labels(self.graph, pos, font_size=font_size, font_weight='bold')

        if title:
            plt.title(title)
        plt.axis('off')
        plt.savefig('knowledge_graph.png', format='png', dpi=300, bbox_inches='tight')
        plt.show()

    def save_graph(self, file_path: str):
        """
        Saves the graph to a file (e.g., .gml, .graphml, .gpickle).

        Args:
            file_path (str): The path to save the graph file.
        """
        try:
            if file_path.endswith('.gml'):
                nx.write_gml(self.graph, file_path)
            elif file_path.endswith('.graphml'):
                nx.write_graphml(self.graph, file_path)
            elif file_path.endswith('.gpickle'):
                nx.write_gpickle(self.graph, file_path)
            else:
                print("Unsupported file format. Please use .gml, .graphml, or .gpickle.")
                return
            print(f"Graph saved to {file_path}")
        except Exception as e:
            print(f"Error saving graph: {e}")
    
    def validate_path(self, nodes_list: List[str]) :
        """
        Validates that the given list of tables can be joined together using the knowledge graph.

        Returns a list of join tuples (source_table, join_column, target_table) for the minimum
        required join path. This will include only mediator tables that are essential for joins.

        Args:
            nodes_list (List[str]): List of seed  tables.

        Returns:
            List[Tuple[str, str, str]]: List of join relationships required to connect all tables.
            ** If a new table is added, then it will automatically be added in the path list.
        """
        if len(nodes_list) < 2:
            return []

        required_joins = set()
        paths = []
        subgraph = self.get_subgraph(nodes_list)

        for i in range(len(nodes_list)):
            for j in range(i + 1, len(nodes_list)):
                source = nodes_list[i]
                target = nodes_list[j]
                try:
                    path = nx.shortest_path(subgraph.to_undirected(), source, target)
                    paths.append(path)
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    try:
                        path = nx.shortest_path(self.graph.to_undirected() , source, target)
                        paths.append(path)
                    except(nx.NetworkXNoPath, nx.NodeNotFound):
                        print(f"No path found between {source} and {target} in either subgraph or whole graph")

                # Convert path like [a, b, c] to [(a,b), (b,c)]
                for u, v in zip(path, path[1:]):
                    if self.graph.has_edge(u, v):
                        data = self.graph.get_edge_data(u, v)
                        join_col = data.get("on_column", data.get("predicate", ""))
                        required_joins.add((u, join_col, v))
                    elif self.graph.has_edge(v, u):
                        data = self.graph.get_edge_data(v, u)
                        join_col = data.get("on_column", data.get("predicate", ""))
                        required_joins.add((v, join_col, u))
                    else:
                        continue  # Not a valid edge

        return paths , list(required_joins)

    @classmethod
    def load_graph(cls, file_path: str):
        """
        Loads a graph from a file and returns a new Knowledge_Graph instance.

        Args:
            file_path (str): The path to the graph file.

        Returns:
            Knowledge_Graph: A new Knowledge_Graph instance loaded from the file, or None on error.
        """
        kg = cls() # Create an empty instance
        try:
            if file_path.endswith('.gml'):
                kg.graph = nx.read_gml(file_path)
            elif file_path.endswith('.graphml'):
                kg.graph = nx.read_graphml(file_path)
            elif file_path.endswith('.gpickle'):
                kg.graph = nx.read_gpickle(file_path)
            else:
                raise ValueError("Unsupported file format. Please use .gml, .graphml, or .gpickle.")
            print(f"Graph loaded from {file_path}")
            return kg
        except Exception as e:
            print(f"Error loading graph: {e}")
            return None 
                         
# ----------------------------------------PYDANTIC MODELS-------------------------------------------
class table_result(BaseModel):
    table_names: List[str] = Field(..., description="Return the names of the required tables in form of a list")
    
class RelevantColumns(BaseModel):
    table_name: str = Field(description = "The name of the table the column belongs to ")
    column_name: str = Field(description = "The name of the column")
    reason:str = Field(description = "briefly describe why the current column is relevant")
    data_type: str = Field(description= "The data type of the extracted column")
    
class RelevantColumnsOutput(BaseModel):
    relevant_columns : List[RelevantColumns] = Field(..., description= "A list of relevant columns identified from the context")
    
    
    
