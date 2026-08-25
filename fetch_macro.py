import os
import pandas as pd
import akshare as ak

def update_china_macro_data():
    print("🚀 开始抓取中国宏观经济指标...")
    
    # 创建存放数据的目录
    os.makedirs("data", exist_ok=True)
    
    # 1. 抓取中国 PMI 数据
    try:
        print("📊 正在获取 PMI 数据...")
        macro_china_pmi_df = ak.macro_china_pmi()
        macro_china_pmi_df.to_csv("data/china_pmi.csv", index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"❌ PMI 抓取失败: {e}")

    # 2. 抓取中国 CPI 数据
    try:
        print("📊 正在获取 CPI 数据...")
        macro_china_cpi_df = ak.macro_china_cpi()
        macro_china_cpi_df.to_csv("data/china_cpi.csv", index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"❌ CPI 抓取失败: {e}")

    # 3. 抓取中国 GDP 季度数据
    try:
        print("📊 正在获取 GDP 数据...")
        macro_china_gdp_yoy_df = ak.macro_china_gdp_yearly()
        macro_china_gdp_yoy_df.to_csv("data/china_gdp.csv", index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"❌ GDP 抓取失败: {e}")

    print("✅ 所有数据刷新完成并已保存至 /data 目录！")

if __name__ == "__main__":
    update_china_macro_data()
