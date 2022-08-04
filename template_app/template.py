from template_app import Builder
import re
class Template:

    def _expr_code(self, expr):
        """Generate a Python expression for `expr`."""
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.vars)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])
            code = "do_dots(%s, %s)" % (code, args)   
        else:
            self._variable(expr, self.vars)
            code = "c_%s" % expr
        return code

    def _syntax_error(self, msg, thing):
        """Raise a syntax error using `msg`, and showing `thing`."""
        raise SyntaxError("%s: %r" % (msg, thing))
    
    def _variable(self, name, vars_set):
        """Track that `name` is used as a variable.

        Adds the name to `vars_set`, a set of variable names.

        Raises an syntax error if `name` is not a valid name.

        """
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._syntax_error("Not a valid name", name)
        vars_set.add(name)
    
    def _do_dots(self, value, *dots):
        """Evaluate dotted expressions at runtime."""
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value

    def __init__(self,text,*info):
        # The info that is passed into the constructor must be an iterable object with a key and value pair describing its functionalit

        self.info={}

        for e in info:
            self.info.update(e)

        # Initalize a set so we can get the context defintion easily
        self.vars=set()
        # Initalize a set to keep track of all the variables that are in the template
        self.temp_var=set()


        #Building the inital part of the code that we will return 
        code=Builder()

        code.add_line("def renderFunc(text,do_dots):")
        code.addIndent()
        variable_code=code.add_section()
        code.add_line("result=[]")
        code.add_line("append_meth=result.append")
        code.add_line("extend_meth=result.extend")
        code.add_line("to_str=str")

        #Inner helper function here since we need to decide when and how many string lines we should append to our return
        buffer=[]
        def flush():
            """
            To prevent our code building class from being too complicated we design the buffer here so that we can add to our code efficently
            """

            if len(buffer)==1:
                code.add_line("append_meth(%s)" % buffer[0])
            elif len(buffer)>1:
                code.add_line("extend_meth([%s])"%",".join(buffer))
            del buffer[:]

        operation_control=[]



        # Parsing the html template using regular expressions
        tokens=re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)

        for token in tokens:
            
            # We have four different types of tokens that we would like to deal with

            #1 The comment: There is no reason for us to parse the comment in the template
            if token.startswith("{#"):
                continue
            # 2 Expression that we need to evaluate
            elif token.startswith("{{"):
                # Convert this expression to python code
                # We will make the function _expr_code later that will evalute the functions
                expr=self._expr_code(token[2:-2].strip())
                buffer.append("to_str(%s)"% expr)
            # 3 Control structures
            elif token.startswith("{%"):
                flush()
                control=token[2:-2].strip().split()

                if control[0]=="if":

                    if len(control)!=2:
                        self._syntax_error("If statement does not make sense",token)
                    operation_control.append("if")
                    code.add_line("if %s:" % self._expr_code(control[1]))
                    code.addIndent()
                elif control[0]=="for":

                    if len(control)!=4 or control[2]!="in":
                        self._syntax_error("For statement does not make sense",token)
                    
                    operation_control.append("for")
                    self._variable(control[1],self.temp_var)
                    code.add_line(
                        "for c_%s in %s:" % (
                            control[1],
                            self._expr_code(control[3])
                        )
                    )
                    code.addIndent()

                elif control[0].startswith('end'):
                    # Endsomething.  Pop the ops stack.
                    if len(control) != 1:
                        self._syntax_error("Don't understand end", token)
                    end_control = control[0][3:]
                    if not operation_control:
                        self._syntax_error("Too many ends", token)
                    start_control = operation_control.pop()
                    if start_control != end_control:
                        self._syntax_error("Mismatched end tag", end_control)
                    code.deindent()
                else:
                    self._syntax_error("Don't understand tag", control[0])
            else:
                # The remaining element is not an if, for or an end so it must be content and we only want it if its not no content
                if token:
                    buffer.append(repr(token))
        
        if operation_control:
            self._syntax_error("Unmtached tag error",operation_control[-1])
        
        # Add our new code to the original code that we are currently developing right now
        flush()

        # We need to add all of the names that are in all_vars but that were not already included by the loop variables 
        #as that would be duplicate code.
        for var_name in self.vars - self.temp_var:
            variable_code.add_line("c_%s = text[%r]" % (var_name, var_name))
                    
        code.add_line("return ''.join(result)")
        code.deindent()

        self._render_function = code.get_globals()['renderFunc']
        self.function_str=code.__str__()

    def render(self, context=None):
        """Render this template by applying it to `context`.

        `context` is a dictionary of values to use in this rendering.

        """
        # Make the complete context we'll use.
        render_context = dict(self.info)
        if context:
            render_context.update(context)
            
        return self._render_function(render_context, self._do_dots)