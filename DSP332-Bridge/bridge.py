#!/bin/env python
# Author: Martins Savickis 211RDB117 10.grupa

class Node:
    """
    Node class represents a node or a state in a graph.

    [Attributes]
        A_SIDE : tuple()
            The starting side of the bridge.
            Format ([<PLAYERS>], <TORCH>).
        B_SIDE : tuple()
            The target side of the bridge.
            Format ([<PLAYERS>], <TORCH>).
        parent : Node
            The parent node (Could be optimized for multiple parent nodes).
        children : list()
            A list of child nodes in the graph.
        is_dead_end : bool
            Is this a dead end node.
            No children, No target state.
        is_target_node : bool
            Is this a target node.
            No children, Target state reached.
    
    [Methods]
        findChildren():
            Find all of the child nodes.
        print(int):
            Print the node in ASCII.
    """

    def __init__(self, a_side, b_side, parent, children):
        """Constructor method that creates a new node object."""
        self.A_SIDE = a_side
        self.B_SIDE = b_side

        self.parent = parent
        self.children = children

        self.is_dead_end = False
        self.is_target_state = False

    def findChildren(self):
        """
        A method that finds all of the node children.

        [Notes]
            Method looks for the side that has the torch.
            It then generates a list of possible crosser configurations.
        
        [Returns]
            A list of tuples (Sides).
            Format ([<PLAYERS>], <TORCH>).
        """

        A_crossers = self.A_SIDE[0]
        A_torch = self.A_SIDE[1]
        B_crossers = self.B_SIDE[0]
        B_torch = self.B_SIDE[1]
        
        # An array to store found children
        children = []

        if A_torch != None:

            # Loops over crossers to create crossing pairs
            for crosser in A_crossers:
                
                # Find the next crosser to the current one
                n = A_crossers.index(crosser) + 1

                for next_index in range(n, len(A_crossers)):

                    # Find the maximum crossing time
                    time = max(crosser[1], A_crossers[next_index][1])

                    # Check if the crossing is legal
                    if (next_torch := A_torch - time) >= 0:

                        # Create lists of child coasts
                        child_B = list(B_crossers)
                        child_B.append(crosser)
                        child_B.append(A_crossers[next_index])
                        
                        child_A = list(A_crossers)
                        child_A.remove(crosser)
                        child_A.remove(A_crossers[next_index])
                        
                        children.append(((child_A, None), (child_B, next_torch)))
            return children
        else:
            # Check for the target state
            # Target state only happens if the torch is on the target side
            if len(A_crossers) == 0:
                self.is_target_state = True
                return children

            for crosser in B_crossers:
                if (next_torch := B_torch - crosser[1]) >= 0:

                    # Create lists of the child coasts
                    child_A = list(A_crossers)
                    child_A.append(crosser)

                    child_B = list(B_crossers)
                    child_B.remove(crosser)

                    children.append(((child_A, next_torch), (child_B, None)))
            return children
    
    def print(self, tabs):
        """
        A method that prints out the node in plain text.
        Format: <SIDE>(<PLAYERS>)-<TORCH>
        
        [Parameters]
            An integer that specifies the amount of tabs to prefix.
            This is used to create a tree like structure.
        """

        print('\t' * tabs + 'A(', end='')
        
        for crosser in self.A_SIDE[0]:
            print(crosser[0], end='')
        
        print(')-' + str(self.A_SIDE[1]), end='')
        
        # Print if the node is a final node
        if self.is_dead_end:
            print(' --- DEAD END')
        elif self.is_target_state:
            print(' --- REACHED TARGET STATE')
        else:
            print()
        
        print('\t' * tabs + 'B(', end='')

        for crosser in self.B_SIDE[0]:
            print(crosser[0], end='')

        print(')-' + str(self.B_SIDE[1]))

class Graph(object):
    """
    An object that represents a Graph/Tree of nodes.

    [Attributes]
        crossers : list()
            A list of tuples that represent crossers.
            This is the start state.
        torch : int
            The amount of the torch given.

    [Methods]
        make():
            Used to create the root node.
            Then invokes the recursive function.
        makeCascade(Node):
            A recursive function to generate nodes.
        print():
            Used to print the format.
            Then invokes the recursive function.
        printCascade():
            Recursively prints nodes.
            Increments the tabs for a tree structure.
    """

    def __init__(self, crossers, torch):
        """Initializes graph with root nodes attributes."""
        self.crossers = crossers

        self.A_SIDE = (self.crossers, torch)
        self.B_SIDE = ([], None)

    def make(self):
        """Creates the root node and runs the recursive generation."""
        self.root_node = Node(self.A_SIDE, self.B_SIDE, [], [])
        self.makeCascade(self.root_node)

    def makeCascade(self, node):
        """
        A recursive method to generate child nodes.
        This method also checks for the dead end state.

        [Parameters]
            node : Node
                The node to generate child nodes.
                The nodes are added to the children list.
        """

        child_list = node.findChildren()

        if len(child_list) == 0:
            if not node.is_target_state:
                node.is_dead_end = True
                return 

        for child in child_list:
            new = Node(child[0], child[1], node, [])
            node.children.append(new)
            self.makeCascade(new)
    
    def print(self):
        """Prints the format and invokes recursive graph printing."""
        print()
        print("Output format:")
        print("<BRIDGE_SIDE>(<PLAYERS>)-<TORCH>")
        print()
        self.printCascade(self.root_node, 0)

    def printCascade(self, node, tabs):
        """
        A recursive method to print nodes.

        [Parameters]
            node : Node
                The node to print.
            tabs : int
                The node level.
                This dictates the indent.
        """

        node.print(tabs)

        for child in node.children:
            self.printCascade(child, tabs=tabs+1)

if __name__ == '__main__':
    print('Author: Martins Savickis 211RDB117 10.grupa')
    
    graph = Graph([('A', 1), ('B', 3), ('C', 5)], 12)
    graph.make()
    graph.print()