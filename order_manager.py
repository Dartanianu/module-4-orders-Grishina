"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


# ============================================
# ЗАДАНИЕ 1.1. get_all_orders
# ============================================
def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


# ============================================
# ЗАДАНИЕ 1.2. get_order_by_id (вспомогательная)
# ============================================
def get_order_by_id(order_id):
    """
    Возвращает заказ по id.
    :param order_id: id заказа
    :return: кортеж (id, дата, клиент) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    return row


# ============================================
# ЗАДАНИЕ 1.3. get_order_items (JOIN)
# ============================================
def get_order_items(order_id):
    """
    Возвращает состав заказа через JOIN.
    :param order_id: id заказа
    :return: список кортежей (id, название, производитель,
                              модель, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
            SELECT Состав_заказа.id, Товар.название, Товар.производитель, Состав_заказа.модель, Состав_заказа.количество, Состав_заказа.цена FROM Состав_заказа JOIN Товар ON Состав_заказа.товар_id = Товар.id WHERE Состав_заказа.заказ_id = ? ORDER BY Состав_заказа.id
    ''', (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


# ============================================
# ЗАДАНИЕ 1.4. get_order_total
# ============================================
def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(количество * цена) FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
    row = cur.fetchone()
    return row[0] or 0.0

# ============================================
# ЗАДАНИЕ 1.5. create_order
# ============================================
def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список (product_id, model, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (date, client))
        order_id = cur.lastrowid
        for product_id, model, quantity, price in items:
            cur.execute("SELECT количество FROM Товар WHERE id = ?",
                        (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")

            cur.execute("INSERT INTO Состав_заказа "
                        "(заказ_id, товар_id, модель, количество, цена) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (order_id, product_id, model, quantity, price))

            cur.execute("UPDATE Товар SET количество = количество - ? "
                        "WHERE id = ?", (quantity, product_id))

        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        return None
    finally:
        conn.close()


# ============================================
# ЗАДАНИЕ 1.6. delete_order
# ============================================
def delete_order(order_id):
    """
    Удаляет заказ и восстанавливает остатки.
    :param order_id: id заказа
    :return: True или False
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
        items = cur.fetchall()
        
        for product_id, quantity in items:
            cur.execute("UPDATE Товар SET количество = количество + ? WHERE id = ?", (quantity, [product_id]))
            cur.execute("DELETE FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
            cur.execute("DELETE FROM Заказ WHERE id = ?", (order_id,))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()


# ============================================
# ЗАДАНИЕ 1.7. update_order_date
# ============================================
def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :param order_id: id заказа
    :param new_date: новая дата (YYYY-MM-DD)
    :return: True
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Заказ SET дата = ? WHERE id = ?", (new_date, order_id))
    conn.commit()
    conn.close()
    return True

# ============================================
# ЗАДАНИЕ 1.8. delete_order_item
# ============================================
def delete_order_item(item_id):
    """
    Удаляет позицию и восстанавливает остаток.
    :param item_id: id позиции в Состав_заказа
    :return: True или False
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE id = ?", (item_id,))
        product_id, quantity = cur.fetchone()
        
        cur.execute("DELETE FROM Состав_заказа WHERE id = ?", (item_id,))
        cur.execute("UPDATE Товар SET количество =  количество + ? WHERE id = ?", (quantity, product_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при удаление позиции{e}")
        conn.rollback()
        return False
    finally:
        conn.close()