import streamlit as st
import streamlit.components.v1 as components

# Настройка страницы браузера
st.set_page_config(page_title="Калькулятор (X * Y - 1%)", page_icon="🧮")

st.title("🧮 Калькулятор формулы")
st.markdown("Формула: **(X × Y) - 1%**")
st.write("---")

# Специальный стиль, чтобы поля были визуально крупными и удобными для тапа пальцем
st.markdown("""
    <style>
    div[data-baseweb="input"] {
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Используем текстовые поля. При клике на них на телефоне зажмите поле пальцем, 
# либо посмотрите на панель подсказок клавиатуры — там появится кнопка "Вставить" (Paste)
x_input = st.text_input("Вставьте или введите первое число (X):", value="", placeholder="Нажмите сюда и выберите 'Вставить'")
y_input = st.text_input("Вставьте или введите второе число (Y):", value="", placeholder="Оставьте пустым для 75.66")

# Переменные для вычислений
x = None
y = None
error_msg = ""

# Обработка данных с очисткой от пробелов и заменой запятых
if x_input:
    try:
        x = float(x_input.replace(',', '.').strip())
    except ValueError:
        error_msg = "❌ Ошибка в поле X: Введите корректное число."

if y_input:
    try:
        y = float(y_input.replace(',', '.').strip())
    except ValueError:
        error_msg = "❌ Ошибка в поле Y: Введите корректное число."
elif x is not None:
    y = 75.66

st.write("---")
st.subheader("📊 Результаты расчётов:")

# Если данные введены корректно — считаем
if x is not None and y is not None and not error_msg:
    product = x * y
    result_int = round(product * 0.99)
    result_str = str(result_int)

    # Отображение результатов
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Результат умножения (X × Y)", value=f"{product:,.2f}")
    with col2:
        st.metric(label="Итог минус 1% (без точек)", value=f"{result_int}")

    st.write("---")
    st.subheader("📋 Копирование результата:")

    # Кнопка копирования (она работает отлично на всех устройствах, так как запись в буфер разрешена)
    if st.button("📋 КОПИРОВАТЬ РЕЗУЛЬТАТ", use_container_width=True, type="primary"):
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
    st.info("👋 Пожалуйста, вставьте число X, чтобы увидеть расчет.")
