import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.data_file = 'books.json'
        self.books = self.load_books()
        self.create_widgets()
        self.update_book_list()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(self.root)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        # Фильтрация
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц >").grid(row=6, column=0, padx=5, pady=5)
        self.filter_pages = tk.Entry(self.root)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5)

        self.filter_btn = tk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky='ew')

        # Таблица книг
        self.book_tree = ttk.Treeview(self.root, columns=('title', 'author', 'genre', 'pages'), show='headings')
        for col in ('title', 'author', 'genre', 'pages'):
            self.book_tree.heading(col, text={'title': 'Название', 'author': 'Автор', 'genre': 'Жанр', 'pages': 'Страниц'}[col])
            self.book_tree.column(col, width=120)
        self.book_tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def load_books(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.books, f)

    def update_book_list(self):
        for i in self.book_tree.get_children():
            self.book_tree.delete(i)
        for book in self.books:
            self.book_tree.insert('', 'end', values=(book['title'], book['author'], book['genre'], book['pages']))

    def validate_input(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return False

        # Валидация страниц: только цифры и больше 0
        if not pages.isdigit() or int(pages) <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом")
            return False

        return True

    def add_book(self):
        if not self.validate_input():
            return

        book = {
            "title": self.title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "genre": self.genre_entry.get().strip(),
            "pages": int(self.pages_entry.get().strip())
        }

        self.books.append(book)
        self.save_books()
        self.update_book_list()

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        
        try:
            pages_filter = int(self.filter_pages.get().strip())
            if pages_filter <= 0:
                raise ValueError
        except ValueError:
            pages_filter = None

        filtered_books = self.books

        if genre_filter:
            filtered_books = [b for b in filtered_books if genre_filter in b['genre'].lower()]

        if pages_filter is not None:
            filtered_books = [b for b in filtered_books if b['pages'] > pages_filter]

        for i in self.book_tree.get_children():
            self.book_tree.delete(i)

        for book in filtered_books:
            self.book_tree.insert('', 'end', values=(book['title'], book['author'], book['genre'], book['pages']))

# Точка входа
if __name__ == '__main__':
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
