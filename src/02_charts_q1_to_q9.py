"""
Buoc 2: Tao 9 bieu do tinh chuan xuat ban (300 DPI PNG) cho Cau 1 -> Cau 9 + ban tom tat Dashboard tinh (Cau 10).
Ap dung Style Guide chung (Start with gray, giam nhieu, nhan truc tiep, tieu de chu dong, khong 3D, khong dual-axis).
"""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter
import seaborn as sns

from style_guide import COLORS, STATUS_COLORS, apply_style, clean_axes, add_header, add_source, fmt_usd, save_chart

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "processed" / "Amazon_clean.csv"
KPI_PATH = ROOT / "data" / "processed" / "kpi_metrics.json"
OUT_DIR = ROOT / "outputs" / "charts"


def load_data() -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(CLEAN_PATH, parse_dates=["OrderDate"])
    kpis = json.loads(KPI_PATH.read_text(encoding="utf-8"))
    return df, kpis


# =============================================================================
# CAU 1: THE KPI TONG QUAN + THANH CO CAU 5 TRANG THAI
# =============================================================================
def plot_q1(df: pd.DataFrame, kpis: dict) -> Path:
    q1 = kpis["q1"]
    fig = plt.figure(figsize=(13.5, 6.8))
    add_header(
        fig,
        "100.000 đơn hàng tạo $91,83M doanh thu gộp — nhưng $5,63M (6,1%) bị mất do hủy & trả hàng",
        "Tổng quan quy mô giao dịch, chi phí vận chuyển và tỉ lệ 5 trạng thái đơn hàng (giai đoạn 2020–2024)",
        x=0.04,
        y_title=0.955,
        y_sub=0.895,
    )

    gs = gridspec.GridSpec(2, 4, figure=fig, left=0.04, right=0.96, top=0.81, bottom=0.12, hspace=0.42, wspace=0.14)

    cards = [
        (
            "TỔNG SỐ ĐƠN HÀNG",
            f"{q1['total_orders']:,}",
            f"{q1['unique_customers']:,} khách hàng · {q1['unique_sellers']:,} người bán",
            COLORS["teal"],
            COLORS["card_bg"],
        ),
        (
            "TỔNG DOANH THU (GROSS)",
            f"${q1['gross_revenue']/1e6:,.2f}M",
            f"Thực giao (Delivered): ${q1['delivered_revenue']/1e6:,.2f}M ({q1['delivered_revenue_pct']}%)",
            COLORS["teal"],
            COLORS["card_bg"],
        ),
        (
            "TỔNG PHÍ VẬN CHUYỂN",
            f"${q1['total_shipping_cost']/1e3:,.1f}K",
            f"TB ${q1['avg_shipping_cost']:.2f}/đơn · chiếm {q1['shipping_share_of_rev_pct']}% DT",
            COLORS["gray_dark"],
            COLORS["card_bg"],
        ),
        (
            "THẤT THOÁT HỦY & TRẢ HÀNG",
            f"${q1['lost_revenue_cancel_return']/1e6:,.2f}M",
            f"6.077 đơn (6,08%) · Hủy ${q1['cancel_revenue']/1e6:.2f}M | Trả ${q1['return_revenue']/1e6:.2f}M",
            COLORS["red"],
            "#FEF2F2",
        ),
    ]

    for idx, (label, big_val, sub_txt, accent, bg) in enumerate(cards):
        ax = fig.add_subplot(gs[0, idx])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        rect = patches.FancyBboxPatch(
            (0.02, 0.04),
            0.96,
            0.92,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=bg,
            edgecolor=COLORS["gray_pale"] if accent != COLORS["red"] else "#FECACA",
            linewidth=1.2,
        )
        ax.add_patch(rect)
        # Vach mau nhan ben trai
        bar = patches.FancyBboxPatch(
            (0.02, 0.08),
            0.032,
            0.84,
            boxstyle="round,pad=0.0,rounding_size=0.02",
            facecolor=accent,
            edgecolor="none",
        )
        ax.add_patch(bar)
        ax.text(0.10, 0.80, label, fontsize=9.0, fontweight="bold", color=COLORS["muted"], va="top")
        ax.text(0.10, 0.56, big_val, fontsize=22.5, fontweight="bold", color=accent, va="center")
        ax.text(0.10, 0.22, sub_txt, fontsize=8.6, color=COLORS["text"], va="center", wrap=True)

    # Hang duoi: thanh 100% chia 5 trang thai don hang
    ax_bar = fig.add_subplot(gs[1, :])
    order_seq = ["Delivered", "Shipped", "Pending", "Returned", "Cancelled"]
    st_map = {r["OrderStatus"]: r for r in q1["status_breakdown"]}

    ax_bar.set_xlim(0, 100)
    ax_bar.set_ylim(-0.65, 1.05)
    ax_bar.axis("off")
    ax_bar.text(
        0,
        0.92,
        "Tỉ lệ 5 trạng thái đơn hàng (lưu ý: tệp dữ liệu thật có thêm trạng thái Pending = 4,10%)",
        fontsize=11.0,
        fontweight="bold",
        color=COLORS["slate"],
    )

    left = 0.0
    label_offsets = {
        "Delivered": (0.18, "white"),
        "Shipped": (0.18, "white"),
        "Pending": (-0.36, COLORS["amber"]),
        "Returned": (0.62, COLORS["red"]),
        "Cancelled": (-0.36, "#991B1B"),
    }
    for st in order_seq:
        r = st_map[st]
        pct = r["order_pct"]
        color = STATUS_COLORS[st]
        ax_bar.barh(0.18, pct, left=left, height=0.42, color=color, edgecolor="white", linewidth=1.8)
        mid = left + pct / 2
        if pct >= 12:
            ax_bar.text(
                mid,
                0.18,
                f"{st}\n{pct:.2f}% ({r['orders']:,})",
                ha="center",
                va="center",
                fontsize=10.0,
                fontweight="bold",
                color="white",
            )
        else:
            y_pos, txt_col = label_offsets[st]
            y_edge = 0.39 if y_pos > 0.18 else -0.03
            x_shift = mid
            ha_align = "center"
            if st == "Pending":
                x_shift = mid - 12.5
                ha_align = "right"
            elif st == "Returned":
                x_shift = mid - 2.0
                ha_align = "center"
            elif st == "Cancelled":
                x_shift = 100.0
                ha_align = "right"
            ax_bar.annotate(
                f"{st}: {pct:.2f}% ({r['orders']:,} đơn)",
                xy=(mid, y_edge),
                xytext=(x_shift, y_pos),
                ha=ha_align,
                va="center",
                fontsize=9.2,
                fontweight="bold",
                color=txt_col,
                arrowprops=dict(arrowstyle="-", color=txt_col, lw=1.0),
            )
        left += pct

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q01_kpi.png")


