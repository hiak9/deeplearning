import get
import show
import streamlit as st
import requests
from bs4 import BeautifulSoup

# 输入作者名
table = show.input_table()
info, submit_button = table.show_table()

if submit_button:
    dblp = get.DBLP()
    candidates = dblp.get_candidate_authors(info['name'])

    if not candidates:
        st.warning("未找到任何匹配的作者")
    else:
        author_names = [c['author'] for c in candidates]

        # 让用户选择作者，并记住选择
        st.selectbox(
            "请选择最匹配的作者",
            author_names,
            key="selected_author",  # 使用 session_state 记录值
        )

# 判断用户是否已经选择了作者（selectbox 会记录在 session_state 中）
if "selected_author" in st.session_state:
    selected = st.session_state["selected_author"]

    # 根据作者名找到对应的 URL
    dblp = get.DBLP()
    candidates = dblp.get_candidate_authors(selected)
    selected_url = [c['url'] for c in candidates if c['author'] == selected]
    
    if selected_url:
        author_url = selected_url[0] + ".xml"
        author_response = requests.get(author_url, headers=dblp.headers)
        soup = BeautifulSoup(author_response.text, 'xml')
        entries = soup.find_all('r')

        show_ui = show.show_data()
        show_ui.show_dblp(entries, selected, if_find=True)



