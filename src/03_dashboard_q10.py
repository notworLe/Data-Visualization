"""
Buoc 3 (TV6 + TV7): Xay dung Dashboard tuong tac HTML bang Plotly (Chuong 3.4)
va Ban do Choropleth tuong tac cho Cau 5.
Dau ra:
  - outputs/dashboard/q10_dashboard.html (mo truc tiep tren trinh duyet khi thuyet trinh)
  - outputs/dashboard/q05_country_map.html (ban do the gioi tuong tac cho Cau 5)
"""

from __future__ import annotations

import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from style_guide import COLORS

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "Amazon_clean.csv"
KPI_PATH = ROOT / "data" / "processed" / "kpi_metrics.json"
DASH_DIR = ROOT / "outputs" / "dashboard"

ISO3_MAP = {
    "United States": "USA",
    "India": "IND",
    "Canada": "CAN",
    "United Kingdom": "GBR",
    "Australia": "AUS",
}


def build_q5_choropleth(kpis: dict) -> Path:
    co = pd.DataFrame(kpis["q5"]["countries"])
    co["iso3"] = co["Country"].map(ISO3_MAP)
    co["rev_m"] = (co["revenue"] / 1e6).round(2)

    fig = px.choropleth(
        co,
        locations="iso3",
        color="rev_m",
        hover_name="Country",
        hover_data={"iso3": False, "rev_m": ":.2f", "rev_pct": ":.2f", "orders": ":,", "avg_order": ":.2f"},
        color_continuous_scale=["#CCFBF1", "#5EEAD4", "#14B8A6", "#0F766E", "#134E4A"],
        labels={"rev_m": "Doanh thu ($M)", "rev_pct": "Tỉ trọng (%)", "orders": "Số đơn", "avg_order": "AOV ($)"},
        title="Hoa Kỳ dẫn đầu doanh thu ($64,31M · 70,0%), tiếp theo là Ấn Độ ($13,88M · 15,1%)",
    )
    fig.update_geos(showframe=False, showcoastlines=True, coastlinecolor="#CBD5E1", projection_type="natural earth")
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, Arial, sans-serif", color=COLORS["text"]),
        title_font=dict(size=16, color=COLORS["slate"]),
        margin=dict(l=20, r=20, t=65, b=20),
        coloraxis_colorbar=dict(title="Doanh thu ($M)"),
    )
    out = DASH_DIR / "q05_country_map.html"
    fig.write_html(out, include_plotlyjs="cdn")
    return out


