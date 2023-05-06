class Equivalence_Checker:
    def __init__(self):
        pass

    def map_var(self,vars1,vars2):
        counter = 0
        vars_1 = []
        vars_2 = []
        for i in range(0,len(vars1)):
            temp = "x"+str(counter)
            vars_1.append(temp)
            counter = counter + 1
        counter = 0
        for i in range(0,len(vars2)):
            temp = "x"+str(counter)
            vars_2.append(temp)
            counter = counter + 1
        return vars_1,vars_2  
  
    def start(self,List1,List2,vars1,vars2):
        vars_1 , vars_2 = self.map_var(vars1,vars2)
        for i in range(0,len(List1)):
            if (List1[i].data != 0) and (List1[i].data != 1):
                List1[i].data = vars_1[vars1.index(List1[i].data)]
        for i in range(0,len(List2)):
            if (List2[i].data != 0) and (List2[i].data != 1):
                List2[i].data = vars_2[vars2.index(List2[i].data)]       
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
        




      