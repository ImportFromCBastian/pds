def divide(a:int|float ,b:int|float )->float:
  """This function devide two numbers"""
  
  try:
    return a/b
  except ZeroDivisionError:
    return "Can't devide by zero"
  
