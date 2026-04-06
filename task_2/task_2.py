"""
Напишите программу, анализирующую текстовый файл:
    - подсчитывающую количество строк, слов и символов;
    - определяющую частоту встречаемости каждого слова (без учёта
регистра);
    - выводящую 5 самых частых слов и их частоту;
    - создающей отчёт в отдельном файле analysis_report.txt;
    - обрабатывающей ошибки чтения файла и записи отчёта.
"""
import re
from pymorphy3 import MorphAnalyzer

path = input("Введите путь к файлу: ")
morph = MorphAnalyzer()

count_lines, count_words, count_symbols = 0, 0, 0
dict_words = {}
word_re = re.compile(r"[а-яА-ЯёЁ]+")
symbol_re = re.compile(r"[а-яА-ЯёЁa-zA-Z0-9]")

try:
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            count_lines += 1

            words = word_re.findall(line)
            count_words += len(words)

            symbols = symbol_re.findall(line)
            count_symbols += len(symbols)

            for word in words:
                wordL = word.lower()
                normal = morph.parse(wordL)[0].normal_form
                dict_words[normal] = dict_words.get(normal, 0) + 1

    # Запись отчёта
    with open("analysis_report.txt", "w", encoding="utf-8") as file:
        for word, count in dict_words.items():
            file.write(f"Слово {word} повторялось {count} раз\n")

        # Добавляем статистику
        file.write(f"\nСтатистика:\n")
        file.write(f"Количество строк: {count_lines}\n")
        file.write(f"Количество слов: {count_words}\n")
        file.write(f"Количество символов: {count_symbols}\n")

    # Топ 5 самых популярных слов
    popular_words = sorted(dict_words.items(), key=lambda x: -x[1])
    print("Топ 5 самых популярных слов:")
    for word, count in popular_words[:5]:
        print(f"{word}: {count} раз")

except FileNotFoundError:
    print("Файл не найден")
except Exception as e:
    print(f"Ошибка при обработке файла: {e}")