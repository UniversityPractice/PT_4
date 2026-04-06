"""
Создайте файл sales.csv со следующими данными:
    Товар, Количество,Цена_за_единицу
    Яблоки,10,50
    Бананы,5,80
    Апельсины,8,60
    Груши,12,45
Напишите программу, которая:
    - читает данные из файла;
    -вычисляет общую стоимость для каждого товара (Количество ×
    Цена_за_единицу);
    - подсчитывает общую выручку по всем товарам;
    - выводит результаты в табличном формате;
    - обрабатывает ошибки чтения файла и некорректных числовых данных.
"""
import csv

common_sum = 0

print("=" * 45)
print(f"{'Товар':<15} {'Общая сумма':<15}")
print("-" * 45)

try:
    with open("sales.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок

        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue

            product = row[0].strip()
            quantity = int(row[1].strip())
            price = int(row[2].strip())

            sum_products = quantity * price
            print(f"{product:<15} {sum_products:<15}")
            common_sum += sum_products
except FileNotFoundError:
    print("File not found")
except ValueError:
    print("Value Error")

print("-" * 45)
print(f"{'ИТОГО:':<15} {common_sum:<15}")
print("=" * 45)
