from collections import defaultdict
import copy
import glob

# using defaultdict instead of normal dict to avoid keyError
# indeg0 array is used to start a path
# outdeg0 array is used to determine end of a path

class Graph :

    def __init__ (self, nodes):
        self.nodes = nodes
        self.indeg0 = [True]*self.nodes
        self.outdeg0 = [True]*self.nodes
        self.adjNodes = defaultdict(list)
        self.allpaths = []
    
    def createGraph(self,edges):

        for edge in edges:
            # getting all nodes with 0 in-degree and 0 out-degree
            if len(edge) > 1:

                first, second = edge[0], edge[1]
                # storing all adjacent nodes for a node to list
                self.adjNodes[first].append(second)
                
                # second node has incoming vertex from first,
                # set indeg0[second] -> false
                self.indeg0[second] = False

                # first node has outgoing vertex to second,
                # set outdeg0[u] -> false
                self.outdeg0[first] = False

    def findAllPaths (self):
        print("adjNodes", self.adjNodes)
        for i in range(self.nodes):
            # for each node with in-degree 0
            # print all possible paths
            if self.indeg0[i] and self.adjNodes[i]:
                # clear previously stored path
                path = []
                path.append(i)
                self.DFS(i, path)
            
            # if a node is 0 in-degree but doesn't have any adjacent node
            if self.indeg0[i] and not self.adjNodes[i]:
                    self.allpaths.append([i])

        # print all paths starting from 0 in-degree nodes
        self.printPaths ()
        return self.allpaths

    def printPaths (self):
        # print (self.allpaths)
        for path in self.allpaths:
            print(*path, sep='->')

    # recursive function to find all the paths in a graph
    def DFS (self, current_node, current_path):
        
        # current node has out-degree 0 that means end of a path,
        # add current path to all paths
        if self.outdeg0[current_node]:
            self.allpaths.append(copy.deepcopy(current_path))
        else:
            for adjnode in self.adjNodes[current_node]:
                # append adjacent node to current path
                current_path.append(adjnode)
                
                # call recursive function to progress through path 
                self.DFS (adjnode,current_path)
                # current path is completed, remove last node from path to backtrack
                current_path.pop()
                

def main():
    # read text datafile to get the data for graph
    for filename in glob.glob('*.txt'):
        print("reading data for filename: ",filename)
        try:
            with open(filename, 'r') as f:
                data = [line.strip() for line in f]
                # first line is number of nodes
                nodes = int(data[0])
                # next lines are list of edges between first and second node
                # create a list of all edges
                edges = [list(map(int,edge.split(','))) for edge in data[1::]]
                
                # intialize graph with number of nodes
                dag = Graph(nodes)

                # create adjacent nodes values for graph and,
                # update nodes for 0 in-degree, 0 out-degree
                dag.createGraph(edges)

                # find all path in dag starting 0 in-degree
                all_paths = dag.findAllPaths()
                print("all_paths",all_paths, "\n")
        except Exception as err:
            print("error while reading file and creating graph: ", err, '\n')
            

if __name__ == "__main__":
    main()
