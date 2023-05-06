num_variables= 2
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
import inspect
import pydot

from graphviz import Source
class node:
    def __init__(self,var,label):
        self.data = var
        self.right = None
        self.left = None
        self.label = label

class BDD:
    def __init__(self):
        pass
    def start(self,vars,TT_output):
            init = 1
            nodes = []
            counter = 0
            TT_output.reverse()
            for v in vars:
                for i in range(0,init):
                    nodes.append(v)
                init = init * 2
            for v in TT_output:
                if v == 'T':
                    TT_output[counter] = 1
                else: 
                    TT_output[counter] = 0
                counter = counter + 1
            nodes_list = []
            label = len(nodes)+1
            for i in range(0,len(nodes)):
                temp = node(nodes[i],label)
                nodes_list.append(temp)
                label = label - 1
            for i in range(0,len(TT_output)):
                temp = node(TT_output[i],TT_output[i])
                nodes_list.append(temp)
            step = 1
            counter = step
            for i in range(0,len(nodes)):
                nodes_list[i].right = nodes_list[(step-1)*2+1 + (step - counter)*2]
                nodes_list[i].left = nodes_list[(step-1)*2+2 + (step - counter)*2]
                counter = counter - 1
                if counter == 0:
                    step = step*2
                    counter = step      
            return nodes_list 
class ROBDD:
    def __init__(self):
        self.Parent_Add = None

    def assign_labels(self,list):                                                       #ROBDD
        for i in range(pow(2, num_variables), len(list)):
            if(list[i].left.label == list[i].right.label):
                list[i].label = list[i].left.label

        temp = list[pow(2, num_variables): ]
        index=0
        for i in range(num_variables-1, -1, -1):   #number of variables= number of levels
            for j in range(0, pow(2, i)):
                for k in range(0, pow(2, i)):
                    if(temp[index+j] != temp[index+k]) and (temp[index+j].left.label==temp[index+k].left.label) and (temp[index+j].right.label==temp[index+k].right.label):
                        temp[index+k].label=temp[index+j].label
            index=index+pow(2, i)
        
        for i in range(pow(2, num_variables), len(list)):
            if(list[i].left.label == list[i].right.label):
                list[i].label = list[i].left.label

        list[pow(2, num_variables): ]=temp
        return list
    # end of assign_labels function

        ######Parent_Find#########
    def findParent(self,node,current_add,parent_add) -> None:
            if (node is None):
                return None
            # If current node is
            # the required node
            if (node == current_add):  
                # Print its parent
                self.Parent_Add = parent_add
            else:
                # Recursive calls
                # for the children
                # of the current node
                # Current node is now
                # the new parent
                self.findParent(node.left,current_add,node)
                self.findParent(node.right,current_add,node)


    ########Reduction########
    def Remove_Nodes(self,list, Reduced_List):
        for i in range(0,len(list)):
            if(list[i].label==0):
                self.findParent(list[-1], list[i], -1)
                if(self.Parent_Add.left==list[i]):
                    self.Parent_Add.left= Reduced_List[0]
                else:
                    self.Parent_Add.right= Reduced_List[0]
                list[i].label=-1
            elif(list[i].label==1):
                self.findParent(list[-1], list[i], -1)
                if(self.Parent_Add.left==list[i]):
                    self.Parent_Add.left= Reduced_List[1]
                else:
                    self.Parent_Add.right= Reduced_List[1]
                list[i].label=-1
            else:
                if(list[i].left.label==list[i].right.label) and (list[i].left.label!=-1) and (list[i].right.label!=-1):
                    list[i].label = -1
                    #print("else:")
                    #print(str(i))
                    #print("------------")
                    self.findParent(list[-1], list[i], -1)
                    #if list[i].data == 'b':
                    #print(i)
                    #print(Parent_Add)
                    if( (self.Parent_Add != None) and (self.Parent_Add != -1)):
                        if(self.Parent_Add.left==list[i]):
                            #print(Parent_Add)
                            #print(Parent_Add.left)
                            #print(Parent_Add.right)
                            #print(list[i])
                            #list[i].right = list[i].left
                            self.Parent_Add.left= list[i].right
                        else:
                            #list[i].right = list[i].left
                            self.Parent_Add.right= list[i].right
        
        #print("****** BEFORE *******")
        #for i in range(0,len(list)):
        #    print("\n")
        #    print("Node: ", i)
        #    #print(i)
        #    print("Data: ", list[i].data)
        #    print("Label: ",list[i].label)
        #    if(list[i].left != None):
        #        print("Left: ",list[i].left.data)
        #        print("Right: ",list[i].right.data)
        #print("****** BEFORE *******")
        #findParent(list[-1],list[8],-1)
        #print("node 8")
        #print("label: "+str(Parent_Add.label))
        #print("data: "+Parent_Add.data)
        #print(Parent_Add)
        #findParent(list[-1],list[9],-1)
        #print("node 9")
        #print("label: "+str(Parent_Add.label))
        #print("data: "+Parent_Add.data)
        #print(Parent_Add)
        #findParent(list[-1],list[10],-1)
        #print("node 10")
        #print("label: "+str(Parent_Add.label))
        #print("data: "+Parent_Add.data)
        #print(Parent_Add)
        #print(list[-1])
        #temp = list[pow(2, num_variables): ]
        index=0
        init = pow(2, num_variables)
        #print("****** AFTER *******")
        for i in range(num_variables-1, -1, -1):   #number of variables= number of levels
            for j in range(init, pow(2, i)+init):
                if(list[j+index].label!=-1):
                    for k in range(init, pow(2, i)+init):
                        if(list[index+j] != list[index+k]) and (list[index+j].label==list[index+k].label):
                            #print("node: "+str(k))
                            list[index+k].label=-1
                            self.findParent(list[-1], list[index+k], -1)
                            #print("Parent label: ",Parent_Add.label)
                            ##print("left: ",Parent_Add.left.data)
                            #print("Parent data: ",Parent_Add.data)
                            #print("right: ",Parent_Add.right.data)
                            if(self.Parent_Add.left==list[index+k]):
                                self.Parent_Add.left= list[index+j]
                            else:
                                self.Parent_Add.right= list[index+j]
            index=index+pow(2, i)
        #print("****** AFTER *******")
        #for i in range(0,len(list)):
        #    print("\n")
        #    print("Node: ", i)
        #    #print(i)
        #    print("Data: ", list[i].data)
        #    print("Label: ",list[i].label)
        #    if(list[i].left != None):
        #        print("Left: ",list[i].left.data)
        #        print("Right: ",list[i].right.data)
        init = pow(2, num_variables)
        for i in range(init,len(list)):
            if (list[i].label != list[i].label):
                list[i] = list[i]
        #list[pow(2, num_variables): ]=temp
        for i in range(0, len(list)):
            if(list[i].label!=-1):
                Reduced_List.append(list[i])
        return Reduced_List
