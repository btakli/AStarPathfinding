import math
import random

class Node:
    '''Node class to be used with A*. Contains a state, parent, and cost.
    
    The node data contains the coordinate of the center of the circle, and side (L/R) of the circle we are on.
    i.e (x,y,L) or (x,y,R). The coordinate of L would in actuality be (x-radius,y) and R would be (x+radius,y).
    ''' 
    def __init__(self, center_coordinate: tuple, radius: float, side: chr, parent: 'Node', isGoal: bool = False):
        '''Creates a new node with the given data. Determines the cost of the node based on the parent's cost and the distance between the parent and the current node.
        
        Arguments:
        - center_coordinate: tuple of the center coordinate of the circle
        - radius: the radius of the circle
        - parent: the parent node
        - side: the side of the circle we are on
        - isGoal: whether the node is the goal node. Last node in the path (L/R) will be the goal node.
        '''
        self.center_coordinate = center_coordinate
        self.radius = radius
        self.side = side
        self.parent = parent
        self.children = []
        
        if parent is not None:
            parent.children.append(self)
        
        self.cost = self.__get_cost()
        self.heuristic = 0
        self.isGoal = isGoal
        self.f = 0 # Initially set to 0, will be calculated later
        
    def __get_cost(self):
        '''Returns the cost of the node'''
        if self.parent is None:
            return 0
        else:
            return self.parent.cost + self.__distance(self.parent)
        
    def calculate_heuristic(self):
        '''Calculates and sets the heuristic of the node: I.E how many circles away from the goal node we are (L/R is one point).'''
        goal = self # Doesn't matter if L or R, since they are both the same distance from the goal
        heuristic = 0
        while not goal.isGoal:
            self.heuristic += 1
            goal = goal.children[0]
        
    def __distance(self, other: 'Node'):
        '''Returns the distance between the current node and the other node'''
        other_x = other.center_coordinate[0] - other.radius if other.side == 'L' else other.center_coordinate[0] + other.radius
        other_y = other.center_coordinate[1]
        
        self_x = self.center_coordinate[0] - self.radius if self.side == 'L' else self.center_coordinate[0] + self.radius
        self_y = self.center_coordinate[1]
        
        return math.sqrt((other_x - self_x)**2 + (other_y - self_y)**2)
        

    def __eq__(self, other: 'Node'):
        '''Returns whether the two nodes are equal'''
        return self.f == other.f
    
    def __lt__(self, other: 'Node'):
        '''Returns whether the current node is less than the other node'''
        return self.f < other.f
    
    def __gt__(self, other: 'Node'):
        '''Returns whether the current node is greater than the other node'''
        return self.f > other.f
    
    def __str__(self):
        '''Returns a string representation of the node'''
        return f"(x:{self.center_coordinate[0]}, y:{self.center_coordinate[1]}, radius:{self.radius}, side:{self.side}, isGoal:{self.isGoal})"
    
    def getPathFromRoot(self) -> list['Node']:
        '''Returns the path from the root node to the current node'''
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]
               
class AStar:
    '''A* algorithm to find the shortest path from the start node to a goal node'''
    def __init__(self, nodes: list[Node]):
        '''Creates a new A* object with the given list of nodes'''
        self.nodes = nodes
        self.open = []
        self.closed = []
        self.visited = []
    
    def search(self):
        '''Performs the A* search algorithm'''
        self.open.append(self.nodes[0])
        #self.open.append(self.nodes[1])
        while len(self.open) > 0:
            current = self.open.pop(0)
            self.closed.append(current)
            
            if current.isGoal:
                return current.getPathFromRoot()
            
            for child in current.children:
                if child not in self.closed:
                    if child not in self.open:
                        self.open.append(child)
                    else:
                        if child.cost < current.cost:
                            child.parent = current
                            self.open.sort(key=lambda x: x.f) # Sort the open list by f value, so that the lowest f value is at the front of the list
                            
            print("Open list: ")
            for node in self.open:
                print(node)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            
                            
        return None
    
def createNodesListFromPoints(points: list[tuple[float, float, float]]):
    '''Creates a list of nodes from the given list of points tuples (x,y,radius). Properly assigns parents and sides, as well as if the node is a goal.'''
    nodes = []
    
    for i in range(len(points)):
        if i == 0:
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'L',None))
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'R',None))
        elif i == len(points)-1: # Last node is goal node
            # Need to set the parents: Could've come from the left or right of the previous node
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'L',nodes[-2],True)) 
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'R',nodes[-2],True))
        else:
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'L',nodes[-2]))
            nodes.append(Node((points[i][0],points[i][1]),points[i][2],'R',nodes[-2]))
            
            
        
            
            
        
    
    for node in nodes:
        node.calculate_heuristic() # Calculate the heuristic for each node after all nodes have been created (we need to know the goal node and have all children created)
        node.f = node.cost + node.heuristic # Calculate the f value for each node
        
    return nodes

def generateCircles(n = 10, coord_range = 250, radius_range = 15) -> list[tuple[float, float, float]]:
    '''Generate a list of n circles on screen, with random coordinates and radius
    
    Arguments:
    - n: number of circles to generate
    - coord_range: range of coordinates to generate from [0-coord_range, 0-coord_range]
    - radius_range: range of radius to generate from'''
    circles = []
    for i in range(n):
        # The y values should allow for clustering in threes
        radius = random.uniform(10,radius_range)
        x = random.uniform(radius_range,coord_range)
        y = 3*i*radius_range + radius_range
        circles.append((x,y,radius))
        
    return circles


        
        
    
    
        
    
    