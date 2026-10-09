"""Каталог товаров."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """
    Создаёт карточку товара.
    :param parent: родительский контейнер
    :param product: кортеж (id, название, категория, производитель,
                            характеристики, цена, количество,
                            изображение, модель)
    :param refresh: callback для обновления каталога после заказа
    :return: созданный Frame
    """
    qty = product[6]
    bg_color = _get_card_color(qty)
    
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    
    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)
    
    card.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    for child in card.winfo_children():
        child.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    return card


def _get_card_color(qty):
    """
    Возвращает цвет фона карточки.
    Если количество ≤ 3 — подсветка #ff8080, иначе белый.
    :param qty: количество товара
    :return: HEX-цвет
    """
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


        
def _add_image(card, product, bg_color):
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product[7], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

def _add_text_info(card, product, bg_color, qty):
    """
    Добавляет текстовую информацию о товаре.
    :param card: карточка товара
    :param product: кортеж с данными товара
    :param bg_color: цвет фона
    :param qty: количество
    """
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    name = product[1] if product[1] else "[Без названия]"
    production = product[3] if product[3] else "[Без производителя]"
    category = product[2] if product[2] else "[Без категории]"
    characteristics = product[4] if product[4] else "[Не указаны]"
    price = product[5] if product[5] is not None else 0

    _add_label(text_frame, f"{production} | {name}", bg_color, bold=True)
    _add_label(text_frame, f"Категория: {category}", bg_color,)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty})", bg_color,)
    _add_label(text_frame, f"Характеристики: {characteristics}", bg_color,)    
    _add_label(text_frame, f"{price} руб.", bg_color, size=FONT_SIZE_HEADER, align="e")
    

def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """
    Добавляет метку с текстом.
    :param parent: родительский фрейм
    :param text: текст метки
    :param bg_color: цвет фона
    :param bold: жирный шрифт
    :param size: размер шрифта
    :param align: выравнивание ("w" — слева, "e" — справа)
    """
    tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).
    :param qty: количество
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"


def _open_view(parent, product, refresh=None):
    """
    Открывает форму просмотра товара.
    :param parent: родительское окно
    :param product: кортеж с данными товара
    :param refresh: callback для обновления каталога
    """
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)