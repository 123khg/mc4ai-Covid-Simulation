import streamlit as st, pygame as pg, numpy as np, matplotlib.pyplot as plt, time

st.set_page_config(page_title="Simulation", layout="wide")
st.title('This is a title')
st.header('This is a header')
st.subheader('This is a subheader')
st.caption('This is a caption')
st.text('This is a text')
st.code('x = 5\nprint(x)')
st.latex('x^2 + \sqrt{y} = \pi')
text = st.text_input('Text input', 'Default')
number = st.number_input('Number input')
textarea = st.text_area('Text area', '''Hello
COTAI''')

if st.button('OK'):
  st.write('text content:', text)
  st.write('number content:', number)
  st.write('text area content:', textarea)
check = st.checkbox('Boy')
  
radio = st.radio('Radio', ('Option 1', {"bana", 2, True}, 'Option 3'), horizontal=False)
if st.button('Yass'):
  st.write('Check box:', check)
  st.write('Radio:', radio, type(radio))

with st.sidebar:
    radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")
    
with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))
tab1, tab2, tab3 = st.tabs(["Cat", "2", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    
st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')

st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a (\frac{1-r^{n}}{1-r})
    ''')

st.write("This is some text.")

b = st.slider("This is a slider", 0, 100, (25, 75))

st.write("---")

st.write(f"This text is between the horizontal rules. {b}")