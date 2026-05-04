import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import random

API_KEY = 'YOUR_API_KEY'  # Замените на свой ключ

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.history_file = 'history.json'
        self.history = self.load_history()

        # Валюты (для примера)
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'RUB']

        # Виджеты
        self.create_widgets()
        self.update_history_table()

    def create_widgets(self):
        # Выбор валют
        tk.Label(self.root, text="Из:").grid(row=0, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(self.root, values=self.currencies)
        self.from_currency.set('USD')
        self.from_currency.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="В:").grid(row=0, column=2, padx=5, pady=5)
        self.to_currency = ttk.Combobox(self.root, values=self.currencies)
        self.to_currency.set('EUR')
        self.to_currency.grid(row=0, column=3, padx=5, pady=5)

        # Сумма
        tk.Label(self.root, text="Сумма:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        # Кнопка конвертации
        self.convert_btn = tk.Button(self.root, text="Конвертировать", command=self.convert)
        self.convert_btn.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky='ew')

        # Результат
        self.result_label = tk.Label(self.root, text="Результат: ")
        self.result_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

        # Таблица истории
        self.history_tree = ttk.Treeview(self.root, columns=('from', 'to', 'amount', 'result', 'rate'), show='headings')
        for col in ('from', 'to', 'amount', 'result', 'rate'):
            self.history_tree.heading(col, text=col.capitalize())
            self.history_tree.column(col, width=100)
        self.history_tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def update_history_table(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for entry in self.history:
            self.history_tree.insert('', 'end', values=(entry['from'], entry['to'], entry['amount'], entry['result'], entry['rate']))

    def validate_input(self):
        amount = self.amount_entry.get()
        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return False
        return True

    def get_rate(self, from_cur, to_cur):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}"
        try:
            response = requests.get(url)
            data = response.json()
            return data['conversion_rate']
        except Exception as e:
            messagebox.showerror("Ошибка API", f"Не удалось получить курс: {e}")
            return None

    def convert(self):
        if not self.validate_input():
            return

        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()
        amount = float(self.amount_entry.get())

        rate = self.get_rate(from_cur, to_cur)
        if rate is None:
            return

        result = round(amount * rate, 2)
        self.result_label.config(text=f"Результат: {result} {to_cur}")

        # Сохранение в историю
        entry = {
            "from": from_cur,
            "to": to_cur,
            "amount": amount,
            "result": result,
            "rate": rate,
            "timestamp": random.randint(1000000000, 9999999999)  # Для уникальности
        }
        self.history.append(entry)
        self.save_history()
        self.update_history_table()