class Equivalence_Checker:
    def __init__(self,List1,List2):
        if (len(List1) != len(List2)):
            return 0
        else:
            flag = 0
            for i in range(0,len(List1)):
                if (List1[i].left!=None) and (List2[i].left!=None):
                    if (List1[i].data == List2[i].data) and (List1[i].left.data == List2[i].left.data) and (List1[i].right.data == List2[i].right.data):
                        flag = 1
                    else:
                        flag = 0
                        break
            return flag
class Drawer:

    #Constuctor
    def __init__(self,list1):
            super(Drawer,self).__init__()

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
            src1.render('render_pdf_name4',view=True)

            # Write the DOT string to a file
            with open('graph1.dot', 'w') as f:
                f.write(dot_str1)
                
            # Convert the DOT file to a PNG image
            (self.__graph1,) = pydot.graph_from_dot_file('graph1.dot')
            self.__graph1.write_png('graph1.png')
'''        
def Equivalence_Checker(List1,List2):
        if (len(List1) != len(List2)):
            return 0
        else:
            flag = 0
            for i in range(0,len(List1)):
                if (List1[i].left!=None) and (List2[i].left!=None):
                    if (List1[i].data == List2[i].data) and (List1[i].left.data == List2[i].left.data) and (List1[i].right.data == List2[i].right.data):
                        flag = 1
                    else:
                        flag = 0
                        break
            return flag
    
def BDD(vars,TT_output):
    init = 1
    nodes = []
    counter = 0
    TT_output.reverse()
    for v in vars:
        for i in range(0,init):
            nodes.append(v)
        init = init * 2
    for v in TT_output:
        if v == 'T':
            TT_output[counter] = 1
        else: 
            TT_output[counter] = 0
        counter = counter + 1
    nodes_list = []
    label = len(nodes)+1
    for i in range(0,len(nodes)):
        temp = node(nodes[i],label)
        nodes_list.append(temp)
        label = label - 1
    for i in range(0,len(TT_output)):
        temp = node(TT_output[i],TT_output[i])
        nodes_list.append(temp)
    step = 1
    counter = step
    for i in range(0,len(nodes)):
        nodes_list[i].right = nodes_list[(step-1)*2+1 + (step - counter)*2]
        nodes_list[i].left = nodes_list[(step-1)*2+2 + (step - counter)*2]
        counter = counter - 1
        if counter == 0:
            step = step*2
            counter = step      
    return nodes_list 
'''
############################################ TESTING #####################

