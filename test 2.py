import numpy as np, streamlit as st

a = [["a", True, 2],
    ["b", True, 1],
    ["a", False,3]]
# print(np.where("a" in a[:, 0])[0])
# if "val" not in st.session_state:
#     st.session_state.val = True
#     st.session_state.c = 0
# while True:
#     b = st.slider("B", 0, 100, 0, key =f"{st.session_state.c}")
#     st.write(f"{b}")
#     st.write(f"{st.session_state.c}")
#     st.session_state.c+= 1
test = np.array([["bruh", 0],
               ["lmao", 2]])[:, 1]
print(test.astype(float))
print(np.array(a)[test[:, 1].astype(float)])