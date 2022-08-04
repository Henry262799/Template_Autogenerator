
class Builder:
    
    # The following class functions as code building class where we can build python code and render it as a string output for the user


    # Global standard indent level (According to pep8 standards)
    INDENT_LEVEL=4

    # Initalizes the Builder object 
    def __init__(self,indent=0):

        # This line contains all of the lines of code that will be returned in our returned function
        self.codelines=[]

        # This keep track of the current indentation level
        self.indent=indent
    

    def add_line(self,text):
        """
        # Add a line of code to the function that we are building 

        @param text: The content of the line that we want to our function

        """
        text=self.indent*" "+text +"\n"
        # Each line is an array so later when we join all off the arrays we can just call the join function one time
        arr_val=[text]
        self.codelines.extend(arr_val)
    

    def addIndent(self):
        """
        Increase the current indent level by the pep8 standard indentation
        """
        self.indent=self.indent+Builder.INDENT_LEVEL
        #self.indent=self.indent+4
    
    def deindent(self):
        """
        Decreases the current indent level by the pep8 standard indentation
        """
        self.indent=self.indent-Builder.INDENT_LEVEL

    
    def add_section(self):
        """
        Adds another builder to the code this simulates that sometimes we want to go back to a line of code to add code or remove code 
        from the given section
        """

        new_builder=Builder(indent=self.indent)
        self.codelines.append(new_builder)
        return new_builder

    def retrieve_globals(self):
        pass

    
    def __str__(self) -> str:
        """
        Outputs the code representation as a string that can be copied  
        """
        
        output=""
        for e in self.codelines:

            if e==type(list):
                output=output.join(e)
            else:
                output=output+e.__str__()
        
        return output
    

    def get_globals(self):
        """Execute the code, and return a dict of globals it defines."""
        # A check that the caller really finished all the blocks they started.
        assert self.indent == 0
        # Get the Python source as a single string.
        python_source = str(self)
        # Execute the source, defining globals, and return them.
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace

    
        