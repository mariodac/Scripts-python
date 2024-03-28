from datetime import datetime, timedelta

data_reference = datetime.today()  

print("Calculadora de Datas")
print("1. Adicionar dias")
print("2. Subtrair dias")
print("3. Adicionar semanas")
print("4. Subtrair semanas")
print("5. Adicionar meses")
print("6. Subtrair meses")
print("7. Adicionar anos")
print("8. Subtrair anos")

option = int(input("Escolha uma opção (1-8): "))

if option == 1:
    days = int(input("Quantos dias adicionar: "))
    complement = f" + {days} dias"
    new_date = data_reference + timedelta(days=days)
elif option == 2:
    days = int(input("Quantos dias subtrair: "))
    new_date = data_reference - timedelta(days=days)
    complement = f" - {days} dias"
elif option == 3:
    weeks = int(input("Quantas semanas adicionar: "))
    new_date = data_reference + timedelta(weeks=weeks)
    complement = f" + {weeks} semanas"
elif option == 4:
    weeks = int(input("Quantas semanas subtrair: "))
    new_date = data_reference - timedelta(weeks=weeks)
    complement = f" - {weeks} semanas"
elif option == 5:
    months = int(input("Quantos meses adicionar: "))
    new_date = data_reference + timedelta(days=30 * months)
    complement = f" + {months} meses"
elif option == 6:
    months = int(input("Quantos meses subtrair: "))
    new_date = data_reference - timedelta(days=30 * months)
    complement = f" - {months} meses"
elif option == 7:
    years = int(input("Quantos anos adicionar: "))
    new_date = data_reference.replace(year=data_reference.year + years)
    complement = f" + {years} anos"
elif option == 8:
    years = int(input("Quantos anos subtrair: "))
    new_date = data_reference.replace(year=data_reference.year - years)
    complement = f" - {years} anos"
else:
    print("Opção inválida")


print(f"{data_reference.strftime('%d/%m/%Y')}{complement} = {new_date.strftime('%d/%m/%Y')}")