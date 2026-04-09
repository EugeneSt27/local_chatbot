import os
import subprocess
import sys
import config
import time

if __name__ == "__main__":
    print("==========================================")
    print(f"Выбранный движок инференса:  {config.ENGINE.upper()}")
    if config.ENGINE == "vllm":
        print(f"Путь к папке модели:         {config.MODEL_PATH_OR_NAME}")
    else:
        print(f"Имя модели в хранилище:      {config.MODEL_PATH_OR_NAME}")
    print(f"Порт подключения:            {config.PORT}")
    print("==========================================")
    
    if config.ENGINE == "vllm":
        print("Запускаем сервер vLLM. Модель загружается в память GPU...")
        command = [
            sys.executable, "-m", "vllm.entrypoints.openai.api_server",
            "--model", config.MODEL_PATH_OR_NAME,
            "--port", str(config.PORT),
            "--gpu-memory-utilization", "0.90",
            "--max-model-len", "8192"
        ]
        # Блокирующий запуск vLLM
        subprocess.run(command)
        
    elif config.ENGINE == "ollama":
        print("Пробуем вызвать сервер Ollama...")
        print("Примечание: Обычно Ollama уже запущена как фоновая служба Windows.")
        try:
            # Пытаемся запустить сервер Ollama
            subprocess.run(["ollama", "serve"])
        except Exception as e:
            print(f"Ошибка при попытке запустить Ollama через командную строку: {e}")
            print("Убедитесь, что Ollama установлена и добавлена в PATH среды Windows.")
        
        # Если ollama уже была запущена в фоне, команда `ollama serve` сразу завершит работу
        # Делаем паузу, чтобы окно не захлопнулось мгновенно и пользователь успел прочитать
        time.sleep(5)
        print("Если окно закроется — не волнуйтесь, значит Ollama работает в фоновом режиме-службе.")
