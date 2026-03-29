import akshare as ak
import streamlit as st
import pandas as pd
import datetime
st.set_page_config(layout="wide")
# ===== 工具函数 =====
def format_symbol(code):
    if code.startswith("6"):
        return "SH" + code
    else:
        return "SZ" + code
def safe_display(df, name, chart=None):
    try:
        if df is None:
            st.warning(f"{name} 获取失败（返回为空）")
            return

        if df.empty:
            st.warning(f"{name} 暂无数据")
            return

        st.markdown(f"### {name}")

        # ===== 冻结前两列（关键）=====
        if df.shape[1] >= 2:
            column_config = {
                df.columns[0]: st.column_config.Column(pinned="left"),
                df.columns[1]: st.column_config.Column(pinned="left"),
            }
        else:
            column_config = {}

        # ===== 表格展示（可冻结列）=====
        st.data_editor(
            df,
            use_container_width=True,
            disabled=True,  # 只读模式
            column_config=column_config,
            height=400
        )

        # ===== 没有图表需求 =====
        if chart is None:
            return

        # 至少要两列才能画图
        if df.shape[1] < 2:
            st.info(f"{name} 数据列不足，无法绘制图表")
            return

        # ===== 图表处理 =====
        try:
            df_plot = df.copy()
            df_plot = df_plot.set_index(df_plot.columns[0])
        except Exception:
            st.info(f"{name} 无法设置索引，跳过图表")
            return

        # 只保留数值列（关键！）
        df_plot = df_plot.select_dtypes(include="number")

        if df_plot.empty:
            st.info(f"{name} 没有可用于绘图的数值列")
            return

        # ===== 绘图 =====
        if chart == "line":
            st.line_chart(df_plot)
        elif chart == "bar":
            st.bar_chart(df_plot)

    except Exception as e:
        st.warning(f"{name} 展示失败")
        st.text(str(e))
