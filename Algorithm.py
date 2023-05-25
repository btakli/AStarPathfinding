import math
import random
import time


class Node:
    '''Node class to be used with A*. Contains a state, parent, and cost.
    
    The node data contains the coordinate of the center of the circle, and side (L/R) of the circle we are on.
    i.e (x,y,L) or (x,y,R). The coordinate of L would in actuality be (x-radius,y) and R would be (x+radius,y).
    ''' 
    def __init__(self, center_coordinate: tuple, radius: float, side: str, parent: 'Node', heuristic: int = 0, isGoal: bool = False):
        '''Creates a new node with the given data. Determines the cost of the node based on the parent's cost and the distance between the parent and the current node.
        
        Arguments:
        - center_coordinate: tuple of the center coordinate of the circle
        - radius: the radius of the circle
        - parent: the parent node
        - heuristic: the heuristic of the node (how many circles away from the goal node we are)
        - side: the side of the circle we are on
        - isGoal: whether the node is the goal node. Last node in the path (L/R) will be the goal node.
        '''
        self.center_coordinate = center_coordinate
        self.radius = radius
        self.side = side
        self.parent = parent
        self.children = []
        
        # if parent is not None and len(parent.children) == 0:
        #     parent.children.append(self)
        #     if self.side == 'L':
        #         parent.children.append(Node((self.center_coordinate[0],self.center_coordinate[1]),self.radius,'R',parent))
        #     else:
        #         parent.children.append(Node((self.center_coordinate[0],self.center_coordinate[1]),self.radius,'L',parent))
        
        self.cost = self.__get_cost()
        self.heuristic = heuristic
        self.isGoal = isGoal
        self.f = self.heuristic + self.cost # Initially set to 0, will be calculated later
        
    def __get_cost(self):
        '''Returns the cost of the node'''
        if self.parent is None:
            return 0
        else:
            return self.parent.cost + self.__distance(self.parent)
        
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
        return f"(x:{self.center_coordinate[0]:.4f}, y:{self.center_coordinate[1]}, radius:{self.radius:.4f}, side:{self.side}, isGoal:{self.isGoal}, f:{self.f:.4f})"
    
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
    def __init__(self, root: Node, circles: list[tuple[float, float, float]]):
        '''Creates a new A* object with the given list of nodes
        
        Arguments:
        - root: the root node
        - circles: the list of circles (x,y,radius) to be used to generate the children of each node)'''
        self.root = root
        self.circles = circles
        self.open = []
        self.closed = []
        self.total_cost = 0
        self.runtime = 0 # Runtime in seconds
    
    def search(self):
        '''Performs the A* search algorithm'''
        self.open.append(self.root)
        
        # Start timer
        start_time = time.perf_counter_ns()
        
        while len(self.open) > 0:
            
            self.open.sort(key=lambda node: node.f) # Sort the open list by f value, so that the lowest f value is at the front of the list
            current = self.open.pop(0)
            self.closed.append((current.center_coordinate[0],current.center_coordinate[1],current.radius,current.side))
            
            if current.isGoal:
                self.total_cost = current.cost
                
                end_time = time.perf_counter_ns()
                self.runtime = (end_time - start_time) * 10**-9
                
                return current.getPathFromRoot()
            
            generateChildren(current, self.circles)
            
            
            for child in current.children:
                # Check if the child is in the closed list (i.e the tuple (x,y,radius,side) is in the closed list))
                if (child.center_coordinate[0],child.center_coordinate[1],child.radius,child.side) not in self.closed:
                    if child not in self.open:
                        self.open.append(child)
                    else:
                        if child.cost < current.cost:
                            child.parent = current
        
        end_time = time.perf_counter_ns()
        self.runtime = (end_time - start_time) * 10**-9
        
        print("No path found! Returning None. This should NEVER happen...")
        return None

def getRootNodes(points: list[tuple[float, float, float]]) -> list[Node]:
    '''Returns the two root nodes based on the list of points'''
    nodes = []
    nodes.append(Node((points[0][0],points[0][1]),points[0][2],'L',None, heuristic=len(points)-1)) # Left side of first circle
    nodes.append(Node((points[0][0],points[0][1]),points[0][2],'R',None, heuristic=len(points)-1)) # Right side of first circle
    
    return nodes

def generateChildren(node: Node, circles: list[tuple[float, float, float]]) -> None:
    '''Generates the children for the given node, based on the list of circles. Children are only generated for circles with a higher y value than the current node, and only your direct child.'''

    for i in range(len(circles)):
        if circles[i][1] > node.center_coordinate[1]:
            
            if (i == len(circles) - 1): # Last circle is goal node
                node.children.append(Node((circles[i][0],circles[i][1]),circles[i][2],'L',node, heuristic=node.heuristic-1, isGoal=True))
                node.children.append(Node((circles[i][0],circles[i][1]),circles[i][2],'R',node, heuristic=node.heuristic-1, isGoal=True))
                break
            else:
                node.children.append(Node((circles[i][0],circles[i][1]),circles[i][2],'L',node, heuristic=node.heuristic-1, isGoal=False))
                node.children.append(Node((circles[i][0],circles[i][1]),circles[i][2],'R',node, heuristic=node.heuristic-1, isGoal=False))
                break
    
    


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