import os

# Список IP-адресов для блокировки
ip_addresses = {
    "login0": [
        "92.223.6.72", "92.223.6.73", "92.223.6.71", "92.223.6.76",
        "92.223.6.75", "92.223.6.74"
    ],
    "login2": [
        "92.223.14.222", "92.223.14.223", "92.223.14.214", "92.223.14.216"
    ],
    "login3": [
        "92.38.156.142", "92.38.156.93", "92.38.156.13", "92.38.156.189"
    ],
    "login4": [
        "92.223.4.190", "92.223.4.178", "92.223.4.179"
    ],
    "login5": [
        "92.223.41.34", "92.223.41.195", "92.223.41.183", "92.223.41.129"
    ]
}

def rule_exists(rule_name):
    command = f'netsh advfirewall firewall show rule name="{rule_name}"'
    result = os.system(command)
    return result == 0

def block_ips(selected_logins):
    for login in selected_logins:
        if login in ip_addresses:
            for ip in ip_addresses[login]:
                command = f'netsh advfirewall firewall add rule name="Block {ip}" dir=out action=block remoteip={ip}'
                print(f"Выполнение: {command}")
                os.system(command)
        else:
            print(f"Логин '{login}' не найден.")

def unblock_ips(selected_logins):
    for login in selected_logins:
        if login in ip_addresses:
            for ip in ip_addresses[login]:
                rule_name = f"Block {ip}"
                if rule_exists(rule_name):
                    command = f'netsh advfirewall firewall delete rule name="{rule_name}"'
                    print(f"Выполнение: {command}")
                    os.system(command)
                else:
                    print(f"Правило '{rule_name}' не найдено.")
        else:
            print(f"Логин '{login}' не найден.")

def main():
    # Меню выбора действия
    print("Выберите действие:")
    print("1. Заблокировать IP-адреса")
    print("2. Разблокировать IP-адреса")
    
    action = input("Введите номер действия (1 или 2): ").strip()

    # Проверка выбора действия
    if action == "1":
        action = "block"
    elif action == "2":
        action = "unblock"
    else:
        print("Неправильный выбор. Завершение программы.")
        return

    # Выбор логинов для обработки
    available_logins = list(ip_addresses.keys())
    print("Доступные логины:")
    for i, login in enumerate(available_logins, 1):
        print(f"{i}. {login}")
    
    selected_indices = input("Введите номера логинов, которые хотите обработать (например: 1,3,5): ").replace(' ', '').split(',')

    try:
        selected_logins = [available_logins[int(index) - 1] for index in selected_indices]
    except (ValueError, IndexError):
        print("Ошибка: Введены некорректные номера логинов.")
        return

    if action == "block":
        block_ips(selected_logins)
    elif action == "unblock":
        unblock_ips(selected_logins)

if __name__ == "__main__":
    main()
