"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT, FONT_SIZE_HEADER,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int


class ViewForm:
    """Форма просмотра товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение — ГОТОВО
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        photo = get_product_image(self.product[7], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        # Информация — ДОПИСАТЬ
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Производитель", self.product[3])
        self._add_field(info_frame, "Наименование", self.product[1])
        self._add_field(info_frame, "Категория", self.product[2])
        self._add_field(info_frame, "Характеристики", self.product[4])
        self._add_field(info_frame, "Цена", self.product[3])
        self._add_field(info_frame, "Модель", self.product[8])

        # Поле ввода количества — ДОПИСАТЬ
        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(qty_frame, text="Количество:", font=font(FONT_SIZE_HEADER, bold=True), bg=COLOR_MAIN_BG, width=25, anchor="w").pack(side="left")
        self.qty_var = tk.StringVar(value="1")

        # Кнопки — ДОПИСАТЬ
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        btn_add = tk.Button(btn_frame, text="Добавить в заказ", command=self.add_to_order,
                            bg=COLOR_ACCENT, fg="white", padx=15, pady=5)
        btn_add.pack(side="left", padx=20)
        
        btn_back = tk.Button(btn_frame, text="Назад", command=self.window.destroy,
                            bg=COLOR_ACCENT, fg="white", padx=15, pady=5)
        btn_back.pack(side="left", padx=20)

    def _add_field(self, parent, label, value):
        """
        Добавляет поле в форму.
        :param parent: родительский фрейм
        :param label: название поля
        :param value: значение
        """
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", padx=3)
        
        label_txt = tk.Label(row, text=f"{label}", font=font(FONT_SIZE_NORMAL, bold=True), width=15, anchor="w", bg=COLOR_MAIN_BG).pack(side="left")
        value_txt = tk.Label(row, text=str(value), font=font(FONT_SIZE_NORMAL, bold=True), width=15, anchor="w", bg=COLOR_MAIN_BG)
        value_txt.pack(side="left", fill="x")

    def add_to_order(self):
        """Обработчик добавления в заказ."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        
        if not ok:
            messagebox.showerror("Ошибка ввода", result)
            return
        qty = result
        
        try:
            product_id = self.product.id
            current_qty = get_product_quantity(product_id)

            if qty_now < 1:
                messagebox.showwarning("Внимание", "Товар закончился")
                return
            if qty > current_qty:
                messagebox.showwarning("Внимание", f"В наличии только {current_qty} шт.")
                return
                       
            messagebox.showinfo("Успех", "Заказ оформлен")
            
            if self.on_add_to_order:
                self.on_add_to_order()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось оформить заказ{e}")