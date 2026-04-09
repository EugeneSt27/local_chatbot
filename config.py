import os

# Динамическое определение путей, чтобы все работало стабильно
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Путь к вашей модели (используем os.path.expanduser для корректной обработки "~" в Windows/Linux)
# Если вы перенесете папку с моделью в другое место, просто измените этот путь
MODEL_PATH = os.path.expanduser("~/tools/llm")

# Сетевые настройки
VLLM_PORT = 8000
# Используем 127.0.0.1 вместо localhost для защиты от IPv6-коллизий на Windows
VLLM_API_URL = f"http://127.0.0.1:{VLLM_PORT}/v1"

# Настройки для интерфейса
APP_TITLE = "Локальный AI Assistant (Qwen)"
APP_SUBTITLE = "Оффлайн-помощник для кода на базе vLLM"
