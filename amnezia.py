#!/usr/bin/env python3
import os, subprocess, sys

DIR = "/etc/amnezia/amneziawg"

def fzf(items, header="", preview=False):
    args = ["fzf", "--height=15", "--border", "--no-info", "--pointer=➤"]
    if header:
        args += ["--header", header]
    result = subprocess.run(args, input="\n".join(items), capture_output=True, text=True)
    return result.stdout.strip()

def header():
    os.system("clear")
    print("╔══════════════════════════════╗")
    print("║      AMNEZIA VPN MANAGER     ║")
    print("╚══════════════════════════════╝")

def server_status():
    result = subprocess.run("awg show awg0 2>/dev/null | grep 'listening port'",
                            shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        port = result.stdout.strip().split()[-1]
        return f"🟢 Запущен (порт {port})"
    return "🔴 Остановлен"

def server_menu():
    while True:
        header()
        print(f"  Сервер: {server_status()}\n")
        choice = fzf([
            "▶️  Запустить",
            "🔄 Перезапустить",
            "⏹️  Остановить",
            "📊 Статус",
            "🔧 Починить",
            "⬅️  Назад"
        ], header="Управление сервером")

        if choice == "▶️  Запустить":
            os.system("sysctl -w net.ipv4.ip_forward=1")
            os.system(f"awg-quick up {DIR}/awg0.conf")
        elif choice == "🔄 Перезапустить":
            os.system(f"awg-quick down {DIR}/awg0.conf")
            os.system("sysctl -w net.ipv4.ip_forward=1")
            os.system(f"awg-quick up {DIR}/awg0.conf")
        elif choice == "⏹️  Остановить":
            os.system(f"awg-quick down {DIR}/awg0.conf")
        elif choice == "📊 Статус":
            header()
            os.system("awg show")
            input("\nEnter...")
        elif choice == "🔧 Починить":
            os.system("sysctl -w net.ipv4.ip_forward=1")
            os.system("echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/99-vpn.conf")
            os.system("iptables -A INPUT -p udp --dport 51820 -j ACCEPT 2>/dev/null")
            os.system("iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT 2>/dev/null")
            os.system(f"awg-quick down {DIR}/awg0.conf 2>/dev/null; awg-quick up {DIR}/awg0.conf")
            print("✅ Готово!")
            input("\nEnter...")
        else:
            break

while True:
    header()
    choice = fzf([
        "➕ Добавить клиента",
        "📋 Список клиентов",
        "🗑️  Удалить клиента",
        "🖥️  Управление сервером",
        "❌ Выход"
    ])

    if choice == "➕ Добавить клиента":
        header()
        os.system("awg-add-client")
        input("\nEnter...")
    elif choice == "📋 Список клиентов":
        os.system("awg show awg0 allowed-ips")
        input("\nEnter...")
    elif choice == "🗑️  Удалить клиента":
        os.system("awg-remove-client")
    elif choice == "🖥️  Управление сервером":
        server_menu()
    elif choice == "❌ Выход":
        os.system("clear")
        sys.exit(0)