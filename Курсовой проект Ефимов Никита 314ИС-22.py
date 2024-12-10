import tkinter as tk
from tkinter import messagebox

# Определяем роли и их права доступа
USER_CREDENTIALS = {
    "admin": "adminpassword",  # Логин и пароль для администратора
    "user": "userpassword"  # Логин и пароль для обычного пользователя
}

# Списки для хранения объектов недвижимости, клиентов и отчетов
properties = []
clients = []
reports = []


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


def open_properties_window(username):
    properties_window = tk.Toplevel()
    properties_window.title("Объекты недвижимости")
    properties_window.geometry("600x500")

    label_info = tk.Label(properties_window, text="Список объектов недвижимости:", font=("Arial", 12))
    label_info.pack(pady=10)

    listbox_properties = tk.Listbox(properties_window)
    listbox_properties.pack(pady=10, fill=tk.BOTH, expand=True)

    # Заполняем список объектов недвижимости
    for property in properties:
        listbox_properties.insert(tk.END, property)

    if username == "admin":  # Проверка на администратора
        def add_property():
            new_property = entry_property.get()
            if new_property:
                properties.append(new_property)  # Добавляем объект в общий список
                listbox_properties.insert(tk.END, new_property)  # Обновляем список в окне
                entry_property.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите название объекта.")

        def remove_property():
            selected_property_index = listbox_properties.curselection()
            if selected_property_index:
                properties.pop(selected_property_index[0])  # Удаляем из общего списка
                listbox_properties.delete(selected_property_index)  # Обновляем список в окне
            else:
                messagebox.showwarning("Предупреждение", "Выберите объект для удаления.")

        entry_property = tk.Entry(properties_window)
        entry_property.pack(pady=5)

        btn_add_property = tk.Button(properties_window, text="Добавить объект", command=add_property)
        btn_add_property.pack(pady=5)

        btn_remove_property = tk.Button(properties_window, text="Удалить объект", command=remove_property)
        btn_remove_property.pack(pady=5)

    close_button = tk.Button(properties_window, text="Закрыть", command=properties_window.destroy)
    close_button.pack(pady=10)


def open_clients_window(username):
    clients_window = tk.Toplevel()
    clients_window.title("Клиенты")
    clients_window.geometry("600x500")

    label_info = tk.Label(clients_window, text="Список клиентов:", font=("Arial", 12))
    label_info.pack(pady=10)

    listbox_clients = tk.Listbox(clients_window)
    listbox_clients.pack(pady=10, fill=tk.BOTH, expand=True)

    for client in clients:
        listbox_clients.insert(tk.END, client)

    if username == "admin":  # Проверка на администратора
        def add_client():
            new_client = entry_client.get()
            if new_client:
                clients.append(new_client)
                listbox_clients.insert(tk.END, new_client)
                entry_client.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите имя клиента.")

        def remove_client():
            selected_client_index = listbox_clients.curselection()
            if selected_client_index:
                clients.pop(selected_client_index[0])
                listbox_clients.delete(selected_client_index)
            else:
                messagebox.showwarning("Предупреждение", "Выберите клиента для удаления.")

        entry_client = tk.Entry(clients_window)
        entry_client.pack(pady=5)

        btn_add_client = tk.Button(clients_window, text="Добавить клиента", command=add_client)
        btn_add_client.pack(pady=5)

        btn_remove_client = tk.Button(clients_window, text="Удалить клиента", command=remove_client)
        btn_remove_client.pack(pady=5)

    close_button = tk.Button(clients_window, text="Закрыть", command=clients_window.destroy)
    close_button.pack(pady=10)


def open_reports_window(username):
    reports_window = tk.Toplevel()
    reports_window.title("Отчеты")
    reports_window.geometry("600x500")

    label_info = tk.Label(reports_window, text="Список отчетов:", font=("Arial", 12))
    label_info.pack(pady=10)

    listbox_reports = tk.Listbox(reports_window)
    listbox_reports.pack(pady=10, fill=tk.BOTH, expand=True)

    for report in reports:
        listbox_reports.insert(tk.END, report)

    if username == "admin":  # Проверка на администратора
        def add_report():
            new_report = entry_report.get()
            if new_report:
                reports.append(new_report)
                listbox_reports.insert(tk.END, new_report)
                entry_report.delete(0, tk.END)
            else:
                messagebox.showwarning("Предупреждение", "Введите название отчета.")

        def remove_report():
            selected_report_index = listbox_reports.curselection()
            if selected_report_index:
                reports.pop(selected_report_index[0])
                listbox_reports.delete(selected_report_index)
            else:
                messagebox.showwarning("Предупреждение", "Выберите отчет для удаления.")

        entry_report = tk.Entry(reports_window)
        entry_report.pack(pady=5)

        btn_add_report = tk.Button(reports_window, text="Добавить отчет", command=add_report)
        btn_add_report.pack(pady=5)

        btn_remove_report = tk.Button(reports_window, text="Удалить отчет", command=remove_report)
        btn_remove_report.pack(pady=5)

    close_button = tk.Button(reports_window, text="Закрыть", command=reports_window.destroy)
    close_button.pack(pady=10)


# Создание основного окна
open_login_window()  # Запускаем окно входа при старте программы