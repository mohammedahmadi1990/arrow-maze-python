from collections import deque

class SpanishRice:        

    # init from file
    def init_maze(self, file_path):
        with open(file_path, "r") as file:
            n = len(file.readline().strip().split(","))

        arr = [[0 for j in range(n)] for i in range(n)]

        with open(file_path, "r") as file:
            for i in range(n):
                line = file.readline().strip().split(",")
                for j in range(n):
                    arr[i][j] = line[j]
        return arr


    # print maze
    def print_maze(self, arr):
        for i in range(len(arr)):              
                print(arr[i][:])


    # Define the successor function
    def expand(self, maze, state):
        n = len(maze)
        x, y = state
        successors = []
        if maze[x][y] == 'N':
            for i in range(x-1, -1, -1):
                if maze[i][y] == '':
                    break
                if i >= 0 and i < n and y >= 0 and y < n:
                    successors.append((i, y))
        elif maze[x][y] == 'S':
            for i in range(x+1, n):
                if maze[i][y] == '':
                    break
                if i >= 0 and i < n and y >= 0 and y < n:
                    successors.append((i, y))
        elif maze[x][y] == 'W':
            for j in range(y-1, -1, -1):
                if maze[x][j] == '':
                    break
                if x >= 0 and x < n and j >= 0 and j < n:
                    successors.append((x, j))
        elif maze[x][y] == 'E':
            for j in range(y+1, n):
                if maze[x][j] == '':
                    break
                if x >= 0 and x < n and j >= 0 and j < n:
                    successors.append((x, j))
        elif maze[x][y] == 'SW':
            i, j = x + 1, y - 1
            while i < n and j >= 0:
                if maze[i][j] == '':
                    break
                if i >= 0 and i < n and j >= 0 and j < n:
                    successors.append((i, j))
                i += 1
                j -= 1
        elif maze[x][y] == 'SE':
            i, j = x + 1, y + 1
            while i < n and j < n:
                if maze[i][j] == '':
                    break
                if i >= 0 and i < n and j >= 0 and j < n:
                    successors.append((i, j))
                i += 1
                j += 1
        elif maze[x][y] == 'NW':
            i, j = x - 1, y - 1
            while i >= 0 and j >= 0:
                if maze[i][j] == '':
                    break
                if i >= 0 and i < n and j >= 0 and j < n:
                    successors.append((i, j))
                i -= 1
                j -= 1
        elif maze[x][y] == 'NE':
            i, j = x - 1, y + 1
            while i >= 0 and j < n:
                if maze[i][j] == '':
                    break
                if i >= 0 and i < n and j >= 0 and j < n:
                    successors.append((i, j))
                i -= 1
                j += 1
        return successors


    # Breadth-First-Search (BFS) method
    def bfs(self, maze):
        start = (0, 0)
        goal = (len(maze) - 1, len(maze) - 1)
        queue = deque([(start, [start])])
        visited = set()
        num_edges = 0
        while queue:
            num_edges += 1
            (x, y), path = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == goal:
                return ('Y', len(path) - 1, len(path) - 1, num_edges, path)
            for x2, y2 in self.expand(maze, (x, y)):                
                queue.append(((x2, y2), path + [(x2, y2)]))
        return ('N', -1, -1, num_edges, None)


    # Depth-First-Search (DFS) method
    def dfs(self, maze):
        start = (0, 0)
        goal = (len(maze) - 1, len(maze) - 1)
        stack = [(start, [start])]
        visited = set()
        num_edges = 0
        while stack:
            num_edges += 1
            (x, y), path = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == goal:
                return ('Y', len(path) - 1, len(path) - 1, num_edges, path)
            for x2, y2 in reversed(self.expand(maze, (x, y))):
                stack.append(((x2, y2), path + [(x2, y2)]))
        return ('N', -1, -1, num_edges, None)


    # Iterative-Deepening-Search (IDS) method
    def ids(self, maze):
        start = (0, 0)
        goal = (len(maze) - 1, len(maze) - 1)
        depth = 0
        num_edges = 0
        while True:
            result = self.depth_limited_search(maze, start, goal, depth, num_edges)
            if result[0]:
                return result
            depth += 1

    # Helper method for the IDS
    def depth_limited_search(self, maze, start, goal, depth_limit, num_edges):
        stack = [(start, [start], 0)]
        visited = set()
        while stack:
            (x, y), path, depth = stack.pop()
            num_edges += 1
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) == goal:
                return ('Y', len(path) - 1, len(path) - 1, num_edges, path)
            if depth < depth_limit:
                for x2, y2 in reversed(self.expand(maze, (x, y))):
                    stack.append(((x2, y2), path + [(x2, y2)], depth + 1))
        return ('N', -1, -1, num_edges, None)


    def solutionAsList(self, cell_list, n):
        if(cell_list[0]=='Y'):
            result =[]        
            for i in range(len(cell_list[4])):
                result.append(cell_list[4][i][0] * n + cell_list[4][i][1]+1)
            return result
        return None

    
    def save_report_file(self, input_file, n, output_file):   
        maze = self.init_maze(input_file)     
        with open(output_file, "w") as f:             
            for i in range(len(maze)):  
                f.write(", ".join(str(item) for item in maze[i]))  
                f.write("\n")      

            f.write("\n\nBFS Solver: ")
            bfs_output = self.bfs(maze)
            f.write("\n[")
            f.write(",".join(str(item) for item in bfs_output))
            mylist = self.solutionAsList(bfs_output,n)
            f.write("]\nPath as List: ")
            if(mylist != None):
                f.write(",".join(str(item) for item in mylist))
            else:
                f.write("None")

            f.write("\n\nDFS Solver: ")
            dfs_output = self.dfs(maze)
            f.write("\n[")            
            f.write(",".join(str(item) for item in dfs_output))
            mylist = self.solutionAsList(dfs_output,n)
            f.write("]\nPath as List: ")
            if(mylist != None):
                f.write(",".join(str(item) for item in mylist))
            else:
                f.write("None")

            f.write("\n\nIDS Solver: ")
            ids_output = self.ids(maze)
            f.write("\n[") 
            f.write(",".join(str(item) for item in ids_output))
            mylist = self.solutionAsList(ids_output,n)
            f.write("]\nPath as List: ")
            if(mylist != None):
                f.write(",".join(str(item) for item in mylist))
            else:
                f.write("None")


########################## APP STARTS HERE ##########################

# object creation
solver = SpanishRice()

# Init file 1
# Solution: 1 3 7 4 6 9
input_file1 = 'maze1.txt'
output_file1 = 'report_maze1.txt'
n = 3
solver.save_report_file(input_file1, n, output_file1)

# Init file 2
# Solution: 1 3 24 34 13 31 7 9 33 23 35 36
input_file2 = 'maze2.txt'
output_file2 = 'report_maze2.txt'
n = 6
solver.save_report_file(input_file2, n, output_file2)

# Init file 3
# Solution: 1 33 60 39 55 50 26 12 14 23 21 28 64
input_file2 = 'maze3.txt'
output_file2 = 'report_maze3.txt'
n = 8
solver.save_report_file(input_file2, n, output_file2)