def build_q10_dashboard(df: pd.DataFrame, kpis: dict) -> Path:
    q1 = kpis["q1"]
    years = ["Tất cả (2020–2024)"] + [str(y) for y in sorted(df["Year"].unique())]

    # -------------------------------------------------------------------------
    # Bieu do 1: Xu huong doanh thu thang + bo loc theo Nam (dropdown)
    # -------------------------------------------------------------------------
    ym_all = (
        df.groupby(["Year", "YearMonth"])
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"))
        .reset_index()
        .sort_values("YearMonth")
    )
    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=ym_all["YearMonth"],
            y=ym_all["revenue"] / 1e6,
            mode="lines+markers",
            name="Tất cả (2020–2024)",
            line=dict(color=COLORS["teal"], width=2.4),
            marker=dict(size=5, color=COLORS["teal"]),
            customdata=ym_all["orders"],
            hovertemplate="<b>Tháng %{x}</b><br>Doanh thu: $%{y:.2f}M<br>Số đơn: %{customdata:,}<extra></extra>",
        )
    )
    for yr in sorted(df["Year"].unique()):
        sub = ym_all[ym_all["Year"] == yr]
        fig_trend.add_trace(
            go.Scatter(
                x=sub["YearMonth"],
                y=sub["revenue"] / 1e6,
                mode="lines+markers",
                name=str(yr),
                visible=False,
                line=dict(color=COLORS["teal"], width=2.8),
                marker=dict(size=7, color=COLORS["teal"]),
                customdata=sub["orders"],
                hovertemplate="<b>Tháng %{x}</b><br>Doanh thu: $%{y:.2f}M<br>Số đơn: %{customdata:,}<extra></extra>",
            )
        )

    buttons = []
    for i, label in enumerate(years):
        vis = [j == i for j in range(len(years))]
        buttons.append(dict(label=label, method="update", args=[{"visible": vis}]))

    fig_trend.update_layout(
        template="plotly_white",
        title="<b>Xu hướng doanh thu theo tháng</b> — ổn định ~$1,53M/tháng (chọn năm ở góc phải)",
        yaxis=dict(title="Doanh thu ($M)", range=[1.15, 1.78]),
        xaxis=dict(title="Tháng", rangeslider=dict(visible=True, thickness=0.08)),
        updatemenus=[dict(buttons=buttons, direction="down", x=1.0, xanchor="right", y=1.18, yanchor="top", bgcolor="#F8FAFC")],
        margin=dict(l=55, r=20, t=72, b=35),
        height=390,
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # -------------------------------------------------------------------------
    # Bieu do 2: Ban do Choropleth 5 quoc gia
    # -------------------------------------------------------------------------
    co = pd.DataFrame(kpis["q5"]["countries"])
    co["iso3"] = co["Country"].map(ISO3_MAP)
    co["rev_m"] = (co["revenue"] / 1e6).round(2)
    fig_map = px.choropleth(
        co,
        locations="iso3",
        color="rev_m",
        hover_name="Country",
        hover_data={"iso3": False, "rev_m": ":.2f", "rev_pct": ":.2f", "orders": ":,", "avg_order": ":.2f"},
        color_continuous_scale=["#CCFBF1", "#5EEAD4", "#14B8A6", "#0F766E", "#134E4A"],
        labels={"rev_m": "Doanh thu ($M)", "rev_pct": "Tỉ trọng (%)", "orders": "Số đơn", "avg_order": "AOV ($)"},
    )
    fig_map.update_geos(showframe=False, showcoastlines=True, coastlinecolor="#CBD5E1", projection_type="natural earth")
    fig_map.update_layout(
        template="plotly_white",
        title="<b>Phân bố doanh thu theo quốc gia</b> — Mỹ chiếm 70,0% ($64,31M)",
        margin=dict(l=10, r=10, t=55, b=10),
        height=390,
        coloraxis_colorbar=dict(title="$M", thickness=14),
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # -------------------------------------------------------------------------
    # Bieu do 3: Ti le Huy & Tra theo Nhom san pham (Cau 6)
    # -------------------------------------------------------------------------
    cat = pd.DataFrame(kpis["q6"]["by_category"]).iloc[::-1]
    fig_cat = go.Figure()
    fig_cat.add_trace(
        go.Bar(
            y=cat["Category"],
            x=cat["return_pct"],
            name="Trả hàng (%)",
            orientation="h",
            marker_color=[COLORS["red"] if c == "Home & Kitchen" else COLORS["red_soft"] for c in cat["Category"]],
            text=[f"{v:.2f}%" for v in cat["return_pct"]],
            textposition="outside",
            customdata=cat[["returned", "lost_rev"]],
            hovertemplate="<b>%{y}</b><br>Tỉ lệ trả: %{x:.2f}% (%{customdata[0]} đơn)<br>Tổng thất thoát Hủy+Trả: $%{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig_cat.add_trace(
        go.Bar(
            y=cat["Category"],
            x=cat["cancel_pct"],
            name="Hủy đơn (%)",
            orientation="h",
            marker_color=[COLORS["teal"] if c == "Electronics" else COLORS["gray"] for c in cat["Category"]],
            text=[f"{v:.2f}%" for v in cat["cancel_pct"]],
            textposition="outside",
            customdata=cat[["cancelled", "lost_rev"]],
            hovertemplate="<b>%{y}</b><br>Tỉ lệ hủy: %{x:.2f}% (%{customdata[0]} đơn)<br>Tổng thất thoát Hủy+Trả: $%{customdata[1]:,.0f}<extra></extra>",
        )
    )
    fig_cat.add_vline(x=3.05, line_dash="dot", line_color=COLORS["amber"], annotation_text="TB Trả 3,05%", annotation_position="top right")
    fig_cat.update_layout(
        template="plotly_white",
        barmode="group",
        title="<b>Hủy & Trả hàng theo nhóm sản phẩm</b> — Home & Kitchen cao nhất (6,27%)",
        xaxis=dict(title="Tỉ lệ (%)", range=[0, 4.1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=130, r=25, t=70, b=40),
        height=370,
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # -------------------------------------------------------------------------
    # Bieu do 4: Phuong thuc thanh toan — Ty le Huy/Tra & Thiet hai (Cau 8)
    # -------------------------------------------------------------------------
    pay = pd.DataFrame(kpis["q8"]["by_payment"]).iloc[::-1]
    fig_pay = make_subplots(rows=1, cols=2, shared_yaxes=True, column_widths=[0.55, 0.45], horizontal_spacing=0.08, subplot_titles=("Tỉ lệ Hủy vs Trả (%)", "Thất thoát ($M)"))
    fig_pay.add_trace(
        go.Bar(
            y=pay["PaymentMethod"],
            x=pay["cancel_pct"],
            name="Hủy (%)",
            orientation="h",
            marker_color=[COLORS["red"] if p == "Cash on Delivery" else COLORS["gray"] for p in pay["PaymentMethod"]],
            hovertemplate="<b>%{y}</b><br>Tỉ lệ hủy: %{x:.2f}%<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig_pay.add_trace(
        go.Bar(
            y=pay["PaymentMethod"],
            x=pay["return_pct"],
            name="Trả (%)",
            orientation="h",
            marker_color=[COLORS["amber"] if p in ("Net Banking", "Amazon Pay") else COLORS["gray_light"] for p in pay["PaymentMethod"]],
            hovertemplate="<b>%{y}</b><br>Tỉ lệ trả: %{x:.2f}%<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig_pay.add_trace(
        go.Bar(
            y=pay["PaymentMethod"],
            x=pay["lost_rev"] / 1e6,
            name="Thất thoát ($M)",
            orientation="h",
            showlegend=False,
            marker_color=[COLORS["red"] if p == "Credit Card" else COLORS["gray_light"] for p in pay["PaymentMethod"]],
            text=[f"${v/1e6:.2f}M" for v in pay["lost_rev"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Doanh thu thất thoát: $%{x:.2f}M<extra></extra>",
        ),
        row=1,
        col=2,
    )
    fig_pay.update_layout(
        template="plotly_white",
        barmode="group",
        title="<b>Thanh toán & Rủi ro</b> — COD hủy cao nhất (3,17%), Credit Card mất tiền lớn nhất ($1,99M)",
        xaxis1=dict(range=[0, 3.8]),
        xaxis2=dict(range=[0, 2.55]),
        legend=dict(orientation="h", yanchor="bottom", y=1.06, xanchor="right", x=0.52),
        margin=dict(l=125, r=20, t=80, b=40),
        height=370,
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # -------------------------------------------------------------------------
    # Bieu do 5: Top 10 SP tra hang cao nhat (Dot plot tuong tac, nhan Top 5)
    # -------------------------------------------------------------------------
    top10 = pd.DataFrame(kpis["q9"]["top10_returned"]).iloc[::-1].reset_index(drop=True)
    fig_top = go.Figure()
    for i, r in enumerate(top10.itertuples()):
        is_top5 = i >= 5
        col = COLORS["red"] if is_top5 else COLORS["gray"]
        fig_top.add_trace(
            go.Scatter(
                x=[3.05, r.return_pct],
                y=[r.ProductName, r.ProductName],
                mode="lines",
                line=dict(color=col, width=3 if is_top5 else 1.8),
                showlegend=False,
                hoverinfo="skip",
            )
        )
    fig_top.add_trace(
        go.Scatter(
            x=top10["return_pct"],
            y=top10["ProductName"],
            mode="markers+text",
            marker=dict(size=[13 if i >= 5 else 9 for i in range(len(top10))], color=[COLORS["red"] if i >= 5 else COLORS["gray"] for i in range(len(top10))]),
            text=[f" {v:.2f}%" for v in top10["return_pct"]],
            textposition="middle right",
            customdata=top10[["ProductID", "orders", "returned", "return_rev", "cancel_pct"]],
            hovertemplate=(
                "<b>%{y} (%{customdata[0]})</b><br>"
                "Tỉ lệ trả hàng: <b>%{x:.2f}%</b> (%{customdata[2]}/%{customdata[1]:,} đơn)<br>"
                "Giá trị hoàn trả: <b>$%{customdata[3]:,.0f}</b><br>"
                "Tỉ lệ hủy đơn: %{customdata[4]:.2f}%<extra></extra>"
            ),
            showlegend=False,
        )
    )
    fig_top.add_vline(x=3.05, line_dash="dash", line_color=COLORS["amber"], annotation_text="TB toàn sàn: 3,05%", annotation_position="bottom right")
    fig_top.update_layout(
        template="plotly_white",
        title="<b>Top 10 sản phẩm có tỉ lệ trả hàng cao nhất</b> (ngưỡng n ≥ 1.000 đơn · nhấn đỏ Top 5)",
        xaxis=dict(title="Tỉ lệ trả hàng (%)", range=[2.9, 4.35]),
        margin=dict(l=180, r=30, t=65, b=40),
        height=400,
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # -------------------------------------------------------------------------
    # Bieu do 6: Ganh nang phi ship theo phan khuc gia tri don (Cau 7)
    # -------------------------------------------------------------------------
    buckets = pd.DataFrame(kpis["q7"]["by_order_value_bucket"])
    fig_ship = go.Figure(
        go.Bar(
            x=buckets["OrderBucket"],
            y=buckets["mean_ship_pct"],
            marker_color=[COLORS["red"] if b == "<$250" else COLORS["gray_light"] for b in buckets["OrderBucket"]],
            text=[f"{v:.2f}%<br>(${s:.2f})" for v, s in zip(buckets["mean_ship_pct"], buckets["mean_ship"])],
            textposition="outside",
            customdata=buckets[["orders", "mean_ship"]],
            hovertemplate="<b>Phân khúc %{x}</b><br>Số đơn: %{customdata[0]:,}<br>Phí ship TB: $%{customdata[1]:.2f}<br>Tỉ trọng trên giá trị đơn: <b>%{y:.2f}%</b><extra></extra>",
        )
    )
    fig_ship.update_layout(
        template="plotly_white",
        title="<b>Gánh nặng phí vận chuyển theo giá trị đơn</b> — đơn &lt;$250 chịu 6,86% (gấp 18× đơn &gt;$1.5K)",
        yaxis=dict(title="Phí ship / Giá trị đơn (%)", range=[0, 8.6]),
        xaxis=dict(title="Phân khúc giá trị đơn hàng"),
        margin=dict(l=55, r=20, t=65, b=45),
        height=400,
        font=dict(family="Segoe UI, Arial, sans-serif"),
    )

    # Render thanh 1 trang HTML doc lap, sach se, mo trinh duyet la xem ngay
    div_trend = fig_trend.to_html(full_html=False, include_plotlyjs="cdn")
    div_map = fig_map.to_html(full_html=False, include_plotlyjs=False)
    div_cat = fig_cat.to_html(full_html=False, include_plotlyjs=False)
    div_pay = fig_pay.to_html(full_html=False, include_plotlyjs=False)
    div_top = fig_top.to_html(full_html=False, include_plotlyjs=False)
    div_ship = fig_ship.to_html(full_html=False, include_plotlyjs=False)

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dashboard Amazon Sales (2020–2024) — Bài Tập Lớn Trực Quan Hóa Dữ Liệu</title>
  <style>
    :root {{
      --teal: #0F766E;
      --red: #DC2626;
      --amber: #D97706;
      --slate: #0F172A;
      --text: #1E293B;
      --muted: #64748B;
      --bg: #F1F5F9;
      --card: #FFFFFF;
      --border: #E2E8F0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: "Segoe UI", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 22px 26px 36px;
    }}
    .container {{ max-width: 1440px; margin: 0 auto; }}
    header {{
      background: var(--slate);
      color: white;
      padding: 20px 26px;
      border-radius: 14px;
      margin-bottom: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    header h1 {{ font-size: 21px; font-weight: 700; margin-bottom: 4px; }}
    header p {{ font-size: 13px; color: #CBD5E1; }}
    .badge {{
      background: rgba(20, 184, 166, 0.2);
      border: 1px solid #14B8A6;
      color: #99F6E4;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 600;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }}
    .kpi {{
      background: var(--card);
      border: 1px solid var(--border);
      border-left: 5px solid var(--teal);
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: 0 1px 3px rgba(15,23,42,0.05);
    }}
    .kpi.alert {{ border-left-color: var(--red); background: #FFFBFB; }}
    .kpi.neutral {{ border-left-color: #475569; }}
    .kpi .lbl {{ font-size: 11.5px; font-weight: 700; color: var(--muted); letter-spacing: 0.4px; text-transform: uppercase; }}
    .kpi .val {{ font-size: 28px; font-weight: 800; color: var(--teal); margin: 5px 0 3px; }}
    .kpi.alert .val {{ color: var(--red); }}
    .kpi.neutral .val {{ color: var(--slate); }}
    .kpi .sub {{ font-size: 12.5px; color: var(--muted); }}
    .row-2 {{
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }}
    .row-eq {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 16px;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: 0 1px 3px rgba(15,23,42,0.05);
    }}
    .rec-section {{
      background: #FEF2F2;
      border: 1px solid #FECACA;
      border-radius: 12px;
      padding: 18px 22px;
      margin-top: 6px;
    }}
    .rec-section h2 {{
      font-size: 16px;
      color: #991B1B;
      margin-bottom: 12px;
    }}
    .rec-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 14px;
    }}
    .rec-card {{
      background: white;
      border: 1px solid #FEE2E2;
      border-left: 4px solid var(--red);
      border-radius: 10px;
      padding: 14px 16px;
    }}
    .rec-card h3 {{ font-size: 14px; color: var(--slate); margin-bottom: 6px; }}
    .rec-card p {{ font-size: 12.8px; line-height: 1.5; color: var(--text); }}
    .rec-card .tag {{
      display: inline-block;
      margin-top: 8px;
      font-size: 11.5px;
      font-weight: 600;
      color: var(--teal);
      background: #F0FDFA;
      padding: 3px 8px;
      border-radius: 6px;
    }}
    footer {{
      margin-top: 16px;
      font-size: 12px;
      color: var(--muted);
      text-align: center;
    }}
    @media (max-width: 980px) {{
      .row-2, .row-eq {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>DASHBOARD VẬN HÀNH ĐƠN HÀNG &amp; KIỂM SOÁT HỦY / TRẢ HÀNG — AMAZON SALES (2020–2024)</h1>
        <p>Tổng quan trước → Lọc &amp; phóng to → Chi tiết khi cần (nguyên tắc Shneiderman · Di chuột vào biểu đồ để xem số liệu chi tiết)</p>
      </div>
      <span class="badge">Dataset 8 · Synthetic · n = 100.000 đơn</span>
    </header>

    <section class="kpi-grid">
      <div class="kpi">
        <div class="lbl">Tổng số đơn hàng</div>
        <div class="val">{q1['total_orders']:,}</div>
        <div class="sub">{q1['unique_customers']:,} khách · {q1['unique_sellers']:,} người bán · 5 trạng thái</div>
      </div>
      <div class="kpi">
        <div class="lbl">Tổng doanh thu (Gross)</div>
        <div class="val">${q1['gross_revenue']/1e6:,.2f}M</div>
        <div class="sub">Thực giao (Delivered): ${q1['delivered_revenue']/1e6:,.2f}M ({q1['delivered_revenue_pct']}%)</div>
      </div>
      <div class="kpi neutral">
        <div class="lbl">Tổng phí vận chuyển</div>
        <div class="val">${q1['total_shipping_cost']/1e3:,.1f}K</div>
        <div class="sub">TB ${q1['avg_shipping_cost']:.2f}/đơn · chiếm {q1['shipping_share_of_rev_pct']}% doanh thu</div>
      </div>
      <div class="kpi alert">
        <div class="lbl">Thất thoát Hủy &amp; Trả hàng</div>
        <div class="val">${q1['lost_revenue_cancel_return']/1e6:,.2f}M</div>
        <div class="sub">6.077 đơn (6,08%) · Hủy 3,03% ($2,85M) · Trả 3,05% ($2,78M)</div>
      </div>
    </section>

    <section class="row-2">
      <div class="card">{div_trend}</div>
      <div class="card">{div_map}</div>
    </section>

    <section class="row-eq">
      <div class="card">{div_cat}</div>
      <div class="card">{div_pay}</div>
    </section>

    <section class="row-eq">
      <div class="card">{div_top}</div>
      <div class="card">{div_ship}</div>
    </section>

    <section class="rec-section">
      <h2>3 Đề Xuất Hành Động Giảm Hủy &amp; Trả Hàng (Dựa Trên Số Liệu Câu 3, 6, 7, 8, 9)</h2>
      <div class="rec-grid">
        <div class="rec-card">
          <h3>1. Kiểm soát chất lượng &amp; mô tả Top 5 SKU trả cao</h3>
          <p>Rà soát quy chuẩn đóng gói, bảng kích thước và thông số kỹ thuật cho 5 SKU có tỉ lệ trả cao nhất (<b>Yoga Mat 3,97%</b>, <b>Noise Cancelling Headphones 3,79%</b>, <b>Dress Shirt 3,59%</b>, <b>Cookware Set 3,55%</b>, <b>Webcam Full HD 3,53%</b>) và nhóm <b>Home &amp; Kitchen ($984K thất thoát)</b>. Đặc biệt ưu tiên <b>Dress Shirt</b> vì vừa nằm Top 6 doanh thu vừa có tổng hủy+trả tới 7,33%.</p>
          <span class="tag">Mục tiêu: Giảm 20% hoàn trả ở Top 5 SKU → cứu ~$67K</span>
        </div>
        <div class="rec-card">
          <h3>2. Tối ưu xác nhận đơn COD &amp; luồng thanh toán thẻ</h3>
          <p>Áp dụng xác thực OTP/nhắc lịch giao tự động cho đơn <b>Cash on Delivery (tỉ lệ hủy cao nhất 3,17%)</b> và cho đơn giá trị cao (đơn hủy có AOV $942 — cao nhất toàn sàn). Đồng thời nâng cấp bước xác nhận giỏ hàng &amp; đổi trả nhanh cho <b>Credit Card ($1,99M thất thoát)</b> và <b>Debit Card ($1,12M)</b> — nơi chiếm 55% tổng thiệt hại toàn sàn.</p>
          <span class="tag">Mục tiêu: Giảm 0,5 đpt tỉ lệ hủy toàn sàn → cứu ~$460K</span>
        </div>
        <div class="rec-card">
          <h3>3. Chính sách gộp đơn / miễn phí ship từ ngưỡng $250</h3>
          <p>Phí ship cố định quanh $7,4/đơn khiến đơn nhỏ <b>&lt;$250</b> gánh tới <b>6,86% giá trị đơn</b> (gấp 18× đơn &gt;$1.500). Đề xuất gói khuyến khích gộp đơn (free-ship ngưỡng $250) kết hợp cảnh báo tồn kho &amp; thời gian giao chuẩn cho nhóm <b>Electronics (tỉ lệ hủy cao nhất 3,23%)</b> nhằm giảm hủy trước khi xuất kho.</p>
          <span class="tag">Mục tiêu: Tăng AOV đơn nhỏ &amp; giảm hủy trước giao</span>
        </div>
      </div>
    </section>

    <footer>
      Nguồn: Kaggle — Amazon Sales Dataset (rohiteng/amazon-sales-dataset, cập nhật 11/2025). Lưu ý: Dữ liệu tổng hợp (synthetic), kết quả không phản ánh hoạt động thực tế của Amazon.
    </footer>
  </div>
</body>
</html>
"""
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    out = DASH_DIR / "q10_dashboard.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CLEAN_PATH, parse_dates=["OrderDate"])
    kpis = json.loads(KPI_PATH.read_text(encoding="utf-8"))
    p_map = build_q5_choropleth(kpis)
    p_dash = build_q10_dashboard(df, kpis)
    print("Da xuat:", p_map)
    print("Da xuat:", p_dash)


if __name__ == "__main__":
    main()
