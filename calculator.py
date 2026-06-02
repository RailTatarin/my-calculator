import streamlit as st
import streamlit.components.v1 as components

# Настройка страницы браузера
st.set_page_config(page_title="Калькулятор (X * Y - 1%)", page_icon="🧮")

st.title("🧮 Калькулятор формулы")
st.markdown("Формула: **(X × Y) - 1%**")
st.write("---")

# Поля ввода данных
x = st.number_input("Введите первое число (X):", value=526.44, format="%.4f")
y = st.number_input("Введите второе число (Y):", value=75.66, format="%.4f")

# Вычисления
product = x * y
# Округляем до целого числа, чтобы убрать точку и копейки
result_int = round(product * 0.99)
result_str = str(result_int)

st.write("---")
st.subheader("📊 Результаты расчётов:")

# Отображение результатов
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Результат умножения (X × Y)", value=f"{product:,.2f}")
with col2:
    st.metric(label="Итог минус 1% (без точек)", value=f"{result_int}")

st.write("---")

# Секция копирования
st.subheader("📋 Копирование результата:")

# Кнопка со встроенным JavaScript для работы с буфером обмена
if st.button("📋 КОПИРОВАТЬ РЕЗУЛЬТАТ", use_container_width=True, type="primary"):
    # Внедряем JS-скрипт, который копирует значение в буфер обмена пользователя
    js_code = f"""
    <script>
    navigator.clipboard.writeText("{result_str}").then(() => {{
        parent.postMessage({{type: 'streamlit:set_component_value', value: true}}, '*');
    }});
    </script>
    """
    components.html(js_code, height=0, width=0)
    st.success(f"🎉 Число {result_str} успешно скопировано в буфер обмена!")
