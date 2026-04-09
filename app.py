import streamlit as st
from openai import OpenAI
import config
import os
import json
import datetime

# Расширенные настройки страницы
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Простые CSS-улучшения для преформатированных блоков (очень важно для кода)
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title(config.APP_TITLE)
st.caption(config.APP_SUBTITLE)

# ================================
# ЛОГИКА СОХРАНЕНИЯ ИСТОРИИ
# ================================
# Используем абсолютный путь к папке истории для гарантии стабильности работы Streamlit из любого окружения
HISTORY_DIR = os.path.join(config.SCRIPT_DIR, "history")

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def get_history_files():
    """Возвращает список файлов истории, отсортированный по дате создания (новые сверху)"""
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    files.sort(reverse=True)
    return files

def load_history(filename):
    """Загружает сообщения из указанного файла истории"""
    path = os.path.join(HISTORY_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(filename, messages):
    """Сохраняет текущий список сообщений в файл"""
    path = os.path.join(HISTORY_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# ================================
# БОКОВАЯ ПАНЕЛЬ С ДИАЛОГАМИ
# ================================
with st.sidebar:
    st.header("Управление историей")
    
    # Кнопка создания нового диалога
    if st.button("➕ Новый диалог", use_container_width=True):
        new_session = f"chat_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        st.session_state.current_session = new_session
        st.session_state.messages = [
            {"role": "assistant", "content": "Привет! Я ваш локальный помощник. Чем могу помочь с написанием кода сегодня?"}
        ]
        save_history(new_session, st.session_state.messages)
        st.rerun()

    st.markdown("### Старые диалоги")
    
    files = get_history_files()
    
    # Инициализация состояния: если мы только зашли, пытаемся открыть самый свежий
    if "current_session" not in st.session_state:
        if len(files) > 0:
            st.session_state.current_session = files[0]
        else:
            first_session = f"chat_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            st.session_state.current_session = first_session
            
    # Загрузка сообщений в память состояния из активного файла сессии
    if "messages" not in st.session_state:
        if st.session_state.current_session in files:
            st.session_state.messages = load_history(st.session_state.current_session)
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": f"Привет! Модель инициализируется (источник: `{config.MODEL_PATH_OR_NAME}`). Готов написать для вас код!"}
            ]
            save_history(st.session_state.current_session, st.session_state.messages)
            files = get_history_files() # обновляем список файлов, чтобы новый отобразился в Sidebar

    # UI Селектора выбора: он всегда будет показывать актуальный файл
    selected_file = st.selectbox(
        "Выберите сессию из списка:", 
        options=files if files else [st.session_state.current_session],
        index=files.index(st.session_state.current_session) if st.session_state.current_session in files else 0
    )
    
    # Если пользователь переключил выбор в селекторе - грузим прошлую историю
    if selected_file != st.session_state.current_session:
        st.session_state.current_session = selected_file
        st.session_state.messages = load_history(selected_file)
        st.rerun() # Мгновенная перезагрузка интерфейса

# ================================
# ИНТЕРФЕЙС И ВЗАИМОДЕЙСТВИЕ
# ================================
# Инициализация клиента OpenAI для локального сервера (vLLM или Ollama)
client = OpenAI(
    api_key="EMPTY",
    base_url=config.API_URL,
)

# Вывод всей истории на главный экран
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

@st.cache_data(ttl=60)
def get_model():
    """Попытка найти название модели динамически (которое отдаст локальный бэкенд)"""
    try:
        models = client.models.list()
        return models.data[0].id
    except Exception:
        return config.MODEL_PATH_OR_NAME

# Пользовательский ввод
if prompt := st.chat_input("Напишите ваш вопрос (например, 'Сделай ревью этой функции...') ..."):
    # Добавляем вопрос пользователя в интерфейс
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_history(st.session_state.current_session, st.session_state.messages)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерация ответа Модели
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            model_id = get_model()
            # Обращаемся к запущенной локальной LLM в режиме потокового генератора (печатает символы по мере "раздумий")
            stream = client.chat.completions.create(
                model=model_id,
                messages=st.session_state.messages,
                stream=True,
                temperature=0.3, # Температура 0.3 отлично подходит для точного написания программного кода
                max_tokens=8192,
            )
            
            for response in stream:
                if response.choices[0].delta.content is not None:
                    # Наращиваем ответ и показываем "каретку загрузки"
                    full_response += response.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            # Финальный принт без каретки
            message_placeholder.markdown(full_response)
            
            # Сохраняем генерацию в историю
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_history(st.session_state.current_session, st.session_state.messages)
            
        except Exception as e:
            st.error(f"⚠️ Ошибка сети или бэкенда:\n`{str(e)}`\n\nМодель не ответила. Убедитесь, что сервер {config.ENGINE.upper()} запущен и порт {config.PORT} доступен.")
