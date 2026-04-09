import os

# Динамическое определение путей
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# НАСТРОЙКИ ДВИЖКА (ВЫБОР БЭКЕНДА)
# ==========================================
# Допустимые значения: "vllm" или "ollama"
# "vllm"   - Оптимален для папки с safetensors + json. Супер-быстрый.
# "ollama" - Идеален для GGUF файлов (в том числе разбитых на 5 частей).
ENGINE = "vllm" 

if ENGINE == "vllm":
    # Для vLLM указывается абсолютный путь к папке с файлами модели
    MODEL_PATH_OR_NAME = os.path.expanduser("~/tools/llm")
    PORT = 8000
elif ENGINE == "ollama":
    # Для Ollama указывается имя модели, которую вы собрали командой (ollama create my_qwen -f Modelfile)
    # По умолчанию пусть будет "my_qwen"
    MODEL_PATH_OR_NAME = "my_qwen"
    PORT = 11434
else:
    raise ValueError("ENGINE должен быть либо 'vllm', либо 'ollama'")

# Сетевые настройки (Оба движка полностью поддерживают OpenAI API формат)
API_URL = f"http://127.0.0.1:{PORT}/v1"

# Настройки для интерфейса
APP_TITLE = "Локальный AI Assistant (Qwen)"
APP_SUBTITLE = f"Оффлайн-помощник для кода | Движок: {ENGINE.upper()}"