BDD_Obj = BDD()
list1 = BDD_Obj.start(['a','b'],['F','F','F','T'])
drawer = Drawer(list1)
list1 = BDD_Obj.start(['a','b'],['F','F','F','T'])
list1.reverse()
ROBDD_Obj = ROBDD()
labelled_list1 = ROBDD_Obj.assign_labels(list1)
Reduced_List1= [node(0, 0), node(1, 1)]
list1 = ROBDD_Obj.Remove_Nodes(labelled_list1, Reduced_List1)
list1.reverse()
drawer2 = Drawer(list1)

'''
#############ROBDD##############

#from collections import deque
 

#Driver Program
#list1= BDD(['a','b','c','d'],['T','F','F','T','T','F','F','T','F','T','T','F','F','T','T','F'])
#list2= BDD(['a','b','c'],['F','F','F','F','F','F','F','T'])
#list1= BDD(['a','b','c'],['F','T','T','F','T','F','F','T'])
#list1= BDD(['a','b','c'],['F','T','T','F','F','T','T','F'])   
#list1= BDD(['a','b','c'],['F','F','F','F','F','F','F','T'])
#list1= BDD(['a','b','c'],['F','T','F','T','F','T','T','T']) 
list1= BDD(['a','b','c','d'],['F','F','F','T','F','F','F','F','F','F','F','F','T','F','F','T'])
#list1= BDD(['a','b','c','d'],['F','T','T','T','F','F','T','F','F','T','T','F','T','F','F','T']) 
#list2.reverse()
list1.reverse()
#print("########REVERSED_LIST########")
#for i in range(0,len(list)):
#    print(list[i].label)

#labelled_list2 = assign_labels(list2)
#labelled_list1 = assign_labels(list1)

print("########LABELLED###########")
print("\n")
for i in range(0, len(labelled_list1)):
    print(labelled_list1[i].data)
    print(labelled_list1[i].label)
print("\n")

Reduced_List1= [node(0, 0), node(1, 1)]
#Reduced_List2= [node(0, 0), node(1, 1)]
#print(Reduced_List1[0].data)
#print(Reduced_List1[0].label)
#print(Reduced_List1[1].data)
#print(Reduced_List1[1].label)

#list2= Remove_Nodes(labelled_list2, Reduced_List2)
list1= Remove_Nodes(labelled_list1, Reduced_List1)
#list2.reverse()
list1.reverse()
print("*************")
for i in range(0,len(list1)):
    print("\n")
    print("Node: ", i)
    #print(i)
    print("Data: ", list1[i].data)
    print("Label: ",list1[i].label)
    if(list1[i].left != None):
        print("Left: ",list1[i].left.data)
        print("Right: ",list1[i].right.data)
#print("*************")
#for i in range(0,len(list2)):
#    print("\n")
#    print("Node: ", i)
#    #print(i)
#    print("Data: ", list2[i].data)
#    print("Label: ",list2[i].label)
#    if(list2[i].left != None):
#        print("Left: ",list2[i].left.data)
#        print("Right: ",list2[i].right.data)
#print("****************")
#print(Equivalence_Checker(list1,list2))

###########################GRAPHICAL Drawer ########################



import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
import inspect
import pydot

from graphviz import Source

graph1 = pydot.Dot(graph_type='digraph')

label_value_left=0
label_value_right=0
# Add nodes to the graph
for  i in range(0,len(list1)):
    graph1.add_node(pydot.Node(list1[i].data))
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
        graph1.add_edge(pydot.Edge(list1[i].data, list1[i].left.data, color="blue", style="dashed"))
        if(type(list1[i].right.data)==type("y") and len(list1[i].right.data)==1):
            label_value_right=label_value_right + 1
            list1[i].right.data=list1[i].right.data+"% s" % label_value_right
            label_value_right=label_value_right+1
            #list1[i].right.data=list1[i].right.data+"% s" % label_value_right
            #label_value_right=label_value_right+1
        print(list1[i].right.data)
        graph1.add_edge(pydot.Edge(list1[i].data, list1[i].right.data))

# Generate the DOT string
dot_str1 = graph1.to_string()
#print(dot_str1)

src1 = Source(dot_str1)
src1.format = 'png'
src1.render('render_pdf_name4',view=True)

# Write the DOT string to a file
with open('graph1.dot', 'w') as f:
    f.write(dot_str1)
    
# Convert the DOT file to a PNG image
(graph1,) = pydot.graph_from_dot_file('graph1.dot')
graph1.write_png('graph1.png')


############################### Drawing BDD ##########################################################
list1_BDD = BDD(['a','b','c','d'],['F','F','F','T','F','F','F','F','F','F','F','F','T','F','F','T'])
#list1_BDD = BDD(['a','b','c','d'],['F','T','T','T','F','F','T','F','F','T','T','F','T','F','F','T']) 
graph1_BDD = pydot.Dot(graph_type='digraph')

"""
print("@$@$$@$@$@@$@$@$@$@$")
for i in range(0, len(list1_BDD)):
    print("\n")
    print("Node: ", i)
    print("Data: ", list1_BDD[i].data)
    if(list1_BDD[i].left != None):
        print("Left: ", list1_BDD[i].left.data)
        print("Right: ", list1_BDD[i].right.data)
"""

label_value_left=0
label_value_right=0

print("###############BDD HERE##############")
# Add nodes to the graph
for  i in range(0,len(list1_BDD)):
    graph1_BDD.add_node(pydot.Node(list1_BDD[i].data))
    print("node:",list1_BDD[i].data)
    if(list1_BDD[i].left != None):
        if(type(list1_BDD[i].left.data)==type("y") and len(list1_BDD[i].left.data)==1):
            label_value_left=label_value_left + 1
            list1_BDD[i].left.data=list1_BDD[i].left.data+ "% s" % label_value_left
            label_value_left_string= "% s" % label_value_left
            list1_BDD[i].left.data= list1_BDD[i].left.data.rstrip(label_value_left_string)

            label_value_left=label_value_left+1
            list1_BDD[i].left.data=list1_BDD[i].left.data+ "% s" % label_value_left

        print(list1_BDD[i].left.data)
        graph1_BDD.add_edge(pydot.Edge(list1_BDD[i].data, list1_BDD[i].left.data, color="blue", style="dashed"))
        if(type(list1_BDD[i].right.data)==type("y") and len(list1_BDD[i].right.data)==1):
            label_value_right=label_value_right + 1
            list1_BDD[i].right.data=list1_BDD[i].right.data+"% s" % label_value_right
            #label_value_right_string= "% s" % label_value_right
            #list1_BDD[i].right.data= list1_BDD[i].right.data.rstrip(label_value_right_string)

            #label_value_right=label_value_right+1
            #list1_BDD[i].right.data=list1_BDD[i].right.data+"% s" % label_value_right

        print(list1_BDD[i].right.data)
        graph1_BDD.add_edge(pydot.Edge(list1_BDD[i].data, list1_BDD[i].right.data))



# Generate the DOT string
dot_str1 = graph1_BDD.to_string()
#print(dot_str1)

src1 = Source(dot_str1)
src1.format = 'png'
src1.render('render_pdf_name4',view=True)

# Write the DOT string to a file
with open('graph1_BDD.dot', 'w') as f:
    f.write(dot_str1)
    
# Convert the DOT file to a PNG image
(graph1_BDD,) = pydot.graph_from_dot_file('graph1_BDD.dot')
graph1_BDD.write_png('graph1_BDD.png')


"""
# Add nodes to the graph
for  i in range(0,len(list1_BDD)):
    graph1_BDD.add_node(pydot.Node(list1_BDD[i].data))
    print("node:",list1_BDD[i].data)
    if(list1_BDD[i].left != None):
        if(type(list1_BDD[i].left.data)==type("y") and len(list1_BDD[i].left.data)==1):
            list1_BDD[i].left.data=list1_BDD[i].left.data+ "% s" % label_value_left
            label_value_left=label_value_left+1
            #list1_BDD[i].left.data=list1_BDD[i].left.data+ "% s" % label_value_left
            #label_value_left=label_value_left+1
        print(list1_BDD[i].left.data)
        graph1_BDD.add_edge(pydot.Edge(list1_BDD[i].data, list1_BDD[i].left.data, color="blue", style="dashed"))
        if(type(list1_BDD[i].right.data)==type("y") and len(list1_BDD[i].right.data)==1):
            list1_BDD[i].right.data=list1_BDD[i].right.data+"% s" % label_value_right
            label_value_right=label_value_right+1
        print(list1_BDD[i].right.data)
        graph1_BDD.add_edge(pydot.Edge(list1_BDD[i].data, list1_BDD[i].right.data))
"""
'''