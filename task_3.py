"""
Создайте конвертер данных между форматами JSON, CSV, TXT (табличный):
    - программа должна загружать данные из одного
    - преобразовывать в другой, сохранять результат;
    - поддержите преобразования: JSON ↔ CSV, JSON ↔ TXT, CSV ↔ TXT;
    - обеспечьте корректную обработку структур данных при конвертации
(например, списки в JSON → несколько строк в CSV);
    - добавьте валидацию данных для каждого формата (некорректный JSON,
несовпадающие колонки в CSV и т. д.);
    - предоставьте пользователю выбор форматов и путей к файлам;
    - логируйте операции конвертации в файл converter_log.txt.
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