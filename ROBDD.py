
class ROBDD:
    def __init__(self,num_variables):
        self.Parent_Add = None

        self.num_variables = num_variables

    def assign_labels(self,list):                                                       
        for i in range(pow(2, self.num_variables), len(list)):
            if(list[i].left.label == list[i].right.label):
                list[i].label = list[i].left.label

        temp = list[pow(2, self.num_variables): ]
        index=0
        for i in range(self.num_variables-1, -1, -1):   #number of variables= number of levels
            for j in range(0, pow(2, i)):
                for k in range(0, pow(2, i)):
                    if(temp[index+j] != temp[index+k]) and (temp[index+j].left.label==temp[index+k].left.label) and (temp[index+j].right.label==temp[index+k].right.label):
                        temp[index+k].label=temp[index+j].label
            index=index+pow(2, i)
        
        for i in range(pow(2, self.num_variables), len(list)):
            if(list[i].left.label == list[i].right.label):
                list[i].label = list[i].left.label

        list[pow(2, self.num_variables): ]=temp
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
        init = pow(2, self.num_variables)
        #print("****** AFTER *******")
        for i in range(self.num_variables-1, -1, -1):   #number of variables= number of levels
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
        init = pow(2, self.num_variables)
        for i in range(init,len(list)):
            if (list[i].label != list[i].label):
                list[i] = list[i]
        #list[pow(2, num_variables): ]=temp
        for i in range(0, len(list)):
            if(list[i].label!=-1):
                Reduced_List.append(list[i])
        return Reduced_List