# =============================================================================
# CAU 2: DOANH THU VA SO DON THEO THANG VA THEO NAM (TRANH DUAL-AXIS)
# =============================================================================
def plot_q2(df: pd.DataFrame, kpis: dict) -> Path:
    ym = (
        df.groupby("YearMonth")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"))
        .reset_index()
        .sort_values("YearMonth")
    )
    ym["dt"] = pd.to_datetime(ym["YearMonth"] + "-01")
    yearly = pd.DataFrame(kpis["q2"]["yearly"])

    fig = plt.figure(figsize=(14.0, 7.6))
    add_header(
        fig,
        "Doanh thu (~$18,4M/năm) và số đơn (~20K/năm) rất ổn định; đáy lặp lại mỗi tháng 2 do ít ngày",
        "Tách 2 biểu đồ đường xếp dọc cùng trục thời gian (tránh sai lệch 2 trục Y) và so sánh tổng theo năm (2020–2024)",
        x=0.04,
        y_title=0.965,
        y_sub=0.915,
    )

    gs = gridspec.GridSpec(
        2, 2, figure=fig, width_ratios=[2.35, 1.0], left=0.065, right=0.97, top=0.84, bottom=0.11, hspace=0.34, wspace=0.22
    )

    # Panel trai tren: Doanh thu theo thang
    ax_rev = fig.add_subplot(gs[0, 0])
    clean_axes(ax_rev, grid_axis="y")
    for yr in range(2020, 2025):
        feb = pd.Timestamp(f"{yr}-02-01")
        ax_rev.axvspan(feb - pd.Timedelta(days=12), feb + pd.Timedelta(days=16), color=COLORS["gray_pale"], alpha=0.55, zorder=0)

    rev_m = ym["revenue"] / 1e6
    ax_rev.plot(ym["dt"], rev_m, color=COLORS["teal"], lw=2.0, zorder=3)
    mean_rev = rev_m.mean()
    ax_rev.axhline(mean_rev, color=COLORS["muted"], ls=":", lw=1.1, zorder=2)
    ax_rev.text(ym["dt"].iloc[-1] + pd.Timedelta(days=18), mean_rev + 0.015, f"TB: ${mean_rev:.2f}M", va="bottom", ha="left", fontsize=8.6, color=COLORS["muted"])

    idx_max_r = rev_m.idxmax()
    idx_min_r = rev_m.idxmin()
    ax_rev.scatter([ym.loc[idx_max_r, "dt"]], [rev_m.loc[idx_max_r]], color=COLORS["teal"], s=55, zorder=5)
    ax_rev.scatter([ym.loc[idx_min_r, "dt"]], [rev_m.loc[idx_min_r]], color=COLORS["red"], s=55, zorder=5)

    ax_rev.annotate(
        f"Đỉnh: {ym.loc[idx_max_r, 'YearMonth']}\n(${rev_m.loc[idx_max_r]:.2f}M)",
        xy=(ym.loc[idx_max_r, "dt"], rev_m.loc[idx_max_r]),
        xytext=(ym.loc[idx_max_r, "dt"] - pd.Timedelta(days=270), rev_m.loc[idx_max_r] + 0.08),
        fontsize=8.8,
        fontweight="bold",
        color=COLORS["teal"],
        arrowprops=dict(arrowstyle="->", color=COLORS["teal"], lw=1.0),
    )
    ax_rev.annotate(
        f"Đáy: {ym.loc[idx_min_r, 'YearMonth']} (${rev_m.loc[idx_min_r]:.2f}M)\nTháng 2 luôn thấp (28–29 ngày)",
        xy=(ym.loc[idx_min_r, "dt"], rev_m.loc[idx_min_r]),
        xytext=(ym.loc[idx_min_r, "dt"] + pd.Timedelta(days=180), rev_m.loc[idx_min_r] - 0.11),
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["red"],
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.0),
    )
    ax_rev.set_ylim(1.15, 1.82)
    ax_rev.set_ylabel("Doanh thu tháng ($ triệu)")
    ax_rev.set_title("Doanh thu hàng tháng (60 tháng, CV = 4,21% — ghi chú: trục cắt để thấy biến động tháng)", loc="left", fontsize=10.2, fontweight="bold", pad=8)
    ax_rev.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:.2f}M"))

    # Panel trai duoi: So don theo thang
    ax_ord = fig.add_subplot(gs[1, 0], sharex=ax_rev)
    clean_axes(ax_ord, grid_axis="y")
    for yr in range(2020, 2025):
        feb = pd.Timestamp(f"{yr}-02-01")
        ax_ord.axvspan(feb - pd.Timedelta(days=12), feb + pd.Timedelta(days=16), color=COLORS["gray_pale"], alpha=0.55, zorder=0)

    ax_ord.plot(ym["dt"], ym["orders"], color=COLORS["gray_dark"], lw=2.0, zorder=3)
    mean_ord = ym["orders"].mean()
    ax_ord.axhline(mean_ord, color=COLORS["muted"], ls=":", lw=1.1, zorder=2)
    ax_ord.text(ym["dt"].iloc[-1] + pd.Timedelta(days=18), mean_ord + 12, f"TB: {mean_ord:,.0f}", va="bottom", ha="left", fontsize=8.6, color=COLORS["muted"])

    idx_max_o = ym["orders"].idxmax()
    idx_min_o = ym["orders"].idxmin()
    ax_ord.scatter([ym.loc[idx_max_o, "dt"]], [ym.loc[idx_max_o, "orders"]], color=COLORS["teal"], s=55, zorder=5)
    ax_ord.scatter([ym.loc[idx_min_o, "dt"]], [ym.loc[idx_min_o, "orders"]], color=COLORS["red"], s=55, zorder=5)
    ax_ord.annotate(
        f"Đỉnh: {ym.loc[idx_max_o, 'YearMonth']} ({ym.loc[idx_max_o, 'orders']:,} đơn)",
        xy=(ym.loc[idx_max_o, "dt"], ym.loc[idx_max_o, "orders"]),
        xytext=(ym.loc[idx_max_o, "dt"] + pd.Timedelta(days=130), ym.loc[idx_max_o, "orders"] + 45),
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["teal"],
        arrowprops=dict(arrowstyle="->", color=COLORS["teal"], lw=1.0),
    )
    ax_ord.annotate(
        f"Đáy: {ym.loc[idx_min_o, 'YearMonth']} ({ym.loc[idx_min_o, 'orders']:,} đơn)",
        xy=(ym.loc[idx_min_o, "dt"], ym.loc[idx_min_o, "orders"]),
        xytext=(ym.loc[idx_min_o, "dt"] + pd.Timedelta(days=180), ym.loc[idx_min_o, "orders"] - 95),
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["red"],
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.0),
    )
    ax_ord.set_ylim(1350, 1920)
    ax_ord.set_ylabel("Số đơn hàng / tháng")
    ax_ord.set_xlabel("Thời gian (vùng xám nhạt đánh dấu tháng 2 hằng năm)")
    ax_ord.set_title("Số lượng đơn hàng hàng tháng", loc="left", fontsize=10.2, fontweight="bold", pad=8)

    # Panel phai tren: Doanh thu theo nam (goc 0 chuan Tufte)
    ax_yr_r = fig.add_subplot(gs[0, 1])
    clean_axes(ax_yr_r, grid_axis="y")
    cols_r = [COLORS["teal"] if y == 2020 else COLORS["gray_light"] for y in yearly["Year"]]
    bars_r = ax_yr_r.bar(yearly["Year"].astype(str), yearly["revenue"] / 1e6, color=cols_r, width=0.58)
    for b, val in zip(bars_r, yearly["revenue"] / 1e6):
        ax_yr_r.text(b.get_x() + b.get_width() / 2, val + 0.45, f"${val:.2f}M", ha="center", va="bottom", fontsize=8.8, fontweight="bold")
    ax_yr_r.set_ylim(0, 22.5)
    ax_yr_r.set_title("Tổng doanh thu theo năm (gốc 0)", loc="left", fontsize=10.2, fontweight="bold", pad=8)
    ax_yr_r.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:.0f}M"))

    # Panel phai duoi: So don theo nam (goc 0 chuan Tufte)
    ax_yr_o = fig.add_subplot(gs[1, 1])
    clean_axes(ax_yr_o, grid_axis="y")
    cols_o = [COLORS["teal"] if y == 2023 else COLORS["gray_light"] for y in yearly["Year"]]
    bars_o = ax_yr_o.bar(yearly["Year"].astype(str), yearly["orders"], color=cols_o, width=0.58)
    for b, val in zip(bars_o, yearly["orders"]):
        ax_yr_o.text(b.get_x() + b.get_width() / 2, val + 450, f"{val:,}", ha="center", va="bottom", fontsize=8.8, fontweight="bold")
    ax_yr_o.set_ylim(0, 24500)
    ax_yr_o.set_xlabel("Năm")
    ax_yr_o.set_title("Tổng số đơn theo năm (gốc 0)", loc="left", fontsize=10.2, fontweight="bold", pad=8)
    ax_yr_o.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q02_trend.png")


