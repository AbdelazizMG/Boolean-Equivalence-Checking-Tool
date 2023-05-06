from node import node
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