"""
Style Guide dung chung cho toan bo du an Truc quan hoa du lieu (Dataset 8: Amazon Sales).
Ap dung 5 huong dan thiet ke Chuong 2 (muc 2.7):
  1. Cho thay du lieu (Show the data)
  2. Giam nhieu / tang ti le data-ink (Reduce clutter)
  3. Gan chu voi hinh: tieu de chu dong, nhan truc tiep, chu thich (Graphics + Text)
  4. Tranh bieu do spaghetti (dung small multiples khi can)
  5. Bat dau tu mau xam (Start with gray) roi moi nhan mau co chu dich
"""

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# Bang mau Start-with-gray thong nhat toan nhom
COLORS = {
    "gray_pale": "#E5E7EB",
    "gray_light": "#CBD5E1",
    "gray": "#94A3B8",
    "gray_dark": "#475569",
    "teal": "#0F766E",
    "teal_mid": "#14B8A6",
    "teal_pale": "#CCFBF1",
    "red": "#DC2626",
    "red_soft": "#F87171",
    "red_pale": "#FEE2E2",
    "amber": "#D97706",
    "amber_pale": "#FEF3C7",
    "blue": "#0369A1",
    "slate": "#0F172A",
    "text": "#1E293B",
    "muted": "#64748B",
    "bg": "#FFFFFF",
    "card_bg": "#F8FAFC",
    "grid": "#E2E8F0",
}

STATUS_COLORS = {
    "Delivered": COLORS["teal"],
    "Shipped": COLORS["gray"],
    "Pending": COLORS["amber"],
    "Returned": COLORS["red"],
    "Cancelled": "#991B1B",
}

DEFAULT_SOURCE = (
    "Nguồn: Kaggle — Amazon Sales Dataset (rohiteng/amazon-sales-dataset, dữ liệu tổng hợp, n = 100.000, 2020–2024)"
)


def apply_style() -> None:
    """Thiet lap theme Matplotlib & Seaborn dong nhat, ho tro day du tieng Viet."""
    sns.set_theme(style="white", context="notebook")
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "text.parse_math": False,
            "figure.facecolor": COLORS["bg"],
            "axes.facecolor": COLORS["bg"],
            "axes.edgecolor": COLORS["gray_light"],
            "axes.linewidth": 0.8,
            "axes.labelcolor": COLORS["text"],
            "axes.labelsize": 10.5,
            "axes.titlecolor": COLORS["slate"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "grid.color": COLORS["grid"],
            "grid.linestyle": "--",
            "grid.linewidth": 0.7,
            "grid.alpha": 0.85,
            "text.color": COLORS["text"],
            "savefig.dpi": 300,
            "savefig.facecolor": COLORS["bg"],
        }
    )


def clean_axes(ax, grid_axis: str | None = None, left_spine: bool = True, bottom_spine: bool = True) -> None:
    """Giam nhieu bieu do: tat vien tren/phai, lam nhe truc va luoi."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(left_spine)
    ax.spines["bottom"].set_visible(bottom_spine)
    if left_spine:
        ax.spines["left"].set_color(COLORS["gray_light"])
    if bottom_spine:
        ax.spines["bottom"].set_color(COLORS["gray_light"])
    ax.tick_params(length=0, pad=6)
    ax.set_axisbelow(True)
    if grid_axis in ("x", "y", "both"):
        ax.grid(True, axis=grid_axis, color=COLORS["grid"], linestyle="--", linewidth=0.7)
    else:
        ax.grid(False)


def add_header(
    fig: plt.Figure,
    title: str,
    subtitle: str,
    x: float = 0.04,
    y_title: float = 0.96,
    y_sub: float = 0.905,
    title_size: float = 14.5,
    sub_size: float = 10.0,
) -> None:
    """Them tieu de chu dong (active title) va phu de can trai thong nhat."""
    fig.text(
        x,
        y_title,
        title,
        fontsize=title_size,
        fontweight="bold",
        color=COLORS["slate"],
        ha="left",
        va="top",
    )
    fig.text(
        x,
        y_sub,
        subtitle,
        fontsize=sub_size,
        color=COLORS["muted"],
        ha="left",
        va="top",
    )


def add_source(fig: plt.Figure, text: str = DEFAULT_SOURCE, x: float = 0.04, y: float = 0.015) -> None:
    """Them chu thich nguon du lieu o chan hinh."""
    fig.text(x, y, text, fontsize=8.5, color=COLORS["muted"], ha="left", va="bottom", style="italic")


def fmt_usd(val: float) -> str:
    """Dinh dang tien USD gon dep."""
    if abs(val) >= 1e6:
        return f"${val / 1e6:,.2f}M"
    if abs(val) >= 1e3:
        return f"${val / 1e3:,.1f}K"
    return f"${val:,.2f}"


def save_chart(fig: plt.Figure, output_path: Path | str) -> Path:
    """Luu anh PNG 300 DPI chuan slide/bao cao."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.2, facecolor=COLORS["bg"])
    plt.close(fig)
    return out
