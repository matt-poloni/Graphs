from collections import deque

class Graph:
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
    def add_edge(self, v1, v2):
        if all(v in self.vertices for v in [v1, v2]):
            self.vertices[v1].add(v2)
        else:
            raise IndexError("At least one of the given vertices does not exist.")
    def get_neighbors(self, vertex_id):
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise IndexError("That vertex does not exist.")


def earliest_ancestor(ancestors, starting_node):
    # Create a family tree of child keys w/ list of parent values
    fam_tree = Graph()
    for (parent, child) in ancestors:
        fam_tree.add_vertex(child)
        fam_tree.add_vertex(parent)
        fam_tree.add_edge(child, parent)
    # Initialize tracking variables
    ancestor = starting_node
    generations = 0
    # Initialize stack
    stack = deque([(ancestor, generations)])
    while len(stack) > 0:
        # Grab next potential child from stack
        (child, child_gens) = stack.pop()
        # If they're a new earliest ancestor, set them as such
        if child_gens > generations:
            ancestor = child
            generations = child_gens
        # If they're equal generations back but have a smaller ID, set them as the new earliest ancestor
        elif child_gens == generations and child < ancestor:
            ancestor = child
        # If the child has known parents...
        if len(parents := fam_tree.get_neighbors(child)) > 0:
            # Extend the stack with their parents and the generations increased by 1
            stack.extend([(parent, child_gens + 1) for parent in parents])
    # Return -1 if starting_node had no parents
    return -1 if generations == 0 else ancestor