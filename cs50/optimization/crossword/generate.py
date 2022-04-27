import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate over all the keys of the dic, which are variables
        for variable in self.domains:

            # Iterate over all the values the dict holdes for the variable
            for domain_value in self.domains[variable]:

                # If the length of the value is not equal to the variables length.
                # it does not satify the unary constraints!
                if len(domain_value) == variable.length:
                    
                    # Remove the value from the variables domain
                    self.domains[variable].remove(domain_value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        
        # Get the overlap of the two variables
        overlap = self.crossword.overlaps.get((x, y))

        # If there is an overlap between the two variables
        if overlap is not None:

            # Loop through the whole domain of x
            for domain_value_of_x in self.domains[x]:

                # For each domain value of x, loop through the whole domain of y
                for domain_value_of_y in self.domains[y]:
                    
                    # Check if the current domain values of x and y have the same value at the overlap
                    # If that is not the case they do not satisfy the binary constraints
                    if domain_value_of_x[overlap[0]] != domain_value_of_y[overlap[1]]:

                        # Delete the domain value, since it does not satisfy the binary constraints
                        self.domains[x].remove(domain_value_of_x)

                        # Set revised to True since changes where made
                        revised = True
        
        return revised
    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If the arcs is none initialize arcs with all the arcs of the csp
        if arcs == None:
            arcs = []

            # For each variable try if there exists an overlap with a other variable
            # If that is the case add both variables to the arcs list/queue
            for x in self.crossword.variables:

                for y in self.crossword.variables:

                    if self.crossword.overlaps.get((x, y)) != None:
                        arcs.append((x, y))

        # While there are still arcs in the queue
        while arcs is not []:

            # Get one arc
            current_arc = arcs.pop(0)

            # Call the revise function with the current arc as argument
            # If the arc is revised, if the funtion returns true
            if self.revise(current_arc[0], current_arc[1]):

                # If the domain of the variable is empty return false
                # The algorithm was not able to make the csp arc consitent
                if len(self.domains[current_arc[0]]) == 0:
                    return False

                # Get all the neighbor of the variable which domain got edited
                neighbors = self.crossword.neighbors(current_arc[0])

                # Delete the variable from the neighbors which was included as argument 
                # when calling the revise function
                neighbors.remove(current_arc[1])

                # Add new arcs to the queue, from each neighbor to the variable which domain
                # got edited
                for z in neighbors:
                    arcs.append((z, current_arc[0]))
        # the algorithm was successful in making the csp arc consisten
        return True


        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # For each variable in the assignment
        for variable in assignment:

            # Check if the value of the variable is smaller than 2
            # => if it is smaller than 2 it is not a word
            if len(assignment[variable]) < 2:
                return False

        # If all the values of the assignment diconary are words the assignment is complete
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        for x in assignment:
            for y in assignment:
                if self.crossword.overlaps.get((x, y)) is not None:
                    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()