# =============================================================================
# CAU 3: CO CAU 5 TRANG THAI DON HANG (THEO NAM + SO SANH SO DON & DOANH THU)
# =============================================================================
def plot_q3(df: pd.DataFrame, kpis: dict) -> Path:
    q3 = kpis["q3"]
    yr_df = pd.DataFrame(q3["status_by_year_pct"])
    st_df = pd.DataFrame(q3["status_summary"])
    order_seq = ["Delivered", "Shipped", "Pending", "Returned", "Cancelled"]
    st_df["OrderStatus"] = pd.Categorical(st_df["OrderStatus"], categories=order_seq, ordered=True)
    st_df = st_df.sort_values("OrderStatus")

    fig = plt.figure(figsize=(13.8, 6.6))
    add_header(
        fig,
        "Cơ cấu 5 trạng thái bất biến suốt 5 năm — riêng Hủy & Trả chiếm 6,08% đơn ($5,63M thất thoát)",
        "Trái: Cột chồng 100% theo năm (χ² = 14,19, p = 0,58) · Phải: Quy mô đơn, giá trị và AOV từng trạng thái",
        x=0.04,
        y_title=0.96,
        y_sub=0.90,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.15, 1.1], left=0.06, right=0.96, top=0.81, bottom=0.14, wspace=0.28)

    # Panel trai: Cot chong 100% theo nam
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis=None, left_spine=False)
    years = yr_df["Year"].astype(str).tolist()
    bottom = np.zeros(len(years))
    stack_colors = {
        "Delivered": COLORS["gray_light"],
        "Shipped": COLORS["gray"],
        "Pending": COLORS["amber"],
        "Returned": COLORS["red_soft"],
        "Cancelled": COLORS["red"],
    }
    for st in order_seq:
        vals = yr_df[st].values
        ax1.bar(years, vals, bottom=bottom, width=0.58, color=stack_colors[st], edgecolor="white", linewidth=1.2)
        for i, v in enumerate(vals):
            if v >= 12:
                ax1.text(i, bottom[i] + v / 2, f"{v:.1f}%", ha="center", va="center", fontsize=9.0, fontweight="bold", color=COLORS["slate"] if st == "Delivered" else "white")
        # Nhan truc tiep ben phai cot 2024
        y_mid = bottom[-1] + vals[-1] / 2
        if st == "Pending":
            y_mid -= 1.0
        elif st == "Returned":
            y_mid += 0.5
        elif st == "Cancelled":
            y_mid += 2.6
        ax1.text(len(years) - 0.62, y_mid, f" {st} ({vals[-1]:.1f}%)", va="center", ha="left", fontsize=8.8, fontweight="bold", color=stack_colors[st] if st != "Delivered" else COLORS["gray_dark"])
        bottom += vals

    # Tong huy + tra tren dau cot
    for i, row in yr_df.iterrows():
        cr = row["Cancelled"] + row["Returned"]
        ax1.text(i, 101.6, f"Hủy+Trả\n{cr:.2f}%", ha="center", va="bottom", fontsize=8.2, fontweight="bold", color=COLORS["red"])

    ax1.set_xlim(-0.5, len(years) + 0.65)
    ax1.set_ylim(0, 113)
    ax1.set_yticks([])
    ax1.set_title("Cơ cấu trạng thái theo từng năm (2020–2024)", loc="left", fontsize=10.5, fontweight="bold", pad=10)

    # Panel phai: Cot ngang so sanh ty trong + nhan truc tiep doanh thu & AOV
    ax2 = fig.add_subplot(gs[0, 1])
    clean_axes(ax2, grid_axis="x", bottom_spine=False)
    plot_df = st_df.iloc[::-1].reset_index(drop=True)
    bar_cols = [COLORS["red"] if s in ("Cancelled", "Returned") else (COLORS["teal"] if s == "Delivered" else COLORS["gray_light"]) for s in plot_df["OrderStatus"]]
    bars = ax2.barh(plot_df["OrderStatus"], plot_df["order_pct"], color=bar_cols, height=0.58)
    for b, row in zip(bars, plot_df.itertuples()):
        txt = f" {row.order_pct:.2f}%  |  {row.orders:,} đơn  |  ${row.revenue/1e6:.2f}M (AOV ${row.avg_order:.0f})"
        col = COLORS["red"] if row.OrderStatus in ("Cancelled", "Returned") else COLORS["text"]
        ax2.text(b.get_width() + 0.8, b.get_y() + b.get_height() / 2, txt, va="center", ha="left", fontsize=8.7, fontweight="bold" if row.OrderStatus in ("Delivered", "Cancelled", "Returned") else "normal", color=col)

    ax2.set_xlim(0, 132)
    ax2.set_xticks([0, 25, 50, 75])
    ax2.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax2.set_title("Tỉ trọng số đơn, tổng doanh thu & AOV theo trạng thái", loc="left", fontsize=10.5, fontweight="bold", pad=10)
    ax2.annotate(
        "Đơn Cancelled có AOV cao nhất ($942)\n→ 3,03% số đơn nhưng mất 3,10% doanh thu!",
        xy=(64, 0.16),
        xytext=(52, 1.55),
        fontsize=8.6,
        fontweight="bold",
        color=COLORS["red"],
        bbox=dict(boxstyle="round,pad=0.38", facecolor="#FEF2F2", edgecolor="#FECACA"),
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.1, connectionstyle="arc3,rad=-0.12"),
    )

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q03_order_status.png")


