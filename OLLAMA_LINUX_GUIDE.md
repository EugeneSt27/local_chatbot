# Инструкция по развертыванию Ollama в закрытом контуре (Linux)

## 1. Подготовка бинарного файла
1. Скачайте [ollama-linux-amd64.tgz](https://ollama.com/download/ollama-linux-amd64.tgz).
2. Перенесите на сервер.
3. Установите: `sudo tar -C /usr -xzf ollama-linux-amd64.tgz`.
4. Проверьте: `ollama --version`.

## 2. Импорт ваших GGUF файлов (если модель разбита на части)
1. Перейдите в папку с файлами `.gguf`.
2. Создайте файл `Modelfile`:
   ```text
   FROM ./имя_вашего_файла_00001-of-00005.gguf
   PARAMETER temperature 0.3
   ```
3. Создайте модель: `ollama create my_qwen -f Modelfile`.

## 3. Запуск в составе проекта
1. В `config.py` выставите:
   - `ENGINE = "ollama"`
   - `MODEL_PATH_OR_NAME = "my_qwen"`
2. Запустите `./start.bat` (или запустите `start_backend.py` и `app.py` вручную через `python`).

## 4. Полезные команды Ollama
- `ollama list` — список всех доступных локально моделей.
- `ollama rm <name>` — удалить модель.
- `ollama serve` — запуск сервера (обычно работает в фоне).
