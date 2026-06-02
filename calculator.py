import streamlit as st
import streamlit.components.v1 as components

# Настройка страницы браузера
st.set_page_config(page_title="Калькулятор (X * Y - 1%)", page_icon="🧮")

st.title("🧮 Калькулятор формулы")
st.markdown("Формула: **(X × Y) - 1%**")
st.write("---")

# Инициализация сессионных переменных для хранения вставленных значений
if "x_value" not in st.session_state:
    st.session_state.x_value = ""
if "y_value" not in st.session_state:
    st.session_state.y_value = ""

# --- БЛОК ВВОДА ЧИСЛА X ---
st.markdown("**Первое число (X):**")
col_x_input, col_x_btn = st.columns([4, 1])  # Соотношение ширины поля и кнопки

with col_x_input:
    # Текстовое поле синхронизировано со внутренним состоянием
    x_input = st.text_input(
        "Поле ввода X", 
        value=st.session_state.x_value, 
        placeholder="Например: 526.44", 
        label_visibility="collapsed"
    )

with col_x_btn:
    # Большая кнопка Вставить
    paste_x = st.button("📋 ВСТАВИТЬ", key="btn_paste_x", use_container_width=True)

# --- БЛОК ВВОДА ЧИСЛА Y ---
st.markdown("**Второе число (Y):**")
col_y_input, col_y_btn = st.columns([4, 1])

with col_y_input:
    y_input = st.text_input(
        "Поле ввода Y", 
        value=st.session_state.y_value, 
        placeholder="Нажмите Enter для 75.66, если поле пустое", 
        label_visibility="collapsed"
    )

with col_y_btn:
    paste_y = st.button("📋 ВСТАВИТЬ", key="btn_paste_y", use_container_width=True)


# --- СКРИПТЫ ДЛЯ ЧТЕНИЯ БУФЕРА ОБМЕНА (JavaScript) ---
# Если нажата кнопка вставить для X
if paste_x:
    js_paste_x = """
    <script>
    navigator.clipboard.readText().then(text => {
        // Передаем текст из буфера обратно в Streamlit
        parent.postMessage({type: 'streamlit:set_component_value', value: text}, '*');
    }).catch(err => {
        console.error('Ошибка доступа к буферу:', err);
    });
    </script>
    """
    # Компонент принимает значение из JS и сохраняет его
    res_x = components.html(js_paste_x, height=0, width=0)
    st.info("🔄 Считывание буфера... Нажмите кнопку еще раз, если значение не обновилось.")
    
# Если нажата кнопка вставить для Y
if paste_y:
    js_paste_y = """
    <script>
    navigator.clipboard.readText().then(text => {
        parent.postMessage({type: 'streamlit:set_component_value', value: text}, '*');
    });
    </script>
    """
    res_y = components.html(js_paste_y, height=0, width=0)
    st.info("🔄 Считывание буфера...")


# Логика обработки ручного или автоматического ввода данных
x = None
y = None
error_msg = ""

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

# Расчет
if x is not None and y is not None and not error_msg:
    product = x * y
    result_int = round(product * 0.99)
    result_str = str(result_int)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Результат умножения (X × Y)", value=f"{product:,.2f}")
    with col2:
        st.metric(label="Итог минус 1% (без точек)", value=f"{result_int}")

    st.write("---")
    st.subheader("📋 Копирование результата:")

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
    st.info("👋 Пожалуйста, введите или вставьте число X, чтобы увидеть результат расчета.")
