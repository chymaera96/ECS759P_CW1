import numpy as np



def bfs(start, end, tube_graph):
    '''
    Breadth First Search

    Parameters:
    ------------
    start: str
        starting station
    end: str
        ending station
    tube_graph: instance of class TubeStationGraph
        provides adjacency matrix and lookup dictionaries


    Returns:
    ------------
    path: list
        list of stations in the path
    time_taken: float
        total average time to traverse the path
    expanded_nodes: int
        number of nodes expanded 

    '''
    # Enqueue state = (node, path traversed, cost)
    queue = [(start, [start], 0)]
    visited = set()
    while queue:
        # Dequeue
        (node, path, cost) = queue.pop(0)
        if node not in visited:
            if node == end:    
            # Goal Test successful
                time_taken = cost           
                expanded_nodes = len(visited)
                return path, time_taken, expanded_nodes
            visited.add(node)

            # Expand node using the adjacency matrix
            for child,  child_cost in enumerate(tube_graph.adj_matrix[tube_graph.station_names.index(node)]):
                if child_cost != np.inf:        # child_cost = np.inf indicates no connection
                    queue.append((tube_graph.station_names[child], path + [tube_graph.station_names[child]], cost + child_cost))

    return [], -1, len(visited)          # Retun failure



def dfs(start, end, tube_graph):
    '''
    Depth First Search

    Parameters:
    ------------
    start: str
        starting station
    end: str
        ending station
    tube_graph: instance of class TubeStationGraph
        provides adjacency matrix and lookup dictionaries


    Returns:
    ------------
    path: list
        list of stations in the path
    time_taken: float
        total average time to traverse the path
    expanded_nodes: int
        number of nodes expanded 

    '''
    # Push state = (node, path traversed, cost)
    stack = [(start, [start], 0)]              
    visited = set()
    while stack:
        # Pop state
        (node, path, cost) = stack.pop()
        if node not in visited:       
            if node == end:    
            # Goal Test successful
                time_taken = cost           
                expanded_nodes = len(visited)
                return path, time_taken, expanded_nodes
            visited.add(node)

            # Expand node
            for child,  child_cost in enumerate(tube_graph.adj_matrix[tube_graph.station_names.index(node)]):
                if child_cost != np.inf:        # child_cost = np.inf indicates no connection
                    stack.append((tube_graph.station_names[child], path + [tube_graph.station_names[child]], cost + child_cost))

    return [], -1, len(visited)          # Retun failure



def ucs(start, end, tube_graph):
    '''
    Uniform Cost Search

    Parameters:
    ------------
    start: str
        starting station
    end: str
        ending station
    tube_graph: instance of class TubeStationGraph
        provides adjacency matrix and lookup dictionaries


    Returns:
    ------------
    path: list
        list of stations in the path
    time_taken: float
        total average time to traverse the path
    expanded_nodes: int
        number of nodes expanded 

    '''

    # Enqueue state = (node, path traversed, cost)
    queue = [(start, [start], 0)]          
    visited = set()
    while queue:
        # Dequeue state
        (node, path, cost) = queue.pop(0)
        if node not in visited:
            if node == end:    
            # Goal Test successful
                time_taken = cost           
                expanded_nodes = len(visited)
                return path, time_taken, expanded_nodes
            visited.add(node)

            # Expand node
            for child,  child_cost in enumerate(tube_graph.adj_matrix[tube_graph.station_names.index(node)]):
                if child_cost != np.inf:        # child_cost = np.inf indicates no connection
                    queue.append((tube_graph.station_names[child], path + [tube_graph.station_names[child]], cost + child_cost))
            queue.sort(key=lambda x: x[-1])          # Sort queue by cost

    return [], -1, len(visited)          # Retun failure



def ucs_improved(start, end, tube_graph, change_time=2):
    '''
    Uniform Cost Search with improved cost function

    Parameters:
    ------------
    start: str
        starting station
    end: str
        ending station
    tube_graph: instance of class TubeStationGraph
        provides adjacency matrix and lookup dictionaries
    change_time: int
        time taken to change lines

    Returns:
    ------------
    path: list
        list of stations in the path

    time: float
        time taken to run the algorithm

    visited: int
        number of nodes visited

    '''
    # The state requires a modification to include th last line used
    queue = [(start, [start], 0, None)]        # state = (node, path traversed, cost, last line used)
    visited = set()
    while queue:
        # Get node from queue
        (node, path, cost, last_line_type) = queue.pop(0)
        if node not in visited:
            if node == end:    
            # Goal Test successful
                time_taken = cost           
                expanded_nodes = len(visited)
                return path, time_taken, expanded_nodes
            visited.add(node)
        
            # Expand node
            for child, child_cost, line in tube_graph.station_dict[node]:
                line_change_cost = 0 if last_line_type is None or last_line_type == line else change_time
                queue.append((child, path + [child], cost + child_cost + line_change_cost, line))
            queue.sort(key=lambda x: x[-2])          # Sort queue by cost

        
    return [], -1, len(visited)          # Retun failure


def best_first_search(start, end, tube_graph, heuristic_fn, zone_distance_matrix, zone_names, change_time=2):
    '''
    Best First Search

    Parameters:
    ------------
    start: str
        starting station
    end: str
        ending station
    tube_graph: instance of class TubeStationGraph
        provides adjacency matrix and lookup dictionaries
    zone_distance_matrix: list
        matrix of distances between zones
    zone_names: list
        list of zone names
    
    Returns:
    ------------
    path: list
        list of stations in the path
    time_taken: float
        total average time to traverse the path
    expanded_nodes: int
        number of nodes expanded
    '''

    # Enqueue state = (node, path traversed, cost, last line used, heuristic)
    queue = [(start, [start], 0, None, 0)]
    visited = set()
    while queue:
        (node, path, cost, last_line_type, heuristic) = queue.pop(0)
        if node not in visited:
            if node == end:    
            # Goal Test successful
                time_taken = cost           
                expanded_nodes = len(visited)
                return path, time_taken, expanded_nodes
            visited.add(node)

            # Expand node
            for child, child_cost, line in tube_graph.station_dict[node]:
                line_change_cost = 0 if last_line_type is None or last_line_type == line else change_time
                heuristic = heuristic_fn(child, end, tube_graph, zone_distance_matrix, zone_names)
                queue.append((child, path + [child], cost + child_cost + line_change_cost, line, heuristic))
            queue.sort(key=lambda x: x[-1])          # Sort queue by heuristic

    return [], len(visited)          # Retun failure