
import re

class Parser:
   def __add_spaces(self,string):
      # Define a regular expression to match logical operators
      op_regex = r"([^\s])(~?[&|^]){1,2}(?=[^\s&|^]){1,2}|(?<=[^\s&|^]){1,2}(~?[&|^]){1,2}([^\s])"
      # Use re.sub() function to add spaces before and after logical operators
      result = re.sub(op_regex, r"\1 \2\3 \4", string)
      return result
   
   def __vars_list(self,string):
      open_bracket = 0
      close_bracket = 0
      vars = []
      for i in string:
         if i == '(':
            open_bracket = open_bracket + 1
         elif i == ')':
            close_bracket = close_bracket + 1
      if open_bracket == close_bracket:
         flag_brackets = 1
      else:
         flag_brackets = 0
      if flag_brackets:
         x = re.sub(r"[()~&|^!]",r" ",string)
         y = re.split(r"[\s]{1,}",x)
         z = [i for i in y if i != '']
         vars.append(z[0])
         for i in range(len(z)-1):
            if z[i+1] in vars:
               continue
            else:
               vars.append(z[i+1])
         return vars,flag_brackets
      else:
         return vars,flag_brackets
   
   def __vars_names_checks(self,vars):
      initial_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
      numbers = ['0','1','2','3','4','5','6','7','8','9']
      correct_name = 0
      error_list = []
      for v in vars:
         temp = v.lower()
         if temp[0] in initial_chars:
            correct_name = 1
            for i in range(1,len(temp)): 
               if (temp[i] in initial_chars) or (temp[i] in numbers):
                  correct_name = 1
               else:
                  correct_name = 0
                  break
         else:
            correct_name = 0
         if not(correct_name):
            error_list.append(v)
      if error_list:
         correct_name = 0
      else: 
         correct_name = 1
      return correct_name,error_list
   
   def __TT_Substitute(self,string,TT,vars_list):
      string_sub_table = []
      col = 2**len(vars_list)
      for j in range(col):
         temp = string
         for i in range(len(vars_list)):
            temp = re.sub(vars_list[i],TT[i][j],temp)
         string_sub_table.append(temp)
      return string_sub_table
   
   def __TT_comb(self,vars_list):
      coloumns = len(vars_list)
      rows = 2**coloumns
      TT = []
      ones_zeros_no = 1
      for i in range(coloumns):
            col = []
            for j in range(int(rows/(2*ones_zeros_no))):
               for k in range(ones_zeros_no):
                  col.append('F')
               for n in range(ones_zeros_no):
                  col.append('T')
            TT.append(col)
            ones_zeros_no = ones_zeros_no*2
      return TT

   def __solve(self,s):
      stack = []
      op = {
         "|": lambda x, y: x or y,
         "&": lambda x, y: x and y,
         "^": lambda x, y: x ^ y,
         "~&": lambda x, y: not(x and y),
         "~|": lambda x, y: not(x or y),
         "~^": lambda x, y: not(x ^ y),
         "||": lambda x, y: x or y,
         "&&": lambda x, y: x and y,
      }
      s = self.__add_spaces(s)
      for v in s.split():
         if v[0] == "(":
            stack.append(v[v.count("(") :] == "T")
         elif v.count(")") > 0:
            ct = v.count(")")
            stack.append(v[:-ct] == "T")
            for _ in range(ct):
               right = stack.pop()
               o = stack.pop()
               left = stack.pop()
               stack.append(o(left, right))
         elif v in ["T", "F"]:
            stack.append(v == "T")
         else:
            stack.append(op[v])
      if len(stack) > 1:
         for i in range(0, len(stack) - 1, 2):
            stack[i + 2] = stack[i + 1](stack[i], stack[i + 2])
         return stack[-1]
      return stack[0]
   
   def __Boolean_Function_Solve(self,string):
      string = re.sub(r"\(\s{0,}[T]\s{0,}\)",r"T",string)
      string = re.sub(r"\(\s{0,}[F]\s{0,}\)",r"F",string)
      string = re.sub(r'[~!]\s{0,}F',r'T',string)
      string = re.sub(r'[!~]\s{0,}T',r'F',string)
      string = re.sub(r"[!~]\s{0,}\(",r"T~&(",string)
      string = re.sub(r"\(\s{0,}F",r"(F",string)
      string = re.sub(r"\(\s{0,}T",r"(T",string)
      string = re.sub(r"T\s{0,}\)",r"T)",string)
      string = re.sub(r"F\s{0,}\)",r"F)",string)
      string = string.replace(" ", "")
      print(string)
      return self.__solve(string)

   def __Check_bool_func(self,vars,string):
      True_vector = 'T'
      temp = string
      for i in range(0,len(vars)):
         temp = re.sub(vars[i],True_vector,temp)
      self.__Boolean_Function_Solve(temp)
   
   def GUI_check(self,string):
      vars,flag_barckets = self.__vars_list(string)
      Correct_flag = 0
      error_list_names = []
      expr_flag = 0
      if flag_barckets:
         Correct_flag,error_list_names = self.__vars_names_checks(vars)
         if Correct_flag:
            try:
               expr_flag = 1
               self.__Check_bool_func(vars,string)
            except Exception as e:
               expr_flag = 0
               print(str(e))
         else:
            expr_flag = 0
         return flag_barckets,Correct_flag,expr_flag,error_list_names
      else:
         return flag_barckets,Correct_flag,expr_flag,error_list_names



if __name__ == "__main__":
   ob = Parser()
   s = "((a~&b|c^(a&&c))||(b&a)~^c~|b)"
   s = "        )a(                &b|   c"
   #s = "           T          &T|T"
   #result = ob.Boolean_Function_Solve(s)
   #vars = ob.vars_no(s)
   #vars = ob.vars_list(s)
   flag_barckets,Correct_flag,expr_flag,error_list_names = ob.GUI_check(s)
   print(flag_barckets)
   
   #print(vars)
   print(Correct_flag)
   print(expr_flag)
   print(error_list_names)
   #TT = ob.TT_comb(vars)
   #TT = ['T','T','T']
   #vars = ['a','b','c']
   #Strings = ob.Substitute(s,TT,vars)
   #output = []
   #for i in Strings:
   #   bol = ob.add_spaces(i)
   #   value = ob.solve(bol)
   #   if value:
   #      output.append('T')
   #   else:
   #      output.append('F')
   #TT.append(output)
   #print(TT)

