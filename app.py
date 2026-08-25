import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 页面基本配置
st.set_page_config(page_title="中国宏观经济指标看板", layout="wide", page_icon="📊")
st.title("🇨🇳 中国宏观经济指标动态看板")
st.caption("数据每日通过 GitHub Actions + AkShare 自动刷新")

# 2. 读取 GitHub 仓库本地生成的最新数据 (防止网络波动，直接读本地相对路径)
@st.cache_data(ttl=3600) # 缓存1小时，避免重复加载
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"无法读取数据 {file_path}: {e}")
        return None

pmi_df = load_data("data/china_pmi.csv")
cpi_df = load_data("data/china_cpi.csv")
gdp_df = load_data("data/china_gdp.csv")

# 🌟 布局：核心指标卡片 (以最新的 PMI 为例)
if pmi_df is not None:
    st.subheader("📌 核心经济雷达")
    latest_pmi = pmi_df.iloc[0] # 假设最新一行在顶部，根据实际AkShare结构调整
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="最新制造业 PMI", value=f"{latest_pmi.get('制造业-指数', 'N/A')}%")
    with col2:
        st.metric(label="非制造业 PMI", value=f"{latest_pmi.get('非制造业-指数', 'N/A')}%")
    with col3:
        st.metric(label="综合 PMI", value=f"{latest_pmi.get('综合PMI输出指数-指数', 'N/A')}%")

st.divider()

# 📊 布局：动态图表呈现
tab1, tab2, tab3 = st.tabs(["📈 PMI 趋势", "🛒 核心通胀 (CPI)", "🧱 经济增长 (GDP)"])

with tab1:
    if pmi_df is not None:
        st.markdown("### 采购经理人指数 (PMI) 走势")
        
        # 克隆一份数据防污染
        plot_pmi_df = pmi_df.copy()
        
        # 💡 核心修复：清洗中文字符 (例如将 "2023年07月份" 转换为 "2023-07")
        try:
            # 兼容带有 “年” 和 “月份/月” 的中文字符串
            plot_pmi_df['月份'] = plot_pmi_df['月份'].astype(str) \
                                                    .str.replace('年', '-', regex=False) \
                                                    .str.replace('月份', '', regex=False) \
                                                    .str.replace('月', '', regex=False)
            
            # 使用 format="%Y-%m" 进行精准转换，异常数据强制转为 NaT 避免崩溃
            plot_pmi_df['月份'] = pd.to_datetime(plot_pmi_df['月份'], format="%Y-%m", errors='coerce')
            
            # 过滤掉无法解析的脏数据
            plot_pmi_df = plot_pmi_df.dropna(subset=['月份'])
            # 按时间正序排列（有些接口默认倒序，画折线图会错乱）
            plot_pmi_df = plot_pmi_df.sort_values('月份')
            
        except Exception as date_err:
            st.error(f"日期字段清洗失败，请检查源数据格式。错误原因: {date_err}")

        # 确保清洗成功后再画图
        if not plot_pmi_df.empty:
            # 绘制折线图
            fig_pmi = px.line(plot_pmi_df, x='月份', y=['制造业-指数', '非制造业-指数'], 
                              labels={'value': '指数 (%)', 'variable': '指标分类'},
                              title="中国 PMI 历史走势（50% 为荣枯线）")
            fig_pmi.add_hline(y=50, line_dash="dash", line_color="red", annotation_text="荣枯线")
            st.plotly_chart(fig_pmi, use_container_width=True)
        else:
            st.warning("⚠️ 过滤后暂无合法的日期数据用于绘图")


with tab2:
    if cpi_df is not None:
        st.markdown("### 居民消费价格指数 (CPI) 走势")
        # 请根据您抓取到的实际 cpi_df 字段名调整 x 和 y
        st.dataframe(cpi_df.head(10), use_container_width=True) 

with tab3:
    if gdp_df is not None:
        st.markdown("### 季度 GDP 同比增长率")
        st.dataframe(gdp_df.head(10), use_container_width=True)
