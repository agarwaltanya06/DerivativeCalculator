#To get the required output, enter the function without spaces and with brackets in the input
#For example, (x+5), or (2/x), or (6*x), or (x*(2^x)), etc

class expr:
    
#assert: the class expr has an attribute 'expr'. This 'expr' attribute is represented in memory as a tree. 
#Each node of that tree is an object of the subclass 'Node'

  def __init__(self,S,Nd = None):
    if (Nd):
      self.expr = Nd
    else:
      (e,n) = self.parse(S)
      self.expr = e

  class Node:
    
  #assert: an object of the subclass 'Node' has an attribute 'data' (which stores an operator/constant/variable value)
  #it also has attributes 'left' and 'right', which further store other data or other objects of the 'Node' subclass
    
    def __init__(self,d):
      self.left = None
      self.right = None
      self.data = d
    
    def toString(self): 
      
    #assert: to convert the node to a string which has the 'left', 'data' and 'right' attributes in order and enclosed by brackets  
      
      if (self.left and self.right):
        left = self.left.toString()
        right = self.right.toString()
        opr = self.data
        return "(" + left + " " + opr + " " + right + ")"
        
      elif(self.right):
      #assert: modification made to print a node that has only a right attribute (eg. 0.0 - 2.0, which doesnt require the 'left' attribute to be printed)
      #This will hence work when further derivatives of subtracted terms need not be taken, and hence will give the correct result when used as a subsidiary while returning division function's derivative
        
        opr = self.data
        right= self.right.toString()
        return "((" + opr + ")" + right + ")" 
      else:
        return self.data

  def prettyprint(self):
    
    #assert: to print the string formed by converting the 'expr' attribute (i.e. a base node of the tree) to a string
    #which has the 'left', 'data' and 'right' attributes in order and enclosed by brackets
    
    s = self.expr.toString()
    print(s)
    

  def parse(self,S):
    
  #assert: to convert a string to the nodes of the tree which represents the 'expr' attribute in memory
    
    l = len(S)
    if (S[0] == "("):
    #assert: this means that there is an expression enclosed by brackets that must be parsed
      (left,n) =  self.parse(S[1:l-2])  
      opr = S[n+1]                        
      (right,m) = self.parse(S[n+2:l-1]) 
      expr = self.Node(opr)
      expr.left = left
      expr.right = right
      return (expr,n+m+3)
    
    elif S[0].isdigit():
    #assert: this means that a constant value part of the string has been encountered, which will be the 'data' of some leaf node of the tree
      i = 0
      while ((i < l) and (S[i].isdigit() or (S[i] == "."))):
        i = i+1
      num = S[0:i]
      expr = self.Node(num)
      return (expr,i)
    
    elif S[0].isalpha():
    #assert: this means that a constant value part of the string has been encountered, which will be the 'data' of some leaf node of the tree   
      i = 0
      while ((i < l) and S[i].isalpha()):
        i = i+1
      var = S[0:i]
      expr = self.Node(var)
      return (expr,i)
    
    else:
      return Exception("Invalid input")

  def constant(self):
  #assert: to determine if the 'data' attribute of the node under consideration (of the tree representing the expression in memory) stores a constant value
    if self.expr.data[0].isdigit():
      return True
    else:
      return False

  def variable(self):
  #assert: to determine if the 'data' attribute of the node under consideration stores a variable value    
    if self.expr.data[0].isalpha():
      return True
    else:
      return False

  def samevariable(self,x):
  #assert: to determine if the 'data' attribute of the node under consideration stores the variable x (with respect to which derivative is being taken)   
    if (self.expr.data == x):
      return True
    else:
      return False
  
  def sum(self):
  #assert: to determine if the node under consideration represents a SUMMED expression (having 1 operator "+" as 'data' and two addends as 'left' and 'right')
    if (self.expr.data == '+'):
      return True
    else:
      return False
  
  def prod(self):
  #assert: to determine if the node under consideration represents a MULTIPLIED expression (having 1 operator "*" as 'data' and two multiplicands as 'left' and 'right' )
      if(self.expr.data=='*'):
          return True
      else:
          return False
          
  def division(self):
  #assert: to determine if the node under consideration represents a DIVIDED expression (having 1 operator "/" as 'data' and a numerator and denominator as 'left' and 'right' respectively) 
      if(self.expr.data=='/'):
          return True
      else:
          return False
  
  def exponent(self):
  #assert: to determine if the node under consideration represents an EXPONENTIATED expression (having 1 operator "^" as 'data' and a base and exponent as 'left' and 'right' respectively)      
      if(self.expr.data=='^'):
          return True
      else:
          return False
  
  def termleft(self):
  #assert: to return the 'left' attribute of the node under consideration (of the tree representing the expression)  
    left = self.expr.left
    return expr("",left)

  def termright(self):
  #assert: to return the 'right' attribute of the node under consideration (of the tree representing the expression) 
    right = self.expr.right
    return expr("",right)

  def makesum(self,e1,e2):
      
  #assert: this creates a new node of the tree for representing the ADDITION of the input e1 and e2 nodes, as (e1+e2)
  #each node here is an object of class expr - whose attribute 'expr' is an object of the subclass Node    
    
    e = self.Node("+")  
    e.left = e1.expr
    e.right = e2.expr
    
    #assert: to REMOVE REDUNDANT ZEROES on adding two expressions 
    if(e.left.data=="0.0"):
        e.left=None
        e=e.right
    elif(e.right.data=="0.0"):
        e.right=None
        e=e.left
    return expr("",e)

  def makeprod(self,e1,e2):
      
  #assert: this creates a new node of the tree for representing the MULTIPLICATION of the input e1 and e2 nodes, as (e1*e2)
  #each node here is an object of class expr - whose attribute 'expr' is an object of the subclass Node    
      
      e=self.Node("*")
      e.left=e1.expr
      e.right=e2.expr
      
      #assert: to REMOVE REDUNDANT ZEROES on multiplying two expressions
      if(e.left.data=="0.0" or e.right.data=="0.0"):
          e.right=None
          e.left=None
          e=self.Node("0.0")
          
      #to REMOVE REDUNDANT ONES on multiplying two expressions
      elif(e.left.data=="1.0" or e.left.data=="1"):
          e.left=None
          e=e.right
      
      elif(e.right.data=="1.0" or e.right.data=="1"):
          e.right=None
          e=e.left
      
      return expr("",e)
  
  def makediv(self,e1,e2):
  
  #assert: this creates a new node of the tree for representing the DIVISION of the input e1 and e2 nodes, as (e1/e2)
  #each node here is an object of class expr - whose attribute 'expr' is an object of the subclass Node       
      
      e=self.Node("/")
      e.left=e1.expr
      e.right=e2.expr
      return expr("",e)
  
  def makediff(self,e1,e2): 
  
  #assert: subsidiary function for representing the difference of the input e1 and e2 nodes
  #Used to represent the numerator of the derivative of an (f(x)/g(x)) type function 
      
      e=self.Node("-")
      e.left=e1.expr
      e.right=e2.expr
      
      #assert: to REMOVE REDUNDANT ZEROES on subtracting two expressions (eg. 0.0 - 2.0)
      #Since our nodes do not have unary operators, this will work only in a function which does not require derivative of subtracted terms to be defined, else this redundant zero could not have been removed in this manner
      #I have defined this only for the purpose of the COL assignment, to remove the redundant zero here
      #This will hence work when further derivatives of subtracted terms need not be taken, and hence will give the correct result when used as a subsidiary while returning division function's derivative
      
      if(e.left.data=="0.0"):
          e.left=None
      elif(e.right.data=="0.0"):
          e.right=None
          e=e.left      
      return expr("",e)
  
  def makeexpo(self,e1,e2):
      
  #assert: this creates a new node of the tree for representing EXPONENTIATION, (base e1 node and exponent e2 node), as (e1^e2)
  #each node here is an object of class expr - whose attribute 'expr' is an object of the subclass Node      
      
      e=self.Node("^")
      e.left=e1.expr
      e.right=e2.expr
      
      #assert: REDUNDANT ZEROES for 0^g(x) type functions have already been removed since that case is separately defined in the deriv function
      
      #assert: Now removing REDUNDANT POWERS: replacing f(x)^1 or f(x)^1.0 with f(x) and f(x)^0 or f(x)^0.0 with 1.0
      
      if e.right.data==("1") or e.right.data==("1.0"):
          return e1
      elif e.right.data==("0") or e.right.data==("0.0"):
          e=self.Node("1.0")
      
      
      return expr("",e)
      
  def reciprocal(self):
      
  #assert: to return reciprocal (of the expression represented by the 'expr' attribute, of 'self' object of class 'expr')
  
  #the exception case for numerator zero has not been defined because, for the purpose of the COL assignment, considering the type of
  #input functions that are allowed, reciprocal of zero will never be taken, especially since the 0^g(x) case has already been defined separately in deriv function
  
      e=self.Node("/")
      leftpart=expr("1")
      e.left=leftpart.expr
      e.right=self.expr
      return expr("",e)
      
  def logval(self):
  #assert: to represent the logarithm or log() (of the expression represented by the 'expr' attribute, of 'self' object of class 'expr')
      k="(log(" + self.expr.toString() + "))"
      e=expr(k)
      return e
  
  def deriv(self,x):
      
  #assert: this function calculates and returns the derivative (of the expression represented by 'expr' attribute, of 'self' object of class 'expr')
  #the derivative is calculated with respect to the variable 'x' here
  
    if self.constant():
        #assert: returns the derivative of a constant function to be zero
        return expr("0.0")
      
    elif self.variable():
        #assert: returns the derivative of a variable value with respect to the variable 'x' (where, here, we are taking derivative w.r.t  variable 'x')
        if self.samevariable(x):
          return expr("1.0")
        else:
            return expr("0.0")
        
    elif self.sum():
    
    #assert: returns the derivative of an expression (represented by 'expr' attribute of object self of expr class), of the form (f(x)+g(x))
    #where, f and g are functions of x
      
      e1 = self.termleft()   #f(x)
      e2 = self.termright()  #g(x)
      return self.makesum(e1.deriv(x),e2.deriv(x))
      
    elif self.prod():
    
    #assert: returns the derivative of an expression (represented by 'expr' attribute of object self of expr class), of the form (f(x)*g(x))
    #where, f and g are functions of x
        
        e1=self.termleft()   #f(x)
        e2=self.termright()  #g(x)
        return self.makesum( self.makeprod( e1.deriv(x),e2 ), self.makeprod( e1,e2.deriv(x)) )
    
    elif self.division(): 
    
    #assert: returns the derivative of an expression (represented by 'expr' attribute of object self of expr class), of the form (f(x)/g(x))
    #where, f and g are functions of x
        
        e1=self.termleft()  #f(x)
        e2=self.termright() #g(x)
        enum=self.makediff(self.makeprod(e2,e1.deriv(x)),self.makeprod(e1,e2.deriv(x)))
        eden=self.makeexpo(e2,expr("2"))
        return self.makediv(enum, eden)
        
    elif self.exponent():
        
    #assert: returns the derivative of an expression (represented by 'expr' attribute of object self of expr class), of the form (f(x)^g(x))
    #where, f and g are functions of x        
        
        e=self.expr.right
        
        if e.data.isdigit():
            
            #assert: here the exponent is a constant expression
            
            e1=self.termleft()  #the base term, f=f(x)
            e2=self.termright()  #the constant exponent, g=constant function
            k=int(e.data)-1
            e3=self.makeexpo(e1,expr(str(k)))
            e4=self.makeprod(expr("",e),e3)
            e5=self.makeprod(e4,e1.deriv(x))
            return e5
            
        else:
            
            #here BOTH THE BASE AND THE EXPONENT CAN BE FUNCTIONS OF X, i.e. the expression is of the form (f^g), where f=f(x), g=g(x)
            #So, we finally obtain: ( (f^g) * (g * 1/f * f' + g' * ln(f)) ), [where f^g = y = original expression]
            
            e1=self.termleft()  #the base term, f=f(x)
            e2=self.termright() #the exponent, g=g(x)
            
            if e1.expr.data==("e"):
            #if it is e^g(x) then the derivative is [e^g(x)] * g'(x)
            #I have defined this separately since the user may put "e" as the input base value instead of typing out the constant 2.71..
                return self.makeprod(self,e2.deriv(x))
            
            elif e1.expr.data==("0.0") or e1.expr.data==("0"):
                return expr("0.0")
                
            else:
                leftval1 = self.makeprod(e1.reciprocal(),e1.deriv(x))
                leftval=self.makeprod(e2,leftval1)
            
                rightval=self.makeprod(e2.deriv(x),e1.logval())
            
                return self.makeprod( self, self.makesum(leftval,rightval))
      
    
    else: 
      raise Exception("DontKnowWhatToDo!")


a = input("Enter an expression: ")

e=expr(a)

f=e.deriv('x')

print("The derivative of: ", end='')
e.prettyprint()
print(" is: ")
f.prettyprint()
