def count_dependencies(edges):
    # Create a dictionary to store dependencies for each node
    dependencies = {}
    
    # Iterate through the edges
    for edge in edges:
        # Add first letter of the edge if not exists
        if edge[0] not in dependencies:
            dependencies[edge[0]] = 0
        
        # Increment dependencies for the first letter
        dependencies[edge[0]] += 1
    
    # Convert to the desired output format
    result = [[letter, count] for letter, count in dependencies.items()]
    
    return result

# Example usage
edges = [['A', 'B'], ['A', 'C'], ['B', 'C'], ['B', 'D'], ['B', 'E'], 
         ['C', 'E'], ['D', 'E'], ['D', 'F'], ['E', 'F'], ['E', 'G'], 
         ['F', 'G'], ['F', 'H'], ['G', 'H']]

# Count dependencies
dependencies_list = count_dependencies(edges)

print(dependencies_list)