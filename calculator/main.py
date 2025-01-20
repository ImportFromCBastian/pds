import calculator
def main():
    a = float(input("Ingresa el primer número: "))
    b = float(input("Ingresa el segundo número: "))
    operation = input("Ingresa la operación(+,-,/,*): ")
    result = calculator.calculate(a,b,operation)
    print(f"El resultado es: {result}")

if __name__ == "__main__":
    main()