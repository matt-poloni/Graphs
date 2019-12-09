from collections import deque
def earliest_ancestor(ancestors, starting_node):
    # Create a family tree of child keys w/ list of parent values
    fam_tree = {}
    for (parent, child) in ancestors:
        # If the child's already there, add the parent
        if child in fam_tree:
            fam_tree[child].append(parent)
        # Otherwise, create the child with the parent
        else:
            fam_tree[child] = [parent]
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
        if child in fam_tree:
            # Extend the stack with their parents and the generations increased by 1
            stack.extend([(parent, child_gens + 1) for parent in fam_tree[child]])
    # Return -1 if 
    return -1 if generations == 0 else ancestor