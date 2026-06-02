import streamlit as st
import streamlit.components.v1 as components

# Настройка страницы браузера
st.set_page_config(page_title="Калькулятор Parity", page_icon="🧮")

st.title("🧮 Калькулятор Parity")
st.markdown("Формула расчёта: **(Сумма USDT × Комиссия Parity) - 1%**")
st.write("---")

# Специальный стиль для увеличения размера текста в полях
st.markdown("""
    <style>
    div[data-baseweb="input"] {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Поля ввода с вашими новыми названиями
x_input = st.text_input("сумма в USDT (к получению):", value="", placeholder="Вставь число")
y_input = st.text_input("комиссия Parity:", value="", placeholder="Оставь пустым для 75.66")

# Переменные для вычислений
x = None
y = None
error_msg = ""

# Обработка введенных данных
if x_input:
    try:
        x = float(x_input.replace(',', '.').strip())
    except ValueError:
        error_msg = "❌ Ошибка: Введите корректное число в поле суммы USDT."

if y_input:
    try:
        y = float(y_input.replace(',', '.').strip())
    except ValueError:
        error_msg = "❌ Ошибка: Введите корректное число в поле комиссии Parity."
elif x is not None:
    # Если сумма введена, а комиссия пустая — подставляем значение по умолчанию
    y = 75.66

st.write("---")
st.subheader("📊 Результаты расчётов:")

# Расчет и вывод результатов
if x is not None and y is not None and not error_msg:
    product = x * y
    result_int = round(product * 0.99)
    result_str = str(result_int)

    # Отображение результатов в красивых карточках
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Полная сумма (без вычета 1%)", value=f"{product:,.2f}")
    with col2:
        st.metric(label="Итог минус 1% (без точек)", value=f"{result_int}")

    st.write("---")
    st.subheader("📋 Копирование итогового результата:")

    # Кнопка копирования
    if st.button("📋 КОПИРОВАТЬ ИТОГ", use_container_width=True, type="primary"):
        js_code = f"""
        <script>
        navigator.clipboard.writeText("{result_str}").then(() => {{
            parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
        }});
        </script>
        """
        components.html(js_code, height=0, width=0)
        st.success(f"🎉 Число {result_str} успешно скопировано в буфер обмена!")

elif error_msg:
    st.error(error_msg)
else:
    st.info("👋 Пожалуйста, вставьте сумму в USDT, чтобы увидеть готовый расчет.")
