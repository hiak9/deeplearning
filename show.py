import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

sort_index = {
    '正序':'asc',
    '倒序':'desc'
}

class show_data:
    def __init__(self) -> None:
        pass

    def show_dblp(self, entries, name, if_find=False, sort_order="desc"):
        # 创建标签页
        tab1, tab2, tab3 = st.tabs(["📊 发表趋势", "👥 合作者分析", "📚 论文列表"])
        
        with tab1:
            self.show_trends(entries, name)
        
        with tab2:
            self.show_coauthors(entries, name)
        
        with tab3:
            self.show_papers(entries, name, if_find, sort_order)

    def show_trends(self, entries, name):
        st.header("📊 发表趋势分析")
        
        # 收集论文数据
        papers_data = []
        for entry in entries:
            year_tag = entry.find('year')
            title_tag = entry.find('title')
            venue_tag = entry.find('venue')
            publication_tag = entry.find('booktitle') or entry.find('journal')
            
            if year_tag:
                paper = {
                    "year": int(year_tag.text),
                    "title": title_tag.text if title_tag else "未知",
                    "venue": venue_tag.text if venue_tag else "未知",
                    "publication": publication_tag.text if publication_tag else "未知"
                }
                papers_data.append(paper)
        
        if papers_data:
            df = pd.DataFrame(papers_data)
            
            # 每年发表论文数量柱状图
            yearly_counts = df.groupby('year').size().reset_index(name='count')
            
            fig1 = px.bar(
                yearly_counts, 
                x='year', 
                y='count',
                labels={'count': '论文数量', 'year': '年份'},
                title=f"{name} 每年发表论文数量"
            )
            
            # 添加趋势线
            fig1.add_trace(
                go.Scatter(
                    x=yearly_counts['year'], 
                    y=yearly_counts['count'],
                    mode='lines',
                    name='趋势线',
                    line=dict(color='red')
                )
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # 累计发表数量折线图
            yearly_counts['cumulative'] = yearly_counts['count'].cumsum()
            
            fig2 = px.line(
                yearly_counts, 
                x='year', 
                y='cumulative',
                labels={'cumulative': '累计论文数量', 'year': '年份'},
                title=f"{name} 累计发表论文数量"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # 发表场所分布
            if 'publication' in df.columns:
                # 提取前10个最常发表的会议/期刊
                publication_counts = df['publication'].value_counts()
                top_venues = publication_counts.head(10).reset_index()
                top_venues.columns = ['会议/期刊', '论文数量']
                
                fig3 = px.bar(
                    top_venues,
                    x='会议/期刊',
                    y='论文数量',
                    title=f"{name} 的Top 10发表场所",
                    color='会议/期刊'
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # 按发表场所的饼图
                # 将出现次数少于2的合并为"其他"类别
                threshold = 2
                other_count = publication_counts[publication_counts < threshold].sum()
                filtered_counts = publication_counts[publication_counts >= threshold]
                if other_count > 0:
                    filtered_counts['其他'] = other_count
                
                fig4 = px.pie(
                    values=filtered_counts.values,
                    names=filtered_counts.index,
                    title=f"{name} 的论文发表场所分布"
                )
                st.plotly_chart(fig4, use_container_width=True)

    def show_coauthors(self, entries, name):
        st.header("👥 合作者分析")
        
        # 收集合作者数据
        coauthors = []
        for entry in entries:
            authors = entry.find_all('author')
            # 如果是合著论文
            if len(authors) > 1:
                paper_authors = [a.text for a in authors]
                # 确保当前作者在论文作者列表中
                if name in paper_authors:
                    for author in paper_authors:
                        if author != name:  # 排除自己
                            coauthors.append(author)
        
        # 计算每个合作者的合作次数
        coauthor_counts = Counter(coauthors)
        
        if coauthors:
            # 显示Top 10合作者
            top_coauthors = coauthor_counts.most_common(10)
            top_coauthors_df = pd.DataFrame(top_coauthors, columns=['合作者', '合作论文数'])
            
            fig5 = px.bar(
                top_coauthors_df,
                x='合作者',
                y='合作论文数',
                title=f"{name} 的Top 10合作者",
                color='合作论文数'
            )
            st.plotly_chart(fig5, use_container_width=True)
            
            # 合作者分布饼图
            if len(coauthor_counts) > 10:
                # 只显示前10名，其他合并为"其他"
                top_n = dict(coauthor_counts.most_common(10))
                others_count = sum(count for author, count in coauthor_counts.items() if author not in top_n)
                
                if others_count > 0:
                    pie_data = top_n.copy()
                    pie_data['其他合作者'] = others_count
                else:
                    pie_data = top_n
            else:
                pie_data = dict(coauthor_counts)
            
            fig6 = px.pie(
                values=list(pie_data.values()),
                names=list(pie_data.keys()),
                title=f"{name} 的合作者分布"
            )
            st.plotly_chart(fig6, use_container_width=True)
            
            # 显示合作者数据表格
            st.subheader("🤝 所有合作者列表")
            all_coauthors_df = pd.DataFrame(coauthor_counts.most_common(), columns=['合作者', '合作论文数'])
            st.dataframe(all_coauthors_df)
        else:
            st.info("未找到合作者数据")

    def show_papers(self, entries, name, if_find=False, sort_order="desc"):
        st.title(f"📚 {name} 的论文列表")

        # 根据年份排序论文
        entries = sorted(entries, key=lambda x: x.find('year').text if x.find('year') else "0", reverse=(sort_order == "desc"))

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
            sort_order = st.selectbox("选择排序方式", ["正序", "倒序"], index=0)
            sort_order = sort_index[sort_order]
            submit_button = st.form_submit_button(label='submit')

        return info, submit_button, sort_order
