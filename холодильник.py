import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

goods = {}

def add(items, title, amount, expiration_date=None):
    
    #Если срок годности не пустой, преобразовываем дату в объект datetime.date
    if expiration_date is not None:
        expiration_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()

    #Создаем запись о новой партии продукта
    product_entry = {
        'amount': amount,
        'expiration_date': expiration_date
    }

    #Проверяем есть ли продукт, добавляем партию
    if title in items:
        items[title].append(product_entry)
    #Добавляем новый
    else:
        items[title] = [product_entry]

#Проверяем работу функции add
add(goods, 'Яйца', Decimal('10'), '2023-9-30')
add(goods, 'Яйца', Decimal('3'), '2023-10-15')
add(goods, 'Картошка', Decimal('10'), '2025-4-3')
add(goods, 'Вода', Decimal('2.5'))
print(goods)

def add_by_note(items, note):
    parts = str.split(note, ' ')
    print(parts)
    #Если в конце дата
    if len(str.split(parts[-1], '-')) == 3:
        expiration_date = parts[-1]
        good_amount = Decimal(parts[-2])
        title = str.join(' ', parts[0:-2])
    # Проверяем работу функции 
    print(expiration_date, good_amount, title)
    #Вызываем функцию add
    add(goods, title, good_amount, expiration_date)

#Проверяем работу функции add_by_note
add_by_note(goods, 'Яйца Фабрики №1 4 2023-07-15')

print(goods)

def find(items, needle):
    #Приводим запрос к нижнему регистру
    needle = needle.lower()
    #Создаем список для вывода результата
    result = []
    #Проверяем все значения в списке. Добавляем результат в список для вывода
    for product in items:
        if needle in product.lower():
            result.append(product)
    #Возвращаем список с результатом поиска
    return result

#Проверяем работу функции find
print(find(goods, 'яйц'))

def get_amount(items, needle):
    # Получаем список продуктов, которые содержат искомую строку
    found_products = find(items, needle)
    
    # Начинаем с нуля
    total_amount = Decimal('0')
    
    # Перебираем все найденные продукты
    for product_name in found_products:
        # Перебираем все партии этого продукта
        for batch in items[product_name]:
            # Добавляем количество партии к общему количеству
            total_amount += batch['amount']

    return total_amount

#Проверяем функцию
print(get_amount(goods, 'яйц'))


def get_expired(items, in_advance_days=0):
    # Получаем текущую дату
    current_date = datetime.date.today()
    
    # Список для хранения просроченных продуктов
    expired_products = []

    # Перебираем все продукты в холодильнике
    for product_name, batches in items.items():
        total_amount = Decimal('0')
        
        # Перебираем все партии данного продукта
        for batch in batches:
            expiration_date = batch['expiration_date']
            
            # Если дата истечения срока годности не задана (None), пропускаем
            if expiration_date is None:
                continue
            
            # Вычисляем разницу между датой истечения срока и текущей датой
            days_left = (expiration_date - current_date).days
            
            # Если срок годности истек или истечет через указанное количество дней
            if days_left <= in_advance_days:
                total_amount += batch['amount']
        
        # Если для продукта найдено количество, добавляем его в результат
        if total_amount > 0:
            expired_products.append((product_name, total_amount))

    return expired_products


print(get_expired(goods, 1))