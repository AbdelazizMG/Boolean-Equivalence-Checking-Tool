import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
import pydot

from graphviz import Source
class Drawer:

    #Constuctor
    def __init__(self):
         super(Drawer,self).__init__()
         self.counter = 0
    
    def draw(self,list1):

            self.__graph1 = pydot.Dot(graph_type='digraph')
            label_value_left  = 0
            label_value_right = 0

            # Add nodes to the graph
            for  i in range(0,len(list1)):
                self.__graph1.add_node(pydot.Node(list1[i].data))
                print("node:",list1[i].data)
                if(list1[i].left != None):
                    if(type(list1[i].left.data)==type("y") and len(list1[i].left.data)==1):
                        label_value_left=label_value_left + 1
                        list1[i].left.data=list1[i].left.data+ "% s" % label_value_left  
                        label_value_left_string= "% s" % label_value_left
                        list1[i].left.data= list1[i].left.data.rstrip(label_value_left_string)

                        label_value_left=label_value_left+1
                        list1[i].left.data=list1[i].left.data+ "% s" % label_value_left

                    print(list1[i].left.data)
                    self.__graph1.add_edge(pydot.Edge(list1[i].data, list1[i].left.data, color="blue", style="dashed"))
                    if(type(list1[i].right.data)==type("y") and len(list1[i].right.data)==1):
                        label_value_right=label_value_right + 1
                        list1[i].right.data=list1[i].right.data+"% s" % label_value_right
                        label_value_right=label_value_right+1
                        #list1[i].right.data=list1[i].right.data+"% s" % label_value_right
                        #label_value_right=label_value_right+1
                    print(list1[i].right.data)
                    self.__graph1.add_edge(pydot.Edge(list1[i].data, list1[i].right.data))

            # Generate the DOT string
            dot_str1 = self.__graph1.to_string()
            #print(dot_str1)

            src1 = Source(dot_str1)
            src1.format = 'png'
            src1.render('render_pdf_name4',view=False)

            # Write the DOT string to a file
            with open('graph1.dot', 'w') as f:
                f.write(dot_str1)
                
            # Convert the DOT file to a PNG image
            (self.__graph1,) = pydot.graph_from_dot_file('graph1.dot')
            self.__graph1.write_png(f'graph{self.counter}.png')   
            self.counter = self.counter + 1

            if(self.counter == 4):
                 self.counter = 0