# =============================================================================
# CAU 4: DOANH THU THEO 6 NHOM SAN PHAM (CATEGORY) + TOP 10 SAN PHAM
# =============================================================================
def plot_q4(df: pd.DataFrame, kpis: dict) -> Path:
    cats = pd.DataFrame(kpis["q4"]["categories"]).iloc[::-1].reset_index(drop=True)
    top10 = pd.DataFrame(kpis["q4"]["top10_products"]).iloc[::-1].reset_index(drop=True)
    top5_ret_names = {r["ProductName"] for r in kpis["q9"]["top5_returned"]}

    fig = plt.figure(figsize=(14.0, 6.7))
    add_header(
        fig,
        "Electronics dẫn đầu 6 nhóm hàng ($15,58M); Top 10 sản phẩm tạo $1,88M–$1,94M mỗi SKU",
        "Đối chiếu tệp thật: dữ liệu chỉ có 6 Category (phân bố rất đều ~16,5%–17,0%), bổ sung Top 10 sản phẩm doanh thu cao nhất",
        x=0.04,
        y_title=0.96,
        y_sub=0.90,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.0, 1.15], left=0.13, right=0.96, top=0.81, bottom=0.13, wspace=0.42)

    # Panel trai: 6 Category
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis="x")
    cols1 = [COLORS["teal"] if c == "Electronics" else COLORS["gray_light"] for c in cats["Category"]]
    bars1 = ax1.barh(cats["Category"], cats["revenue"] / 1e6, color=cols1, height=0.58)
    for b, r in zip(bars1, cats.itertuples()):
        is_top = r.Category == "Electronics"
        ax1.text(
            b.get_width() + 0.25,
            b.get_y() + b.get_height() / 2,
            f"${r.revenue/1e6:.2f}M ({r.rev_pct:.1f}%)",
            va="center",
            fontsize=9.2,
            fontweight="bold" if is_top else "normal",
            color=COLORS["teal"] if is_top else COLORS["text"],
        )
    ax1.set_xlim(0, 21.5)
    ax1.set_xlabel("Doanh thu ($ triệu, trục bắt đầu từ 0)")
    ax1.set_title("Doanh thu 6 nhóm sản phẩm (Category · chênh đỉnh–đáy +2,8%)", loc="left", fontsize=10.3, fontweight="bold", pad=10)

    # Panel phai: Top 10 ProductName
    ax2 = fig.add_subplot(gs[0, 1])
    clean_axes(ax2, grid_axis="x")
    cols2 = []
    for name in top10["ProductName"]:
        if name == "Memory Card 128GB":
            cols2.append(COLORS["teal"])
        elif name in top5_ret_names:
            cols2.append(COLORS["red"])
        else:
            cols2.append(COLORS["gray_light"])
    bars2 = ax2.barh(top10["ProductName"], top10["revenue"] / 1e6, color=cols2, height=0.62)
    for b, r in zip(bars2, top10.itertuples()):
        suffix = "  • Top 3 trả hàng!" if r.ProductName in top5_ret_names else ""
        col = COLORS["red"] if r.ProductName in top5_ret_names else (COLORS["teal"] if r.ProductName == "Memory Card 128GB" else COLORS["text"])
        ax2.text(
            b.get_width() + 0.03,
            b.get_y() + b.get_height() / 2,
            f"${r.revenue/1e6:.2f}M ({r.orders:,} đơn){suffix}",
            va="center",
            fontsize=8.5,
            fontweight="bold" if (r.ProductName in top5_ret_names or r.ProductName == "Memory Card 128GB") else "normal",
            color=col,
        )
    ax2.set_xlim(0, 3.05)
    ax2.set_xlabel("Doanh thu ($ triệu, trục bắt đầu từ 0)")
    ax2.set_title("Top 10 sản phẩm doanh thu cao nhất (trong 50 SKU)", loc="left", fontsize=10.4, fontweight="bold", pad=10)

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q04_category_revenue.png")


# =============================================================================
# CAU 5: DOANH THU THEO KHU VUC KHACH HANG (5 QUOC GIA + AOV)
# =============================================================================
def plot_q5(df: pd.DataFrame, kpis: dict) -> Path:
    co = pd.DataFrame(kpis["q5"]["countries"]).iloc[::-1].reset_index(drop=True)

    fig = plt.figure(figsize=(13.8, 6.4))
    add_header(
        fig,
        "Hoa Kỳ chiếm áp đảo 70,0% tổng doanh thu ($64,31M) — gấp 2,34 lần 4 thị trường còn lại cộng lại",
        "Phân tích theo cột Country (không dùng City/State do lỗi ghép ngẫu nhiên dữ liệu synthetic); xem thêm bản đồ tương tác HTML",
        x=0.04,
        y_title=0.96,
        y_sub=0.90,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.55, 1.0], left=0.12, right=0.96, top=0.80, bottom=0.14, wspace=0.30)

    # Panel trai: Cot ngang xep hang doanh thu 5 quoc gia
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis="x")
    cols = [
        COLORS["teal"] if c == "United States" else (COLORS["teal_mid"] if c == "India" else COLORS["gray_light"])
        for c in co["Country"]
    ]
    bars = ax1.barh(co["Country"], co["revenue"] / 1e6, color=cols, height=0.56)
    for b, r in zip(bars, co.itertuples()):
        is_hi = r.Country in ("United States", "India")
        ax1.text(
            b.get_width() + 1.0,
            b.get_y() + b.get_height() / 2,
            f"${r.revenue/1e6:.2f}M  ({r.rev_pct:.1f}% · {r.orders:,} đơn)",
            va="center",
            fontsize=9.3,
            fontweight="bold" if is_hi else "normal",
            color=COLORS["teal"] if r.Country == "United States" else COLORS["text"],
        )
    ax1.set_xlim(0, 92)
    ax1.set_xlabel("Tổng doanh thu ($ triệu, gốc 0)")
    ax1.set_title("Tổng doanh thu & số đơn theo quốc gia", loc="left", fontsize=10.5, fontweight="bold", pad=10)

    # Panel phai: Dot plot gia tri don trung binh (AOV) — ly giai nguyen nhan chenh lech
    ax2 = fig.add_subplot(gs[0, 1])
    clean_axes(ax2, grid_axis="x")
    mean_aov = kpis["q1"]["avg_order_value"]
    ax2.axvline(mean_aov, color=COLORS["amber"], ls="--", lw=1.3, zorder=1)
    ax2.text(mean_aov + 1.2, 4.48, f"TB sàn: ${mean_aov:.0f}", ha="left", va="bottom", fontsize=8.6, fontweight="bold", color=COLORS["amber"])

    for i, r in enumerate(co.itertuples()):
        col = COLORS["teal"] if r.Country == "India" else COLORS["gray_dark"]
        ax2.hlines(i, 880, r.avg_order, color=COLORS["gray_pale"], lw=2.5, zorder=2)
        ax2.scatter([r.avg_order], [i], color=col, s=95, zorder=4)
        ax2.text(r.avg_order + 2.2, i, f"${r.avg_order:.2f}", va="center", fontsize=9.2, fontweight="bold" if r.Country == "India" else "normal", color=col)

    ax2.set_yticks(range(len(co)))
    ax2.set_yticklabels([""] * len(co))
    ax2.set_xlim(880, 942)
    ax2.set_ylim(-0.6, 4.85)
    ax2.set_xlabel("Giá trị đơn trung bình — AOV ($)")
    ax2.set_title("AOV gần như tương đương giữa 5 nước (~$915–$922)", loc="left", fontsize=10.5, fontweight="bold", pad=10)
    ax2.text(
        882,
        2.45,
        "Chênh lệch doanh thu\n100% do quy mô số đơn,\nkhông phải mức chi/đơn.",
        fontsize=8.4,
        color=COLORS["text"],
        va="center",
        bbox=dict(boxstyle="round,pad=0.38", facecolor=COLORS["card_bg"], edgecolor=COLORS["gray_pale"]),
    )

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q05_region_revenue.png")


