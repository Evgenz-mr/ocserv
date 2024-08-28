#!/bin/bash

# Detect the OS type
if [ -f /etc/debian_version ]; then
    OS="Debian"
    INSTALL_CMD="apt-get install -y"
    UPDATE_CMD="apt-get update -y"
elif [ -f /etc/redhat-release ]; then
    OS="CentOS"
    INSTALL_CMD="yum install -y"
    UPDATE_CMD="yum update -y"
else
    echo "Unsupported OS"
    exit 1
fi

# Обновление списка пакетов
$UPDATE_CMD

# Запрос имени пользователя
read -p 'Укажите имя пользователя: ' user

# Запрос пароля
read -sp "Укажите пароль для пользователя $user: " pass
echo  # Переход на новую строку после ввода пароля

# Установка expect
$INSTALL_CMD expect

# Проверка наличия ocpasswd
if ! command -v ocpasswd &> /dev/null; then
    echo "ocpasswd command not found. Please install ocserv."
    exit 1
fi

# Использование expect для автоматического ввода пароля в ocpasswd
expect <<EOF
spawn ocpasswd -c /etc/ocserv/passwd -g default $user
expect "Enter password:"
send "$pass\r"
expect "Re-enter password:"
send "$pass\r"
expect eof
EOF

# Проверка успешности выполнения ocpasswd
if [ $? -ne 0 ]; then
    echo "Failed to set password for user $user"
    exit 1
fi

# Перезапуск сервиса ocserv
echo "Перезапуск службы ocserv..."
sudo systemctl restart ocserv

# Проверка статуса сервиса
sudo systemctl status ocserv --no-pager

# Проверка успешности перезапуска сервиса
if [ $? -ne 0 ]; then
    echo "Failed to restart ocserv service"
    exit 1
fi
