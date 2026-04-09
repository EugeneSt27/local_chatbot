import os
import subprocess
import sys
import config

if __name__ == "__main__":
    print(f"Запускаем vLLM бэкенд...")
    print(f"Модель: {config.MODEL_PATH}")
    print(f"Порт: {config.VLLM_PORT}")
    
    # Использование массива аргументов для subprocess гарантирует безопасную обработку путей с пробелами
    command = [
        sys.executable, "-m", "vllm.entrypoints.openai.api_server",
        "--model", config.MODEL_PATH,
        "--port", str(config.VLLM_PORT),
        "--gpu-memory-utilization", "0.90",
        "--max-model-len", "8192" # Полезная настройка для моделей с большим контекстом
    ]
    
    # Запускаем сервер
    subprocess.run(command)