# =============================================================================
# CAU 6: TI LE HUY VA TRA HANG THEO NHOM SAN PHAM (TACH RIENG HUY VS TRA)
# =============================================================================
def plot_q6(df: pd.DataFrame, kpis: dict) -> Path:
    q6 = kpis["q6"]
    cat = pd.DataFrame(q6["by_category"]).iloc[::-1].reset_index(drop=True)

    fig = plt.figure(figsize=(13.8, 6.5))
    add_header(
        fig,
        "Home & Kitchen có tổng tỉ lệ Hủy+Trả cao nhất (6,27% · $984K); Electronics dẫn đầu về tỉ lệ Hủy (3,23%)",
        "Tách riêng Hủy đơn (trước giao) và Trả hàng (sau giao) cho 6 nhóm sản phẩm — chênh lệch biên độ hẹp (χ² p = 0,84)",
        x=0.04,
        y_title=0.96,
        y_sub=0.90,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.55, 1.0], left=0.14, right=0.96, top=0.80, bottom=0.14, wspace=0.25)

    # Panel trai: Cot nhom ngang tach Cancel % va Return %
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis="x")
    y = np.arange(len(cat))
    h = 0.34

    bars_ret = ax1.barh(y + h / 2, cat["return_pct"], height=h, color=[COLORS["red"] if c == "Home & Kitchen" else COLORS["red_soft"] for c in cat["Category"]], label="Tỉ lệ Trả hàng (Returned %)")
    bars_can = ax1.barh(y - h / 2, cat["cancel_pct"], height=h, color=[COLORS["teal"] if c == "Electronics" else COLORS["gray"] for c in cat["Category"]], label="Tỉ lệ Hủy đơn (Cancelled %)")

    ax1.axvline(q6["overall_return_pct"], color=COLORS["red"], ls=":", lw=1.1, alpha=0.85)
    ax1.text(q6["overall_return_pct"] + 0.04, 5.55, f"TB Trả: {q6['overall_return_pct']}% · TB Hủy: {q6['overall_cancel_pct']}%", fontsize=8.4, color=COLORS["muted"])

    for b, r in zip(bars_ret, cat.itertuples()):
        is_hi = r.Category == "Home & Kitchen"
        ax1.text(b.get_width() + 0.05, b.get_y() + b.get_height() / 2, f"{r.return_pct:.2f}% ({r.returned})", va="center", fontsize=8.6, fontweight="bold" if is_hi else "normal", color=COLORS["red"] if is_hi else COLORS["text"])
    for b, r in zip(bars_can, cat.itertuples()):
        is_hi = r.Category == "Electronics"
        ax1.text(b.get_width() + 0.05, b.get_y() + b.get_height() / 2, f"{r.cancel_pct:.2f}% ({r.cancelled})", va="center", fontsize=8.6, fontweight="bold" if is_hi else "normal", color=COLORS["teal"] if is_hi else COLORS["text"])

    ax1.set_yticks(y)
    ax1.set_yticklabels(cat["Category"], fontweight="bold")
    ax1.set_xlim(0, 4.35)
    ax1.set_ylim(-0.6, 5.85)
    ax1.set_xlabel("Tỉ lệ trên tổng đơn của nhóm (%, gốc 0)")
    ax1.set_title("Tỉ lệ Trả hàng vs Hủy đơn theo từng Category", loc="left", fontsize=10.4, fontweight="bold", pad=22)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.00), ncol=2, frameon=False, fontsize=8.6)

    # Panel phai: Tong doanh thu that thoat (Huy + Tra)
    ax2 = fig.add_subplot(gs[0, 1])
    clean_axes(ax2, grid_axis="x")
    cols2 = [COLORS["red"] if c == "Home & Kitchen" else COLORS["gray_light"] for c in cat["Category"]]
    bars2 = ax2.barh(y, cat["lost_rev"] / 1e3, color=cols2, height=0.52)
    for b, r in zip(bars2, cat.itertuples()):
        is_hi = r.Category == "Home & Kitchen"
        ax2.text(
            b.get_width() + 15,
            b.get_y() + b.get_height() / 2,
            f"${r.lost_rev/1e3:,.0f}K  ({r.combined_pct:.2f}%)",
            va="center",
            fontsize=8.9,
            fontweight="bold" if is_hi else "normal",
            color=COLORS["red"] if is_hi else COLORS["text"],
        )
    ax2.set_yticks(y)
    ax2.set_yticklabels([""] * len(cat))
    ax2.set_xlim(0, 1450)
    ax2.set_ylim(-0.6, 5.85)
    ax2.set_xlabel("Doanh thu thất thoát Hủy + Trả ($ nghìn)")
    ax2.set_title("Tổng thất thoát & tỉ lệ gộp (Hủy + Trả)", loc="left", fontsize=10.4, fontweight="bold", pad=10)

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q06_cancel_return_category.png")


# =============================================================================
# CAU 7: CHI PHI VAN CHUYEN THEO KHU VUC & THEO GIA TRI DON
# =============================================================================
def plot_q7(df: pd.DataFrame, kpis: dict) -> Path:
    q7 = kpis["q7"]
    country_order = [r["Country"] for r in q7["by_country"]]
    buckets = pd.DataFrame(q7["by_order_value_bucket"])

    fig = plt.figure(figsize=(14.2, 7.2))
    add_header(
        fig,
        "Phí vận chuyển đồng nhất quanh $7,4/đơn ở mọi quốc gia (p = 0,57) và hầu như không đổi theo giá trị đơn (r = 0,04)",
        "Hệ quả: đơn hàng nhỏ (<$250) chịu gánh nặng phí vận chuyển tới 6,86% giá trị đơn — cao gấp 18 lần đơn >$1.500 (0,38%)",
        x=0.04,
        y_title=0.965,
        y_sub=0.912,
    )

    gs = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[1.05, 1.25], height_ratios=[1.35, 1.0], left=0.065, right=0.96, top=0.84, bottom=0.11, hspace=0.45, wspace=0.26)

    # Panel trai (chiem ca 2 hang): Boxplot phi van chuyen theo 5 quoc gia
    ax_box = fig.add_subplot(gs[:, 0])
    clean_axes(ax_box, grid_axis="y")
    pal = {c: (COLORS["teal_pale"] if c == "United States" else "#E2E8F0") for c in country_order}
    sns.boxplot(
        data=df,
        x="Country",
        y="ShippingCost",
        order=country_order,
        hue="Country",
        palette=pal,
        legend=False,
        width=0.52,
        linewidth=1.2,
        fliersize=0,
        ax=ax_box,
    )
    ax_box.axhline(kpis["q1"]["avg_shipping_cost"], color=COLORS["amber"], ls="--", lw=1.2)
    for i, r in enumerate(q7["by_country"]):
        ax_box.scatter([i], [r["mean"]], color=COLORS["teal"] if r["Country"] == "United States" else COLORS["slate"], s=45, zorder=5)
        ax_box.text(i, r["q75"] + 0.75, f"TB: ${r['mean']:.2f}\nTV: ${r['median']:.2f}", ha="center", va="bottom", fontsize=8.4, fontweight="bold", color=COLORS["text"])
    ax_box.set_ylim(0, 16.5)
    ax_box.set_xlabel("")
    ax_box.set_ylabel("Chi phí vận chuyển ($ / đơn)")
    ax_box.set_xticks(range(len(country_order)))
    ax_box.set_xticklabels(["Canada", "Australia", "United\nStates", "India", "United\nKingdom"])
    ax_box.set_title("Phân phối phí vận chuyển theo quốc gia (ANOVA F = 0,73, p = 0,57)", loc="left", fontsize=10.2, fontweight="bold", pad=10)
    ax_box.text(
        0.03,
        0.04,
        "Dải phí gần như cố định $0–$15\nQ1 ≈ $3,7 · Trung vị ≈ $7,3 · Q3 ≈ $11,2",
        transform=ax_box.transAxes,
        fontsize=8.5,
        color=COLORS["muted"],
        bbox=dict(boxstyle="round,pad=0.35", facecolor=COLORS["card_bg"], edgecolor=COLORS["gray_pale"]),
    )

    # Panel phai tren: Hexbin mat do 100.000 don (TotalAmount vs ShippingCost) + duong hoi quy
    ax_hex = fig.add_subplot(gs[0, 1])
    clean_axes(ax_hex, grid_axis=None)
    hb = ax_hex.hexbin(df["TotalAmount"], df["ShippingCost"], gridsize=34, cmap="Greys", mincnt=5, alpha=0.88)
    cb = fig.colorbar(hb, ax=ax_hex, pad=0.02, aspect=16)
    cb.set_label("Số đơn / ô", fontsize=8.5, color=COLORS["muted"])
    cb.ax.tick_params(labelsize=8)

    xs = np.linspace(0, 3500, 100)
    ys = q7["regression_line"]["slope"] * xs + q7["regression_line"]["intercept"]
    ax_hex.plot(xs, ys, color=COLORS["red"], lw=2.2, label=f"Hồi quy tuyến tính (r = {q7['corr_total_amount_vs_ship']['pearson_r']:.3f})")
    ax_hex.set_xlim(0, 3550)
    ax_hex.set_ylim(0, 15.8)
    ax_hex.set_xlabel("Giá trị đơn hàng — TotalAmount ($)")
    ax_hex.set_ylabel("Phí vận chuyển ($)")
    ax_hex.set_title("Quan hệ Giá trị đơn vs Phí vận chuyển (mật độ n = 100.000, tránh chồng điểm)", loc="left", fontsize=10.2, fontweight="bold", pad=8)
    ax_hex.legend(loc="upper right", frameon=True, facecolor="white", edgecolor=COLORS["gray_pale"], fontsize=8.5)

    # Panel phai duoi: Ty trong phi van chuyen / gia tri don theo nhom gia tri don
    ax_b = fig.add_subplot(gs[1, 1])
    clean_axes(ax_b, grid_axis="y")
    cols_b = [COLORS["red"] if b == "<$250" else COLORS["gray_light"] for b in buckets["OrderBucket"]]
    bars_b = ax_b.bar(buckets["OrderBucket"], buckets["mean_ship_pct"], color=cols_b, width=0.56)
    for b, r in zip(bars_b, buckets.itertuples()):
        is_hi = r.OrderBucket == "<$250"
        ax_b.text(
            b.get_x() + b.get_width() / 2,
            r.mean_ship_pct + 0.25,
            f"{r.mean_ship_pct:.2f}%\n(${r.mean_ship:.2f})",
            ha="center",
            va="bottom",
            fontsize=8.6,
            fontweight="bold" if is_hi else "normal",
            color=COLORS["red"] if is_hi else COLORS["text"],
        )
    ax_b.set_ylim(0, 8.8)
    ax_b.set_ylabel("Phí ship / Giá trị đơn (%)")
    ax_b.set_xlabel("Phân khúc giá trị đơn hàng")
    ax_b.set_title("Gánh nặng phí vận chuyển theo phân khúc giá trị đơn (gốc 0)", loc="left", fontsize=10.2, fontweight="bold", pad=8)

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q07_shipping_cost.png")


