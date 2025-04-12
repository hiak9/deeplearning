import get
import show
import streamlit as st


table = show.input_table()
info, submit_button = table.show_table()

if submit_button:
    dblp = get.DBLP()
    entries, if_find = dblp.get_name(info['name'])
    # for entry in entries:
    #     title = entry.find('title')
    #     authors = entry.find_all('author')
    #     year = entry.find('year')
    #     ee_tags = entry.find_all('ee')

    #     st.text(f"标题: {title.text if title else 'N/A'}")
    #     st.text(f"作者: {[a.text for a in authors]}")
    #     st.text(f"年份: {year.text if year else 'N/A'}")
    #     st.text(f"链接: {[ee.text for ee in ee_tags]}")
    #     st.text('-' * 40)

    show = show.show_data()
    show.show_dblp(entries, info['name'], if_find=if_find)