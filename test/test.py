import unittest

import sys 
sys.path.append("..")
#print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)
from template_app import Builder
from template_app import Template

#from template_app import Builder

class TestBuilder(unittest.TestCase):

    def test_add_line(self):
        obj=Builder()

        self.assertEqual(obj.codelines,[])

        obj.add_line("def(text,content):")
        self.assertEqual(obj.codelines,["def(text,content):\n"])

        obj.add_line("context[optional]=Invalid")
        self.assertEqual(obj.codelines,["def(text,content):\n","context[optional]=Invalid\n"])

        # Make a new codebuilder object

        obj2=Builder()

        self.assertEqual(obj2.codelines,[])

        obj2.add_line("class Adding:")

        self.assertEqual(obj2.codelines,["class Adding:\n"])

        obj2.add_line("def __init__(self,nums):")

        self.assertEqual(obj2.codelines,["class Adding:\n","def __init__(self,nums):\n"])

    def test_indent(self):

        obj1=Builder()

        print(obj1)

        obj1.add_line("class healer:")

        obj1.addIndent()

        obj1.add_line("def __init__(self):")

        self.assertEqual(obj1.codelines,["class healer:\n","    def __init__(self):\n"])

        obj1.addIndent()
        obj1.add_line("self.value=[]")

        obj1.deindent()

        obj1.add_line("class_var2")

        self.assertEqual(obj1.codelines,["class healer:\n","    def __init__(self):\n","        self.value=[]\n","    class_var2\n"])

    
    def test_str(self):

        obj1=Builder()

        self.assertEqual(obj1.__str__(),"")

        obj1.add_line("class healer:")

        self.assertEqual(obj1.__str__(),"class healer:\n")
        
        obj1.addIndent()

        obj1.add_line("def __init__(self):")

        self.assertEqual(obj1.__str__(),"class healer:\n    def __init__(self):\n")

        obj1.addIndent()
        obj1.add_line("self.value=[]")

        self.assertEqual(obj1.__str__(),"class healer:\n    def __init__(self):\n        self.value=[]\n")

        
        obj1.deindent()

        obj1.add_line("class_var2")

        self.assertEqual(obj1.__str__(),"class healer:\n    def __init__(self):\n        self.value=[]\n    class_var2\n")
    
    # The test for the template class will start here
    def test_template(self):
        template = Template('''
    <h1>Hello {{name|upper}}!</h1>
    {% for topic in topics %}
        <p>You are interested in {{topic}}.</p>
    {% endfor %}
    ''',
    {'upper': str.upper},)


        print(template.render({'name':"ned","topics":["Math","Science"]}))











if __name__ == '__main__':
    unittest.main()

    