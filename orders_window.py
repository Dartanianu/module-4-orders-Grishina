"""Окно списка заказов."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent, current_user=None):
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_orders()

    def is_admin(self):
        """Проверяет роль Администратора."""
        return( self.current_user and self.current_user[5] == "Администратор")

    def build_ui(self):
        """Строит интерфейс."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="СПИСОК ЗАКАЗОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Treeview — ДОПИСАТЬ
        columns = ("id", "date", "client")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("client", text="Клиент")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("client", width=400, anchor="w")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        self.tree.bind("<Double-1>", self.on_order_select)

        btn_frame = tk.Button(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="Просмотор состава", command=self.on_order_select)
        
        tk.Button(btn_frame, text="Обновить", command=self.load_orders)
        
        tk.Button(btn_frame, text="Назад", command=self.window.destroy)

    def load_orders(self):
        """Загружает заказы из БД."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            orders = om.get_all_orders()
            for order in orders:
                self.tree.insert("", tk.END, values=order)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите заказ")
            return

        item = self.tree.item(selected[0])
        order_id = item["values"][0]
        from order_items_window import OrderItemsWindow
        OrderItemsWindow(self.window, order_id, self.current_user)