# =============================================================================
# CAU 8: HINH THUC THANH TOAN & TI LE HUY / TRA HANG
# =============================================================================
def plot_q8(df: pd.DataFrame, kpis: dict) -> Path:
    q8 = kpis["q8"]
    pay = pd.DataFrame(q8["by_payment"]).iloc[::-1].reset_index(drop=True)

    fig = plt.figure(figsize=(14.0, 6.5))
    add_header(
        fig,
        "COD có tỉ lệ hủy cao nhất (3,17%), nhưng Credit Card gây thất thoát lớn nhất ($1,99M · 35% tổng thiệt hại)",
        "Tách tỉ lệ Hủy vs Trả theo 6 phương thức thanh toán (χ² p = 0,78) và đối chiếu quy mô tiền mặt thất thoát thực tế",
        x=0.04,
        y_title=0.96,
        y_sub=0.90,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.45, 1.05], left=0.14, right=0.96, top=0.80, bottom=0.14, wspace=0.25)

    # Panel trai: Cot nhom ngang Cancel % vs Return %
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis="x")
    y = np.arange(len(pay))
    h = 0.34

    bars_ret = ax1.barh(
        y + h / 2,
        pay["return_pct"],
        height=h,
        color=[COLORS["amber"] if p in ("Net Banking", "Amazon Pay") else COLORS["gray_light"] for p in pay["PaymentMethod"]],
        label="Tỉ lệ Trả hàng (Returned %)",
    )
    bars_can = ax1.barh(
        y - h / 2,
        pay["cancel_pct"],
        height=h,
        color=[COLORS["red"] if p == "Cash on Delivery" else COLORS["gray"] for p in pay["PaymentMethod"]],
        label="Tỉ lệ Hủy đơn (Cancelled %)",
    )

    ax1.axvline(kpis["q6"]["overall_cancel_pct"], color=COLORS["muted"], ls=":", lw=1.1)
    ax1.text(3.04, 5.55, "TB sàn ~3,04%", fontsize=8.4, color=COLORS["muted"])

    for b, r in zip(bars_ret, pay.itertuples()):
        hi = r.PaymentMethod in ("Net Banking", "Amazon Pay")
        ax1.text(b.get_width() + 0.05, b.get_y() + b.get_height() / 2, f"{r.return_pct:.2f}%", va="center", fontsize=8.6, fontweight="bold" if hi else "normal", color=COLORS["amber"] if hi else COLORS["text"])
    for b, r in zip(bars_can, pay.itertuples()):
        hi = r.PaymentMethod == "Cash on Delivery"
        ax1.text(b.get_width() + 0.05, b.get_y() + b.get_height() / 2, f"{r.cancel_pct:.2f}%", va="center", fontsize=8.6, fontweight="bold" if hi else "normal", color=COLORS["red"] if hi else COLORS["text"])

    ax1.set_yticks(y)
    ax1.set_yticklabels([f"{r.PaymentMethod}\n({r.order_pct:.1f}% đơn)" for r in pay.itertuples()], fontweight="bold", fontsize=9.0)
    ax1.set_xlim(0, 4.1)
    ax1.set_ylim(-0.6, 5.85)
    ax1.set_xlabel("Tỉ lệ trên tổng đơn của phương thức (%, gốc 0)")
    ax1.set_title("Tỉ lệ Hủy vs Trả theo phương thức thanh toán", loc="left", fontsize=10.4, fontweight="bold", pad=22)
    ax1.legend(loc="lower left", bbox_to_anchor=(0.0, 1.00), ncol=2, frameon=False, fontsize=8.5)

    # Panel phai: Doanh thu that thoat (Huy + Tra)
    ax2 = fig.add_subplot(gs[0, 1])
    clean_axes(ax2, grid_axis="x")
    cols2 = [COLORS["red"] if p == "Credit Card" else (COLORS["gray_dark"] if p == "Debit Card" else COLORS["gray_light"]) for p in pay["PaymentMethod"]]
    bars2 = ax2.barh(y, pay["lost_rev"] / 1e6, color=cols2, height=0.52)
    for b, r in zip(bars2, pay.itertuples()):
        hi = r.PaymentMethod == "Credit Card"
        ax2.text(
            b.get_width() + 0.05,
            b.get_y() + b.get_height() / 2,
            f"${r.lost_rev/1e6:.2f}M  ({r.cancelled + r.returned:,} đơn)",
            va="center",
            fontsize=8.9,
            fontweight="bold" if hi else "normal",
            color=COLORS["red"] if hi else COLORS["text"],
        )
    ax2.set_yticks(y)
    ax2.set_yticklabels([""] * len(pay))
    ax2.set_xlim(0, 2.85)
    ax2.set_ylim(-0.6, 5.85)
    ax2.set_xlabel("Doanh thu thất thoát Hủy + Trả ($ triệu)")
    ax2.set_title("Thiệt hại tiền mặt thực tế theo phương thức", loc="left", fontsize=10.4, fontweight="bold", pad=10)
    ax2.annotate(
        "Credit + Debit Card chiếm 55% đơn\n→ $3,10M thất thoát (55,1% toàn sàn)!",
        xy=(1.99, 3.85),
        xytext=(1.15, 2.35),
        fontsize=8.5,
        fontweight="bold",
        color=COLORS["red"],
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#FEF2F2", edgecolor="#FECACA"),
        arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.1),
    )

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q08_payment_cancel_return.png")


