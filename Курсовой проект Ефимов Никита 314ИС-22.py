import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Определяем роли и их права доступа
USER_CREDENTIALS = {
    "admin": "adminpassword",  # Логин и пароль для администратора
    "user": "userpassword"  # Логин и пароль для обычного пользователя
}


# Создание базы данных и таблиц
def init_db():
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()

    # Создание таблиц с полем для времени добавления, если они не существуют
    cursor.execute('''CREATE TABLE IF NOT EXISTS properties (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')

    # Таблицы для удаленных объектов
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS deleted_properties (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS deleted_clients (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS deleted_reports (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT)''')

    conn.commit()
    conn.close()


def login():
    username = entry_username.get()
    password = entry_password.get()

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        messagebox.showinfo("Успех", "Вы успешно вошли в систему!")
        open_main_window(username)
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")


def open_main_window(username):
    global root  # Делаем root глобальной переменной
    root.destroy()
    main_window = tk.Tk()
    main_window.title("Главное окно системы учета недвижимости")
    main_window.geometry("600x500")

    label = tk.Label(main_window, text="Добро пожаловать в систему учета недвижимости!", font=("Arial", 14))
    label.pack(pady=20)

    btn_properties = tk.Button(main_window, text="Объекты недвижимости",
                               command=lambda: open_properties_window(username))
    btn_properties.pack(pady=10)

    if username == "admin":
        btn_clients = tk.Button(main_window, text="Клиенты", command=lambda: open_clients_window(username))
        btn_clients.pack(pady=10)

        btn_reports = tk.Button(main_window, text="Отчеты", command=lambda: open_reports_window(username))
        btn_reports.pack(pady=10)

    # Кнопка выхода
    btn_logout = tk.Button(main_window, text="Выход", command=lambda: logout(main_window))
    btn_logout.pack(pady=20)

    main_window.mainloop()


def logout(current_window):
    current_window.destroy()  # Закрываем текущее окно
    open_login_window()  # Открываем окно входа


def open_login_window():
    global root
    root = tk.Tk()
    root.title("Система учета недвижимости")
    root.geometry("600x500")

    # Метки и поля для ввода логина и пароля
    label_username = tk.Label(root, text="Логин:")
    label_username.pack(pady=5)

    global entry_username  # Делаем entry_username глобальной переменной
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    label_password = tk.Label(root, text="Пароль:")
    label_password.pack(pady=5)

    global entry_password  # Делаем entry_password глобальной переменной
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    # Кнопка для входа в систему
    btn_login = tk.Button(root, text="Войти", command=login)
    btn_login.pack(pady=20)

    # Запуск главного цикла приложения
    root.mainloop()


def fetch_properties():
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, created_at FROM properties")

    properties = cursor.fetchall()  # Получаем все строки

    conn.close()

    return properties


def fetch_clients():
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, created_at FROM clients")

    clients = cursor.fetchall()  # Получаем все строки

    conn.close()

    return clients


def fetch_reports():
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, created_at FROM reports")

    reports = cursor.fetchall()  # Получаем все строки

    conn.close()

    return reports


