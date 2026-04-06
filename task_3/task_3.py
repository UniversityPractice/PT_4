"""
Создайте конвертер данных между форматами JSON, CSV, TXT (табличный):
    - программа должна загружать данные из одного
    - преобразовывать в другой, сохранять результат;
    - поддержите преобразования: JSON ↔ CSV, JSON ↔ TXT, CSV ↔ TXT;
    - обеспечьте корректную обработку структур данных при конвертации
(например, списки в JSON → несколько строк в CSV);
    - добавьте валидацию данных для каждого формата
(некорректный JSON, несовпадающие колонки в CSV и т. д.);
    - предоставьте пользователю выбор форматов и путей к файлам;
    - логируйте операции конвертации в файл converter_log.txt.
"""

import csv
import json
from pathlib import Path
from datetime import datetime


LOG_FILE = "converter_log.txt"


# ------------------ ЛОГИРОВАНИЕ ------------------
def log(message: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")


# ------------------ ВАЛИДАЦИЯ ------------------
def validate_json(path: Path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("❌ Некорректный JSON")


def validate_csv(path: Path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            raise ValueError("❌ CSV пустой")

        headers = reader.fieldnames
        for row in rows:
            if set(row.keys()) != set(headers):
                raise ValueError("❌ Несовпадающие колонки в CSV")

        return rows


def validate_txt(path: Path):
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines:
            raise ValueError("❌ TXT пустой")
        return lines


# ------------------ КОНВЕРТЕРЫ ------------------
def json_to_csv(data, output_path):
    if isinstance(data, list):
        keys = set()
        for item in data:
            keys.update(item.keys())

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(keys))
            writer.writeheader()
            writer.writerows(data)

    elif isinstance(data, dict):
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for k, v in data.items():
                writer.writerow([k, v])

    log("JSON → CSV выполнен")


def json_to_txt(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        if isinstance(data, list):
            for item in data:
                f.write(str(item) + "\n")
        else:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))

    print("JSON → TXT выполнен")


def csv_to_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("CSV → JSON выполнен")


def csv_to_txt(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for row in data:
            f.write(str(row) + "\n")

    print("CSV → TXT выполнен")


def txt_to_csv(lines, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for line in lines:
            writer.writerow(line.split())

    print("TXT → CSV выполнен")


def txt_to_json(lines, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lines, f, indent=2, ensure_ascii=False)

    print("TXT → JSON выполнен")


# ------------------ ОСНОВНАЯ ЛОГИКА ------------------
def main():
    path = input("Введите путь к файлу: ").strip()
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError("❌ Файл не найден")

    ext = file_path.suffix.lower()

    output_format = input("В какой формат конвертировать (json/csv/txt): ").strip().lower()
    output_path = input("Введите путь для сохранения результата: ").strip()

    try:
        if ext == ".json":
            data = validate_json(file_path)

            if output_format == "csv":
                json_to_csv(data, output_path)
            elif output_format == "txt":
                json_to_txt(data, output_path)

        elif ext == ".csv":
            data = validate_csv(file_path)

            if output_format == "json":
                csv_to_json(data, output_path)
            elif output_format == "txt":
                csv_to_txt(data, output_path)

        elif ext == ".txt":
            lines = validate_txt(file_path)

            if output_format == "csv":
                txt_to_csv(lines, output_path)
            elif output_format == "json":
                txt_to_json(lines, output_path)

        else:
            raise ValueError("❌ Поддерживаются только json/csv/txt")

        print("✅ Конвертация завершена")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()