# =============================================================================
# CAU 9: TOP 5 SAN PHAM CO TI LE TRA HANG CAO NHAT (DOT PLOT + BANG SO LIEU)
# =============================================================================
def plot_q9(df: pd.DataFrame, kpis: dict) -> Path:
    q9 = kpis["q9"]
    top10 = pd.DataFrame(q9["top10_returned"]).iloc[::-1].reset_index(drop=True)
    top5 = pd.DataFrame(q9["top5_returned"])
    overall = q9["overall_return_pct"]

    fig = plt.figure(figsize=(14.0, 7.2))
    add_header(
        fig,
        "Yoga Mat (3,97%) dẫn đầu Top 5 sản phẩm trả hàng nhiều nhất — gây $334K giá trị hoàn trả",
        f"Ngưỡng tối thiểu: n ≥ {q9['min_orders_threshold']:,} đơn/SP (50/50 SKU đạt, 1.910–2.098 đơn) · Dot plot giúp phân biệt rõ các tỉ lệ gần nhau",
        x=0.04,
        y_title=0.965,
        y_sub=0.912,
    )

    gs = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[1.25, 1.15], left=0.18, right=0.97, top=0.83, bottom=0.13, wspace=0.16)

    # Panel trai: Dot plot (Lollipop) Top 10, nhan do Top 5
    ax1 = fig.add_subplot(gs[0, 0])
    clean_axes(ax1, grid_axis="x")
    ax1.axvline(overall, color=COLORS["amber"], ls="--", lw=1.4, zorder=1)
    ax1.text(overall + 0.03, 0.25, f"TB toàn sàn: {overall:.2f}%", fontsize=8.8, fontweight="bold", color=COLORS["amber"])

    for i, r in enumerate(top10.itertuples()):
        is_top5 = i >= 5
        col = COLORS["red"] if is_top5 else COLORS["gray"]
        ax1.hlines(i, overall, r.return_pct, color=col, lw=2.4 if is_top5 else 1.5, alpha=0.85, zorder=2)
        ax1.scatter([r.return_pct], [i], color=col, s=95 if is_top5 else 55, zorder=4)
        ax1.text(
            r.return_pct + 0.04,
            i,
            f"{r.return_pct:.2f}%  ({r.returned}/{r.orders:,})",
            va="center",
            fontsize=8.8,
            fontweight="bold" if is_top5 else "normal",
            color=COLORS["red"] if is_top5 else COLORS["muted"],
        )

    ax1.axhline(4.5, color=COLORS["gray_light"], ls=":", lw=1.0)
    ax1.text(3.09, 4.62, "TOP 5 ƯU TIÊN XỬ LÝ ↑", fontsize=8.2, fontweight="bold", color=COLORS["red"])

    ax1.set_yticks(range(len(top10)))
    ax1.set_yticklabels(top10["ProductName"], fontsize=9.3)
    for idx_tick, lbl in enumerate(ax1.get_yticklabels()):
        if idx_tick >= 5:
            lbl.set_fontweight("bold")
            lbl.set_color(COLORS["slate"])
    ax1.set_xlim(2.8, 4.55)
    ax1.set_ylim(-0.6, 9.7)
    ax1.set_xlabel("Tỉ lệ trả hàng (%) — so với đường chuẩn trung bình toàn sàn")
    ax1.set_title("Xếp hạng Top 10 sản phẩm có tỉ lệ trả hàng cao nhất", loc="left", fontsize=10.4, fontweight="bold", pad=10)

    # Panel phai: Bang so lieu cu the Top 5 + Insight box
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis("off")
    ax2.text(0.0, 0.96, "Bảng số liệu chi tiết Top 5 sản phẩm (đủ ngưỡng n ≥ 1.000)", fontsize=10.4, fontweight="bold", color=COLORS["slate"], va="top")

    col_labels = ["#", "Sản phẩm (Mã)", "Tổng đơn", "Đơn trả", "Tỉ lệ trả", "Giá trị trả"]
    cell_text = []
    for rank, r in enumerate(top5.itertuples(), start=1):
        cell_text.append(
            [
                f"#{rank}",
                f"{r.ProductName}\n({r.ProductID})",
                f"{r.orders:,}",
                f"{r.returned}",
                f"{r.return_pct:.2f}%",
                f"${r.return_rev:,.0f}",
            ]
        )
    tot_ord = int(top5["orders"].sum())
    tot_ret = int(top5["returned"].sum())
    tot_rev = float(top5["return_rev"].sum())
    cell_text.append(["Tổng", "Top 5 SKU", f"{tot_ord:,}", f"{tot_ret}", f"{tot_ret/tot_ord*100:.2f}%", f"${tot_rev:,.0f}"])

    tbl = ax2.table(
        cellText=cell_text,
        colLabels=col_labels,
        cellLoc="center",
        colWidths=[0.07, 0.42, 0.12, 0.10, 0.12, 0.17],
        bbox=[0.0, 0.30, 1.0, 0.60],
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.5)

    for (row_i, col_i), cell in tbl.get_celld().items():
        cell.set_edgecolor(COLORS["gray_pale"])
        if row_i == 0:
            cell.set_facecolor(COLORS["slate"])
            cell.set_text_props(color="white", fontweight="bold")
        elif row_i == len(cell_text):
            cell.set_facecolor("#FEF2F2")
            cell.set_text_props(color=COLORS["red"], fontweight="bold")
        else:
            cell.set_facecolor("#FFFFFF" if row_i % 2 == 1 else COLORS["card_bg"])
            if col_i == 4:
                cell.set_text_props(color=COLORS["red"], fontweight="bold")
            if col_i == 1:
                cell.set_text_props(ha="left")

    # Hop chu thich phan tich chuyen sau
    note = (
        "Phát hiện đáng chú ý:\n"
        "• Yoga Mat cao hơn trung bình sàn +0,92 điểm % (gấp 1,8 lần sản phẩm thấp nhất:\n"
        "  Bluetooth Speaker 2,20%).\n"
        "• Dress Shirt (P00030) là điểm nóng kép: vừa nằm Top 6 doanh thu ($1,90M), vừa có\n"
        "  tỉ lệ trả 3,59% ($76,6K) và tỉ lệ hủy cao nhất nhóm Top 5 (3,74% → tổng 7,33%)."
    )
    ax2.text(
        0.0,
        0.22,
        note,
        fontsize=8.7,
        color=COLORS["text"],
        va="top",
        linespacing=1.45,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS["card_bg"], edgecolor=COLORS["gray_pale"]),
    )

    add_source(fig)
    return save_chart(fig, OUT_DIR / "q09_top5_return.png")


