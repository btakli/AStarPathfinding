import pygame
import Algorithm

def drawCircles(screen, circles: list[tuple[float, float, float]], path: list[Algorithm.Node] = []):
    '''Draws the circles on screen, given the list of circles.
    
    Optional: Also draws the lines between the circles based on the search algorithm.'''
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    
        # Make the background white
        screen.fill((255,255,255))
    
        for circle in circles:
            pygame.draw.circle(screen, (255,0,0), (circle[0],circle[1]), circle[2], 1)
            
        for node in path:
            if node.parent is None:
                continue
            
            start_x = node.parent.center_coordinate[0] - node.parent.radius if node.parent.side == 'L' else node.parent.center_coordinate[0] + node.parent.radius
            start_y = node.parent.center_coordinate[1]
            
            end_x = node.center_coordinate[0] - node.radius if node.side == 'L' else node.center_coordinate[0] + node.radius
            end_y = node.center_coordinate[1]
            
            pygame.draw.line(screen, (0,255,0), (start_x, start_y), (end_x, end_y), 1)

        # Update the display
        pygame.display.update()
    
    
def main():
    circles = Algorithm.generateCircles()
    
    screen = pygame.display.set_mode((500,500))
    
    drawCircles(screen, circles)
    
    leftRoot, rightRoot = Algorithm.getRootNodes(circles)
    
    # print("Children of first node: ")
    # for child in nodes[0].children:
    #     print(child)
        
    # aStar = Algorithm.AStar(nodes)
    
    aStarLeft = Algorithm.AStar(leftRoot, circles)
    aStarRight = Algorithm.AStar(rightRoot, circles)
    
    leftPath = aStarLeft.search()
    
    if leftPath is None:
        print("No left path found")
        
    rightPath = aStarRight.search()
    
    if rightPath is None:
        print("No right path found")
    
    print(f"Left path cost: {aStarLeft.total_cost}")
    print(f"Right path cost: {aStarRight.total_cost}")
    
    path = []
    if aStarLeft.total_cost < aStarRight.total_cost:
        path = leftPath
    else:
        path = rightPath
    
    for node in path:
        print(node)
        
    drawCircles(screen, circles, path)
    
    

if __name__ == '__main__':
    main()
        
        