# ===== 安全获取函数 =====
def safe_fetch(func, name, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.warning(f"{name} 获取失败")
        st.text(str(e))
        return None
def get_last_trade_date_str(today=None):
    """
    获取最近的交易日，返回 YYYYMMDD 字符串格式
    如果 today 是交易日，返回 today
    如果 today 不是交易日，返回上一个交易日
    参数:
        today: datetime.date 或 None（默认今天）
    返回:
        最近交易日字符串，格式 "YYYYMMDD"
    """
    if today is None:
        today = datetime.date.today()

    # 获取交易日历
    df = ak.tool_trade_date_hist_sina()
    df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date

    # 筛选出 <= today 的交易日
    df = df[df["trade_date"] <= today]

    # 最近交易日
    last_trade_date = df["trade_date"].iloc[-1]

    # 转成 YYYYMMDD 字符串
    return last_trade_date.strftime("%Y%m%d")
def get_last_year_1231():
    """
    返回上一年的12月31日，格式YYYYMMDD
    """
    today = datetime.date.today()
    last_year = today.year - 1
    return f"{last_year}1231"
# 英文 → 中文映射
mapping = {
        "name": "公司名称",
        "symbol": "股票代码",
        "current": "当前价格",
        "percent": "涨跌幅",
        "chg": "涨跌额",
        "market_capital": "总市值",
        "float_market_capital": "流通市值",
        "turnover_rate": "换手率",
        "pe_ttm": "市盈率(TTM)",
        "pb": "市净率",
        "volume": "成交量",
        "amount": "成交额",
        "amplitude": "振幅",
        "high": "最高价",
        "low": "最低价",
        "open": "开盘价",
        "last_close": "昨收价",
        "org_id": "公司ID",
        "org_name_cn": "公司中文全称",
        "org_short_name_cn": "公司中文简称",
        "org_name_en": "公司英文全称",
        "org_short_name_en": "公司英文简称",
        "main_operation_business": "主营业务",
        "operating_scope": "经营范围",
        "district_encode": "地区编码",
        "provincial_name": "省份",
        "org_cn_introduction": "公司简介",
        "legal_representative": "法定代表人",
        "chairman": "董事长",
        "general_manager": "总经理",
        "secretary": "董事会秘书",
        "established_date": "成立日期",
        "listed_date": "上市日期",
        "reg_asset": "注册资本",
        "staff_num": "员工人数",
        "telephone": "联系电话",
        "fax": "传真",
        "email": "邮箱",
        "postcode": "邮编",
        "org_website": "公司官网",
        "reg_address_cn": "注册地址（中文）",
        "reg_address_en": "注册地址（英文）",
        "office_address_cn": "办公地址（中文）",
        "office_address_en": "办公地址（英文）",
        "currency": "货币",
        "currency_encode": "货币编码",
        "actual_controller": "实际控制人",
        "classi_name": "公司类型",
        "pre_name_cn": "曾用名",
        "executives_nums": "高管人数",
        "actual_issue_vol": "实际发行量",
        "issue_price": "发行价格",
        "actual_rc_net_amt": "实际募集资金净额",
        "pe_after_issuing": "发行后市盈率",
        "online_success_rate_of_issue": "网上中签率",
        "affiliate_industry": "所属行业"
    }
def show_home():
    st.title("📊 股票信息分析面板")
    st.markdown("请选择功能👇")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 个股分析"):
            st.session_state.page = "stock"
            st.rerun()  # ⭐ 关键！
        if st.button("📅 公司事件"):
            st.session_state.page = "event"
            st.rerun()  # ⭐ 关键！
        if st.button("📌 质押"):
            st.session_state.page = "pledge"
            st.rerun()
        if st.button("⏸️ 停复牌"):
            st.session_state.page = "suspend"
            st.rerun()
    with col2:

        if st.button("🆕 IPO受益股"):
            st.session_state.page = "ipo_benefit"
            st.rerun()
        if st.button("🏢 机构调研"):
            st.session_state.page = "institution_research"
            st.rerun()
        if st.button("💸 商誉减值"):
            st.session_state.page = "goodwill"
            st.rerun()
def show_stock_page():
    st.title("📈 个股分析")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()  # ⭐ 关键！
    # ===== 这里放你原来的代码 =====
    # ===== 输入区域 =====
    symbol_input = st.text_input("请输入股票代码（如：600000）", "600000")

    if st.button("开始分析"):

        symbol_xq = format_symbol(symbol_input)  # 雪球
        symbol_em = symbol_input                 # 东方财富

        # ===== 上半部分：左右布局 =====
        col1, col2 = st.columns([1, 2])

        # ===== 左侧：基本信息 =====
        with col1:
            st.subheader("📋 个股基本信息")

            try:
                df = ak.stock_individual_basic_info_xq(symbol=symbol_xq)

                df["item"] = df["item"].map(lambda x: mapping.get(x, x))

                for i in range(len(df)):
                    st.write(f"**{df.iloc[i,0]}：** {df.iloc[i,1]}")

            except Exception as e:
                st.error(f"基本信息获取失败: {e}")

        # ===== 右侧：简单行情（可扩展K线） =====
        with col2:
            st.subheader("📊 财务分析")
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 成长能力",
                "💰 估值分析",
                "🧮 杜邦分析",
                "🏢 公司规模"
            ])
            with tab1:
                df_growth = safe_fetch(
                    ak.stock_zh_growth_comparison_em,
                    "成长能力",
                    symbol=symbol_xq
                )
                safe_display(df_growth, "成长能力",)

            with tab2:
                df_val = safe_fetch(
                    ak.stock_zh_valuation_comparison_em,
                    "估值分析",
                    symbol=symbol_xq
                )
                safe_display(df_val, "估值分析")

            with tab3:
                df_dupont = safe_fetch(
                    ak.stock_zh_dupont_comparison_em,
                    "杜邦分析",
                    symbol=symbol_xq
                )
                safe_display(df_dupont, "杜邦分析")

            with tab4:
                df_scale = safe_fetch(
                    ak.stock_zh_scale_comparison_em,
                    "公司规模",
                    symbol=symbol_xq
                )
                safe_display(df_scale, "公司规模")

        st.divider()
def show_event_page():
    st.title("📅 公司事件")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()  # ⭐ 关键！
    # ===== 你刚写的事件功能 =====
    st.subheader("📅 公司事件查询")

    # ===== 日期选择 =====
    selected_date = st.date_input(
        "选择日期",
        value=get_last_trade_date_str()
    )

    # ===== 同步用户选择 =====
    st.session_state.selected_date = selected_date

    # ===== 查询按钮 =====
    if st.button("查询公司事件"):

        try:
            # 转字符串（AKShare需要 YYYYMMDD）
            date_str = selected_date.strftime("%Y%m%d")

            df_event = ak.stock_gsrl_gsdt_em(date=date_str)

            if df_event is None or df_event.empty:
                st.warning("该日期暂无公司事件")
            else:
                safe_display(df_event, f"{date_str} 公司事件")

        except Exception as e:
            st.error("公司事件获取失败")
            st.text(str(e))
