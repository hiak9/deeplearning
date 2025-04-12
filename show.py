import streamlit as st

class show_data:
    def __init__(self) -> None:
        pass

    def show_dblp(self, entries, name, if_find=False):
        st.title(f"📚 {name} 的论文列表")

        st.write(f"共找到 {len(entries)} 篇论文：")

        for i, entry in enumerate(entries, start=1):
            title = entry.find('title')
            authors = entry.find_all('author')
            year = entry.find('year')
            ee_tags = entry.find_all('ee')

            with st.container():
                st.markdown(f"### {i}. {title.text if title else 'N/A'}")
                st.markdown(f"👥 **作者**: {', '.join([a.text for a in authors]) if authors else 'N/A'}")
                st.markdown(f"📅 **年份**: {year.text if year else 'N/A'}")

                if ee_tags:
                    st.markdown("🔗 **链接：**")
                    for idx, ee in enumerate(ee_tags, 1):
                        st.markdown(f"- [{ee.text}]({ee.text})")
                else:
                    st.markdown("🔗 **链接：** N/A")

                st.markdown("---")

class input_table:
    def __init__(self):
        pass

    def show_table(self):
        info = {}

        with st.form(key='table'):
            info['name'] = st.text_input(label='name')

            submit_button = st.form_submit_button(label='submit')

        return info, submit_button

