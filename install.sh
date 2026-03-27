#!/bin/bash
set -e

echo "📦 Устанавливаем зависимости..."
apt update -q
apt install -y python3 python3-pip fzf iptables

echo "🔗 Копируем скрипты..."
cp awg-add-client.py /usr/local/bin/awg-add-client
cp awg-remove-client.py /usr/local/bin/awg-remove-client
cp amnezia.py /usr/local/bin/amnezia

chmod +x /usr/local/bin/awg-add-client
chmod +x /usr/local/bin/awg-remove-client
chmod +x /usr/local/bin/amnezia

echo "✅ Готово! Запускай: amnezia"