def show_ipo_benefit_page():
    st.title("💹 IPO受益股分析")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()  # 返回主页

    st.subheader("📊 查询近期IPO受益股")

    if st.button("查询IPO受益股"):
        df_ipo = safe_fetch(
            ak.stock_ipo_benefit_ths,
            "IPO受益股"
        )

        if df_ipo is None or df_ipo.empty:
            st.warning("暂无IPO受益股数据")
        else:
            # 直接展示，无需映射
            safe_display(df_ipo, "IPO受益股", chart="bar")
def show_institution_research_page():
    st.title("🏦 机构调研统计")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()  # 返回主页

    st.subheader("📊 查询机构调研统计数据")

    # ===== 用户选择开始日期 =====
    start_date = st.date_input(
        "选择开始查询日期",
        value=datetime.date.today() - datetime.timedelta(days=30)
    )
    date_str = start_date.strftime("%Y%m%d")  # AKShare 需要 YYYYMMDD 格式

    if st.button("查询机构调研"):
        df_jgdy = safe_fetch(
            ak.stock_jgdy_tj_em,
            "机构调研",
            date=date_str
        )

        if df_jgdy is None or df_jgdy.empty:
            st.warning("暂无机构调研数据")
        else:
            # 删除“序号”列，不显示
            if "序号" in df_jgdy.columns:
                df_jgdy = df_jgdy.drop(columns=["序号"])
            # 直接展示，无需字段映射
            safe_display(df_jgdy, "机构调研")
def show_goodwill_impairment_page():
    st.title("💸 商誉减值预期明细")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("📊 查询商誉减值预期明细（上一年12月31日）")

    # 上一年的12月31日
    date_str = get_last_year_1231()

    # 获取数据
    df = safe_fetch(
        ak.stock_sy_yq_em,
        "商誉减值预期明细",
        date=date_str
    )

    # 数据检查
    if df is None or df.empty:
        st.warning("暂无商誉减值预期数据")
        return
    # 删除“序号”列，避免最左边显示
    if "序号" in df.columns:
        df = df.drop(columns=["序号"])
    # 安全显示
    safe_display(df, f"商誉减值预期明细（{date_str}）")
def show_suspend_resume_page():
    st.title("⏸️ 停复牌公告）")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("📊 查询停复牌公告")

    # 获取数据
    df = safe_fetch(
        ak.stock_tfp_em,
        "停复牌公告",
        date=get_last_trade_date_str()
    )

    # 数据检查
    if df is None or df.empty:
        st.warning("暂无停复牌公告")
        return

    # 删除“序号”列（如果有）
    if "序号" in df.columns:
        df = df.drop(columns=["序号"])

    # 显示表格
    safe_display(df, "停复牌公告")
def show_pledge_page():
    st.title("📌 个股质押分析")

    if st.button("⬅️ 返回主页"):
        st.session_state.page = "home"
        st.rerun()

    st.subheader("📊 查询个股质押相关数据")
    today = datetime.date.today()
    today_str = today.strftime("%Y%m%d")
    # Tab 页面
    tab1, tab2, tab3 = st.tabs([
        "上市公司质押比例",
        "重要股东股权质押明细",
        "上市行业质押比例"
    ])

    with tab1:
        df_ratio = safe_fetch(ak.stock_gpzy_pledge_ratio_em, "上市公司质押比例",date=get_last_trade_date_str())
        safe_display(df_ratio, "上市公司质押比例")

    with tab2:
        df_detail = safe_fetch(ak.stock_gpzy_pledge_ratio_detail_em, "重要股东股权质押明细")
        safe_display(df_detail, "重要股东股权质押明细")

    with tab3:
        df_industry = safe_fetch(ak.stock_gpzy_industry_data_em, "上市行业质押比例")
        safe_display(df_industry, "上市行业质押比例")
if "page" not in st.session_state:
    st.session_state.page = "home"
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "stock":
    show_stock_page()
elif st.session_state.page == "event":
    show_event_page()
elif st.session_state.page == "ipo_benefit":
    show_ipo_benefit_page()
elif st.session_state.page == "institution_research":
    show_institution_research_page()
elif st.session_state.page == "pledge":
    show_pledge_page()
elif st.session_state.page == "goodwill":
    show_goodwill_impairment_page()
elif st.session_state.page == "suspend":
    show_suspend_resume_page()