def open_properties_window(username):
    properties_window = tk.Toplevel()
    properties_window.title("Объекты недвижимости")
    properties_window.geometry("600x500")

    label_info = tk.Label(properties_window, text="Список объектов недвижимости:", font=("Arial", 12))
    label_info.pack(pady=10)

    listbox_properties = tk.Listbox(properties_window)
    listbox_properties.pack(pady=10, fill=tk.BOTH, expand=True)

    # Заполняем список объектов недвижимости из базы данных
    for property in fetch_properties():
        property_info = f"{property[0]} (Добавлено: {property[1]})"
        listbox_properties.insert(tk.END, property_info)

    if username == "admin":  # Проверка на администратора
        def add_property():
            new_property = entry_property.get()
            if new_property:
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO properties (name, created_at) VALUES (?, ?)", (new_property, created_at))
                conn.commit()
                conn.close()

                listbox_properties.insert(tk.END,
                                          f"{new_property} (Добавлено: {created_at})")
                entry_property.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите название объекта.")

        def remove_property():
            selected_property_index = listbox_properties.curselection()
            if selected_property_index:
                property_name_info = listbox_properties.get(selected_property_index)
                property_name = property_name_info.split(" (")[0]

                # Перемещаем объект в таблицу удаленных объектов
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO deleted_properties (name, created_at) VALUES (?, ?)",
                               (property_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                cursor.execute("DELETE FROM properties WHERE name=?", (property_name,))
                conn.commit()
                conn.close()

                listbox_properties.delete(selected_property_index)
            else:
                messagebox.showwarning("Предупреждение", "Выберите объект для удаления.")

        def open_deleted_properties_window():
            deleted_properties_window = tk.Toplevel()
            deleted_properties_window.title("Удаленные объекты")
            deleted_properties_window.geometry("600x500")

            label_info_deleted = tk.Label(deleted_properties_window, text="Список удаленных объектов:",
                                          font=("Arial", 12))
            label_info_deleted.pack(pady=10)

            listbox_deleted_properties = tk.Listbox(deleted_properties_window)
            listbox_deleted_properties.pack(pady=10, fill=tk.BOTH, expand=True)

            # Заполняем список удаленных объектов из базы данных
            conn = sqlite3.connect('DB.db')
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM deleted_properties")

            deleted_properties = cursor.fetchall()  # Получаем все строки

            for property in deleted_properties:
                listbox_deleted_properties.insert(tk.END, property[0])  # Добавляем только имя

            close_button_deleted = tk.Button(deleted_properties_window, text="Закрыть",
                                             command=deleted_properties_window.destroy)
            close_button_deleted.pack(pady=10)

        entry_property = tk.Entry(properties_window)
        entry_property.pack(pady=5)

        btn_add_property = tk.Button(properties_window, text="Добавить объект", command=add_property)
        btn_add_property.pack(pady=5)

        btn_remove_property = tk.Button(properties_window, text="Удалить объект", command=remove_property)
        btn_remove_property.pack(pady=5)

        btn_view_deleted_properties = tk.Button(properties_window,
                                                text="Просмотреть удаленные объекты",
                                                command=open_deleted_properties_window)
        btn_view_deleted_properties.pack(pady=5)

    close_button = tk.Button(properties_window, text="Закрыть", command=properties_window.destroy)
    close_button.pack(pady=10)


def open_clients_window(username):
    clients_window = tk.Toplevel()
    clients_window.title("Клиенты")
    clients_window.geometry("600x500")

    label_info_clients = tk.Label(clients_window, text="Список клиентов:", font=("Arial", 12))
    label_info_clients.pack(pady=10)

    listbox_clients = tk.Listbox(clients_window)
    listbox_clients.pack(pady=10, fill=tk.BOTH, expand=True)

    for client in fetch_clients():
        client_info = f"{client[0]} (Добавлено: {client[1]})"
        listbox_clients.insert(tk.END, client_info)

    if username == "admin":  # Проверка на администратора
        def add_client():
            new_client = entry_client.get()
            if new_client:
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clients (name, created_at) VALUES (?, ?)", (new_client, created_at))
                conn.commit()
                conn.close()

                listbox_clients.insert(tk.END,
                                       f"{new_client} (Добавлено: {created_at})")
                entry_client.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите имя клиента.")

        def remove_client():
            selected_client_index = listbox_clients.curselection()
            if selected_client_index:
                client_name_info = listbox_clients.get(selected_client_index)
                client_name = client_name_info.split(" (")[0]

                # Перемещаем клиента в таблицу удаленных клиентов
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO deleted_clients (name, created_at) VALUES (?, ?)",
                               (client_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                cursor.execute("DELETE FROM clients WHERE name=?", (client_name,))
                conn.commit()
                conn.close()

                listbox_clients.delete(selected_client_index)
            else:
                messagebox.showwarning("Предупреждение", "Выберите клиента для удаления.")

        def open_deleted_clients_window():
            deleted_clients_window = tk.Toplevel()
            deleted_clients_window.title("Удаленные клиенты")
            deleted_clients_window.geometry("600x500")

            label_info_deleted_clients = tk.Label(deleted_clients_window,
                                                  text="Список удаленных клиентов:", font=("Arial", 12))
            label_info_deleted_clients.pack(pady=10)

            listbox_deleted_clients = tk.Listbox(deleted_clients_window)
            listbox_deleted_clients.pack(pady=10, fill=tk.BOTH, expand=True)

            # Заполняем список удаленных клиентов из базы данных
            conn = sqlite3.connect('DB.db')
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM deleted_clients")

            deleted_clients = cursor.fetchall()  # Получаем все строки

            for client in deleted_clients:
                listbox_deleted_clients.insert(tk.END, client[0])  # Добавляем только имя

            close_button_deleted_clients = tk.Button(deleted_clients_window,
                                                     text="Закрыть",
                                                     command=deleted_clients_window.destroy)
            close_button_deleted_clients.pack(pady=10)

        entry_client = tk.Entry(clients_window)
        entry_client.pack(pady=5)

        btn_add_client = tk.Button(clients_window,
                                   text="Добавить клиента",
                                   command=add_client)
        btn_add_client.pack(pady=5)

        btn_remove_client = tk.Button(clients_window,
                                      text="Удалить клиента",
                                      command=remove_client)
        btn_remove_client.pack(pady=5)

        btn_view_deleted_clients = tk.Button(clients_window,
                                             text="Просмотреть удаленные клиенты",
                                             command=open_deleted_clients_window)
        btn_view_deleted_clients.pack(pady=5)

    close_button_clients = tk.Button(clients_window,
                                     text="Закрыть",
                                     command=clients_window.destroy)
    close_button_clients.pack(pady=10)


def open_reports_window(username):
    reports_window = tk.Toplevel()
    reports_window.title("Отчеты")
    reports_window.geometry("600x500")

    label_info_reports = tk.Label(reports_window,
                                  text="Список отчетов:", font=("Arial", 12))
    label_info_reports.pack(pady=10)

    listbox_reports = tk.Listbox(reports_window)
    listbox_reports.pack(pady=10, fill=tk.BOTH, expand=True)

    for report in fetch_reports():
        report_info = f"{report[0]} (Добавлено: {report[1]})"
        listbox_reports.insert(tk.END, report_info)

    if username == "admin":  # Проверка на администратора
        def add_report():
            new_report = entry_report.get()
            if new_report:
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO reports (name, created_at) VALUES (?, ?)", (new_report, created_at))
                conn.commit()
                conn.close()

                listbox_reports.insert(tk.END,
                                       f"{new_report} (Добавлено: {created_at})")
                entry_report.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите название отчета.")

        def remove_report():
            selected_report_index = listbox_reports.curselection()
            if selected_report_index:
                report_name_info = listbox_reports.get(selected_report_index)
                report_name = report_name_info.split(" (")[0]

                # Перемещаем отчет в таблицу удаленных отчетов
                conn = sqlite3.connect('DB.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO deleted_reports (name, created_at) VALUES (?, ?)",
                               (report_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                cursor.execute("DELETE FROM reports WHERE name=?", (report_name,))
                conn.commit()
                conn.close()

                listbox_reports.delete(selected_report_index)
            else:
                messagebox.showwarning("Предупреждение", "Выберите отчет для удаления.")

        def open_deleted_reports_window():
            deleted_reports_window = tk.Toplevel()
            deleted_reports_window.title("Удаленные отчеты")
            deleted_reports_window.geometry("600x500")

            label_info_deleted_reports = tk.Label(deleted_reports_window,
                                                  text="Список удаленных отчетов:", font=("Arial", 12))
            label_info_deleted_reports.pack(pady=10)

            listbox_deleted_reports = tk.Listbox(deleted_reports_window)
            listbox_deleted_reports.pack(pady=10, fill=tk.BOTH, expand=True)

            # Заполняем список удаленных отчетов из базы данных
            conn = sqlite3.connect('DB.db')
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM deleted_reports")

            deleted_reports = cursor.fetchall()  # Получаем все строки

            for report in deleted_reports:
                listbox_deleted_reports.insert(tk.END, report[0])  # Добавляем только имя

            close_button_deleted_reports = tk.Button(deleted_reports_window,
                                                     text="Закрыть",
                                                     command=deleted_reports_window.destroy)
            close_button_deleted_reports.pack(pady=10)

        entry_report = tk.Entry(reports_window)
        entry_report.pack(pady=5)

        btn_add_report = tk.Button(reports_window,
                                   text="Добавить отчет",
                                   command=add_report)
        btn_add_report.pack(pady=5)

        btn_remove_report = tk.Button(reports_window,
                                      text="Удалить отчет",
                                      command=remove_report)
        btn_remove_report.pack(pady=5)

        btn_view_deleted_reports = tk.Button(reports_window,
                                             text="Просмотреть удаленные отчеты",
                                             command=open_deleted_reports_window)
        btn_view_deleted_reports.pack(pady=5)

    close_button_reports = tk.Button(reports_window,
                                     text="Закрыть",
                                     command=reports_window.destroy)
    close_button_reports.pack(pady=10)

# Инициализация базы данных при запуске программы
init_db()

# Создание основного окна
open_login_window()  # Запускаем окно входа при старте программы.
