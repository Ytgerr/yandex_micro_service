import streamlit as st
import requests
import json

BACKEND_URL = "http://api:8000"

st.sidebar.title("Навигация")
mode = st.sidebar.radio("Режим", ["Чат", "Администрирование"])

if mode == "Чат":
    st.title("чат")
    st.write("Введите ваш запрос:")

    if "dialog" not in st.session_state:
        st.session_state.dialog = []

    user_input = st.text_area("Ваш вопрос:")
    if st.button("Отправить"):
        if user_input.strip():
            st.session_state.dialog.append({"role": "user", "text": user_input})
            payload = {
                "dialog": st.session_state.dialog,
            }
            r = requests.post(f"{BACKEND_URL}/answer", json=payload)
            if r.status_code == 200:
                answer = r.json().get("answer", "Нет ответа")
                st.session_state.dialog.append({"role": "assistant", "text": answer})
            else:
                st.error(f"Ошибка: {r.text}")

    for msg in st.session_state.dialog:
        role = "👤 Пользователь" if msg["role"] == "user" else "🤖 Модель"
        st.markdown(f"**{role}:** {msg['text']}")

elif mode == "Администрирование":
    st.title("Администрирование индексов")

    action = st.selectbox("Выберите действие", [
        "Проверить health",
        "Список индексов",
        "Загрузить документы",
        "Получить документы",
        "Удалить документы"
    ])

    if action == "Проверить health":
        if st.button("Проверить"):
            r = requests.get(f"{BACKEND_URL}/health")
            st.write(r.json())

    elif action == "Список индексов":
        if st.button("Получить список"):
            r = requests.get(f"{BACKEND_URL}/indexes")
            st.write(r.json())

    elif action == "Загрузить документы":
        idx = st.text_input("Имя индекса")
        docs = st.text_area("Документы (JSON)", "[]")
        if st.button("Загрузить"):
            payload = {
                "index_name": idx,
                "documents": json.loads(docs)
            }
            r = requests.post(f"{BACKEND_URL}/indexes/{idx}/documents", json=payload)
            st.write(r.json())

    elif action == "Получить документы":
        idx = st.text_input("Имя индекса")
        if st.button("Получить"):
            r = requests.get(f"{BACKEND_URL}/indexes/{idx}/documents")
            st.write(r.json())

    elif action == "Удалить документы":
        idx = st.text_input("Имя индекса")
        ids = st.text_area("IDs документов (JSON-массив)", "[]")
        if st.button("Удалить"):
            docs_ids = json.loads(ids)
            r = requests.delete(f"{BACKEND_URL}/indexes/{idx}/documents")
            st.write(r.json())
