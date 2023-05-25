# AStarPathfinding
A* Pathfinding algorithm to find the shortest path taken, touching either the left or right side of each circle.

Uses a heuristic of # of circles from the goal (last circle). Cost is the euclidean distance from the start circle.

For demonstration purposes, creates a random set of points, going down at a regular interval. Draws the circles and path taken using `pygame`.