# =============================================================================
# CAU 10 (BAN TINH CHO SLIDE): DASHBOARD TONG HOP 1 TRANG CO CHU THICH
# =============================================================================
def plot_q10_static(df: pd.DataFrame, kpis: dict) -> Path:
    q1 = kpis["q1"]
    co = pd.DataFrame(kpis["q5"]["countries"]).iloc[::-1]
    cat = pd.DataFrame(kpis["q6"]["by_category"]).iloc[::-1]
    pay = pd.DataFrame(kpis["q8"]["by_payment"]).iloc[::-1]
    top5 = pd.DataFrame(kpis["q9"]["top5_returned"]).iloc[::-1]
    ym = df.groupby("YearMonth").agg(revenue=("TotalAmount", "sum")).reset_index().sort_values("YearMonth")
    ym["dt"] = pd.to_datetime(ym["YearMonth"] + "-01")

    fig = plt.figure(figsize=(16.0, 9.2))
    add_header(
        fig,
        "DASHBOARD VẬN HÀNH AMAZON SALES (2020–2024): Kiểm soát thất thoát $5,63M từ Hủy & Trả hàng",
        "Bản tổng hợp tĩnh cho slide (bản tương tác đầy đủ mở tại outputs/dashboard/q10_dashboard.html — nguyên tắc Shneiderman)",
        x=0.03,
        y_title=0.97,
        y_sub=0.925,
        title_size=15.0,
    )

    gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[0.62, 1.25, 1.3], left=0.04, right=0.97, top=0.87, bottom=0.07, hspace=0.45, wspace=0.28)

    # Hang 1: 4 the KPI gon (trai -> phai)
    gs_kpi = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=gs[0, :], wspace=0.12)
    kpi_items = [
        ("TỔNG ĐƠN HÀNG", "100.000", "2020–2024 · 5 quốc gia", COLORS["teal"], COLORS["card_bg"]),
        ("DOANH THU GỘP", "$91,83M", "Thực giao: $68,37M (74,5%)", COLORS["teal"], COLORS["card_bg"]),
        ("TỔNG PHÍ VẬN CHUYỂN", "$740,7K", "TB $7,41/đơn · 0,81% DT", COLORS["gray_dark"], COLORS["card_bg"]),
        ("THẤT THOÁT HỦY + TRẢ", "$5,63M (6,08%)", "Hủy 3,03% · Trả 3,05%", COLORS["red"], "#FEF2F2"),
    ]
    for i, (lbl, val, sub, acc, bg) in enumerate(kpi_items):
        ax = fig.add_subplot(gs_kpi[0, i])
        ax.axis("off")
        ax.add_patch(patches.FancyBboxPatch((0.01, 0.04), 0.98, 0.92, boxstyle="round,pad=0.02,rounding_size=0.08", facecolor=bg, edgecolor=COLORS["gray_pale"]))
        ax.add_patch(patches.Rectangle((0.01, 0.06), 0.025, 0.88, facecolor=acc, edgecolor="none"))
        ax.text(0.08, 0.82, lbl, fontsize=8.3, fontweight="bold", color=COLORS["muted"], va="top")
        ax.text(0.08, 0.48, val, fontsize=17.5, fontweight="bold", color=acc, va="center")
        ax.text(0.08, 0.16, sub, fontsize=8.0, color=COLORS["text"], va="center")

    # Hang 2, Cot 1-2: Xu huong doanh thu thang
    ax_tr = fig.add_subplot(gs[1, :2])
    clean_axes(ax_tr, grid_axis="y")
    ax_tr.plot(ym["dt"], ym["revenue"] / 1e6, color=COLORS["teal"], lw=1.8)
    ax_tr.axhline(ym["revenue"].mean() / 1e6, color=COLORS["muted"], ls=":", lw=1.0)
    ax_tr.set_ylim(1.2, 1.75)
    ax_tr.set_ylabel("$ triệu")
    ax_tr.set_title("1. Xu hướng doanh thu tháng ổn định (~$1,53M/tháng; đáy tháng 2)", loc="left", fontsize=9.8, fontweight="bold", pad=6)

    # Hang 2, Cot 3: Doanh thu 5 quoc gia
    ax_co = fig.add_subplot(gs[1, 2])
    clean_axes(ax_co, grid_axis="x")
    ax_co.barh(co["Country"], co["revenue"] / 1e6, color=[COLORS["teal"] if c == "United States" else COLORS["gray_light"] for c in co["Country"]], height=0.58)
    for i, r in enumerate(co.itertuples()):
        ax_co.text(r.revenue / 1e6 + 1.0, i, f"${r.revenue/1e6:.1f}M ({r.rev_pct:.0f}%)", va="center", fontsize=8.2, fontweight="bold" if r.Country == "United States" else "normal")
    ax_co.set_xlim(0, 88)
    ax_co.set_title("2. Hoa Kỳ chiếm 70% doanh thu", loc="left", fontsize=9.8, fontweight="bold", pad=6)

    # Hang 3, Cot 1: Huy + Tra theo Category
    ax_c6 = fig.add_subplot(gs[2, 0])
    clean_axes(ax_c6, grid_axis="x")
    ax_c6.barh(cat["Category"], cat["combined_pct"], color=[COLORS["red"] if c == "Home & Kitchen" else COLORS["gray_light"] for c in cat["Category"]], height=0.58)
    for i, r in enumerate(cat.itertuples()):
        ax_c6.text(r.combined_pct + 0.08, i, f"{r.combined_pct:.2f}% (${r.lost_rev/1e3:.0f}K)", va="center", fontsize=8.0, fontweight="bold" if r.Category == "Home & Kitchen" else "normal", color=COLORS["red"] if r.Category == "Home & Kitchen" else COLORS["text"])
    ax_c6.set_xlim(0, 8.8)
    ax_c6.set_title("3. Hủy+Trả theo nhóm hàng", loc="left", fontsize=9.8, fontweight="bold", pad=6)

    # Hang 3, Cot 2: Top 5 SP tra hang cao nhat
    ax_c9 = fig.add_subplot(gs[2, 1])
    clean_axes(ax_c9, grid_axis="x")
    ax_c9.axvline(3.05, color=COLORS["amber"], ls="--", lw=1.1)
    for i, r in enumerate(top5.itertuples()):
        ax_c9.hlines(i, 3.05, r.return_pct, color=COLORS["red"], lw=2.2)
        ax_c9.scatter([r.return_pct], [i], color=COLORS["red"], s=65, zorder=4)
        ax_c9.text(r.return_pct + 0.04, i, f"{r.return_pct:.2f}% (${r.return_rev/1e3:.0f}K)", va="center", fontsize=8.0, fontweight="bold", color=COLORS["red"])
    ax_c9.set_yticks(range(len(top5)))
    ax_c9.set_yticklabels([n[:19] + ("…" if len(n) > 19 else "") for n in top5["ProductName"]], fontsize=8.3)
    ax_c9.set_xlim(2.9, 4.65)
    ax_c9.set_title("4. Top 5 SP trả hàng cao nhất (TB: 3,05%)", loc="left", fontsize=9.8, fontweight="bold", pad=6)

    # Hang 3, Cot 3: Hop 3 De xuat hanh dong gan so lieu
    ax_rec = fig.add_subplot(gs[2, 2])
    ax_rec.set_xlim(0, 1)
    ax_rec.set_ylim(0, 1)
    ax_rec.axis("off")
    ax_rec.add_patch(patches.FancyBboxPatch((0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.02,rounding_size=0.05", facecolor="#FEF2F2", edgecolor="#FECACA", linewidth=1.2))
    ax_rec.text(0.05, 0.93, "3 ĐỀ XUẤT GIẢM HỦY & TRẢ HÀNG", fontsize=9.2, fontweight="bold", color=COLORS["red"], va="top")
    ax_rec.plot([0.05, 0.95], [0.83, 0.83], color="#FECACA", lw=1.2)
    rec_text = (
        "1. Kiểm soát chất lượng & mô tả Top 5 SKU\n"
        "   trả cao (Yoga Mat 3,97%, Dress Shirt 3,59%\n"
        "   — $334K hoàn trả) & nhóm Home & Kitchen.\n\n"
        "2. Tối ưu luồng thanh toán trọng điểm:\n"
        "   xác thực OTP/nhắc đơn COD (hủy 3,17%)\n"
        "   & giảm lỗi giao dịch Credit Card ($1,99M).\n\n"
        "3. Gói gộp đơn / miễn ship ngưỡng $250\n"
        "   giảm gánh nặng phí 6,86% ở đơn nhỏ,\n"
        "   hạn chế hủy trước giao ở Electronics."
    )
    ax_rec.text(0.05, 0.78, rec_text, fontsize=8.3, color=COLORS["slate"], va="top", linespacing=1.35)

    add_source(fig, x=0.03, y=0.012)
    return save_chart(fig, OUT_DIR / "q10_dashboard_preview.png")


def main() -> None:
    apply_style()
    df, kpis = load_data()
    paths = [
        plot_q1(df, kpis),
        plot_q2(df, kpis),
        plot_q3(df, kpis),
        plot_q4(df, kpis),
        plot_q5(df, kpis),
        plot_q6(df, kpis),
        plot_q7(df, kpis),
        plot_q8(df, kpis),
        plot_q9(df, kpis),
        plot_q10_static(df, kpis),
    ]
    for p in paths:
        print("Da xuat:", p)


if __name__ == "__main__":
    main()
