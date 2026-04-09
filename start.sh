#!/bin/bash

# Скрипт запуска Локального AI Ассистента для Linux
# Цвета для красивого вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

echo -e "${GREEN}========================================================${NC}"
echo -e "${GREEN}      Запуск Локального AI-ассистента (Linux)      ${NC}"
echo -e "${GREEN}========================================================${NC}"

# 1. Запуск бэкенда
echo -e "${YELLOW}1. Запуск бэкенда...${NC}"
# Запускаем python в фоновом режиме (&)
# Мы перенаправляем вывод в лог-файл, чтобы он не мешался в терминале, но его можно было проверить
python3 start_backend.py > backend.log 2>&1 &
BACKEND_PID=$!

# Функция для корректного завершения при нажатии Ctrl+C
cleanup() {
    echo -e "\n${YELLOW}Завершение работы...${NC}"
    kill $BACKEND_PID
    exit
}
trap cleanup SIGINT

# 2. Ожидание инициализации
echo -en "${YELLOW}2. Ожидание загрузки модели в GPU (15 сек)...${NC} "
for i in {1..15}; do
    echo -n "."
    sleep 1
done
echo -e " ${GREEN}Готово!${NC}"

# 3. Запуск Streamlit
echo -e "${YELLOW}3. Запуск интерфейса Streamlit...${NC}"
# Streamlit обычно блокирует терминал, пока вы его не закроете
streamlit run app.py

# Если Streamlit завершил работу (вы нажали Ctrl+C)
cleanup
