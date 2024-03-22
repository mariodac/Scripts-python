from datetime import date, datetime
from datetime import timedelta

def get_days_in_month(month, year):
    # Retorna o número de dias em um determinado mês e ano
    if month == 2:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): 
            return 29  # Ano Bisexto
        else:
            return 28
    elif month in [4, 6, 9, 11]:  # Abril, Junho, Setembro, Novembro 
        return 30
    else:
        return 31

def age_calculator(birth_date):
    current_date = date.today()
    birth_year = birth_date.year
    age = current_date.year - birth_year
    # verifica se mês atual é menor que mês do nascimento OU 
    # (mês atual é igual a mês do nascimento E dia atual é menor que dia do nascimento)
    # significa que data atual ainda não ultrapassou a data de nascimento, sendo assim diminui 1 da idade
    if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
        age -= 1
    return age
    
def age_calculator_days_months_years(birth_date:date):
    current_date = date.today()
    years =  current_date.year - birth_date.year
    months = current_date.month - birth_date.month
    days = current_date.day - birth_date.day
    # se o dia for negativo, significa que o dia atual não atingiu o dia de nascimento
    if days < 0:
        months -= 1
        days += get_days_in_month(birth_date.month, birth_date.year)
    # se o mês for negativo, significa que o mês atual não atingiu o mês de nascimento
    if months < 0:
        years -= 1
        months += 12
    return years, months, days
    

print('ATENÇÃO\nUtilize o formato dia/mês/ano (30/12/2020)')
birth_date = input('Digite sua data de nascimento => ')
date_object_birth_date = datetime.strptime(birth_date, '%d/%m/%Y').date()
current_date = date.today()
if date_object_birth_date <= current_date:
    # age = age_calculator(date_object_birth_date)
    # print(f'Sua idade é: {age} anos')
    year, month, day = age_calculator_days_months_years(date_object_birth_date)
    birthday = date(current_date.year, 8, 5)
    left_days = birthday - current_date
    print(f'Você possui {year} anos, {month} meses e {day} dias')
    if left_days.days > 30:
        left_months = left_days.days // 30.417
        left_day = round(left_days.days%30.417)
        print(f'Faltam {left_months} meses e {left_day} dias para seu aniversário')
    else:
        print(f'Faltam {left_days.days} dias para seu aniversário')
else:
    print('Data inválida')
