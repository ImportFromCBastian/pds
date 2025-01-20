from operaciones import division, multiplicacion, resta, suma
def calculate(a,b,operation):
    if operation == "-":
        return resta.subtract(a,b)
    elif operation == "*":
        return multiplicacion.multiplicar(a,b)
    elif operation == "/":
        return division.divide(a,b)
    elif operation == "+":
        return suma.add(a,b) 
    else:
        raise ValueError("Esa operación no está soportada!")