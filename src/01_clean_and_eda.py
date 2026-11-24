"""
Buoc 1 (TV2 + TV1): Lam sach du lieu, kiem dinh chat luong & tinh toan toan bo KPI cho 10 cau hoi.
Dau vao : data/raw/Amazon.csv
Dau ra  :
  - data/processed/Amazon_clean.csv
  - data/processed/cleaning_summary.json
  - data/processed/kpi_metrics.json
"""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "Amazon.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
CLEAN_PATH = PROCESSED_DIR / "Amazon_clean.csv"
CLEAN_LOG_PATH = PROCESSED_DIR / "cleaning_summary.json"
KPI_PATH = PROCESSED_DIR / "kpi_metrics.json"


def run_cleaning_and_eda() -> tuple[pd.DataFrame, dict, dict]:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(RAW_PATH)
    df = raw.copy()

    # 1. Kiem tra co ban: kich thuoc, thieu, trung lap
    missing_by_col = {col: int(cnt) for col, cnt in df.isna().sum().items() if cnt > 0}
    dup_rows = int(df.duplicated().sum())
    dup_order_id = int(df["OrderID"].duplicated().sum())

    # 2. Chuan hoa kieu ngay & tao cot thoi gian + chi so dan xuat
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], format="%Y-%m-%d", errors="coerce")
    invalid_dates = int(df["OrderDate"].isna().sum())

    # Loai khoang trang thua o cot chu (neu co)
    str_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    trimmed_cells = 0
    for c in str_cols:
        before = df[c]
        after = before.str.strip()
        trimmed_cells += int((before != after).sum())
        df[c] = after

    df["Year"] = df["OrderDate"].dt.year.astype(int)
    df["Month"] = df["OrderDate"].dt.month.astype(int)
    df["Quarter"] = df["OrderDate"].dt.quarter.astype(int)
    df["YearMonth"] = df["OrderDate"].dt.strftime("%Y-%m")
    df["Subtotal"] = (df["Quantity"] * df["UnitPrice"] * (1.0 - df["Discount"])).round(2)
    df["CalcTotal"] = (df["Subtotal"] + df["Tax"] + df["ShippingCost"]).round(2)
    df["FormulaDiff"] = (df["TotalAmount"] - df["CalcTotal"]).abs()
    formula_exact_pct = float((df["FormulaDiff"] <= 0.01).mean() * 100.0)
    max_formula_diff = float(df["FormulaDiff"].max())
    df["ShippingPct"] = (df["ShippingCost"] / df["TotalAmount"] * 100.0).round(4)

    # 3. Kiem tra ngoai le theo quy tac IQR (Chuong 2, Slide 20-21)
    iqr_report = {}
    for col in ["Quantity", "UnitPrice", "Discount", "Tax", "ShippingCost", "TotalAmount"]:
        q1 = float(df[col].quantile(0.25))
        q3 = float(df[col].quantile(0.75))
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        mask = (df[col] < low) | (df[col] > high)
        cnt = int(mask.sum())
        iqr_report[col] = {
            "q1": round(q1, 4),
            "median": round(float(df[col].median()), 4),
            "q3": round(q3, 4),
            "iqr": round(iqr, 4),
            "lower_bound": round(low, 4),
            "upper_bound": round(high, 4),
            "outlier_count": cnt,
            "outlier_pct": round(cnt / len(df) * 100.0, 2),
            "decision": "Giữ nguyên (giá trị hợp lệ từ đơn hàng giá/số lượng cao, không phải lỗi nhập liệu)",
        }

    # 4. Phat hien dac thu du lieu tong hop (synthetic anomalies)
    country_state_pairs = df.groupby("Country")["State"].nunique().to_dict()
    product_category_pairs = int(df.groupby("ProductName")["Category"].nunique().mean())
    cleaning_summary = {
        "source": "Kaggle — rohiteng/amazon-sales-dataset (Amazon Sales Dataset - synthetic)",
        "raw_shape": {"rows": int(raw.shape[0]), "cols": int(raw.shape[1])},
        "clean_shape": {"rows": int(df.shape[0]), "cols": int(df.shape[1]) - 2},  # bo CalcTotal, FormulaDiff
        "date_range": {
            "min": df["OrderDate"].min().strftime("%Y-%m-%d"),
            "max": df["OrderDate"].max().strftime("%Y-%m-%d"),
            "invalid_dates": invalid_dates,
        },
        "missing_values": {"total": int(sum(missing_by_col.values())), "by_column": missing_by_col},
        "duplicates": {"duplicate_rows": dup_rows, "duplicate_order_ids": dup_order_id},
        "whitespace_trimmed_cells": trimmed_cells,
        "formula_check": {
            "formula": "TotalAmount = Quantity * UnitPrice * (1 - Discount) + Tax + ShippingCost",
            "exact_match_pct": round(formula_exact_pct, 4),
            "max_abs_diff": round(max_formula_diff, 4),
        },
        "iqr_outliers": iqr_report,
        "synthetic_notes": {
            "order_status_count": int(df["OrderStatus"].nunique()),
            "order_statuses": sorted(df["OrderStatus"].unique().tolist()),
            "category_count": int(df["Category"].nunique()),
            "categories": sorted(df["Category"].unique().tolist()),
            "brand_count": int(df["Brand"].nunique()),
            "product_count": int(df["ProductName"].nunique()),
            "country_count": int(df["Country"].nunique()),
            "countries": sorted(df["Country"].unique().tolist()),
            "city_state_vs_country_note": (
                "Cả 5 quốc gia đều xuất hiện đủ 13 mã bang Mỹ (TX, CA, DC...); "
                "vì vậy phân tích địa lý dùng cột Country thay vì City/State."
            ),
            "country_unique_states": {k: int(v) for k, v in country_state_pairs.items()},
            "avg_categories_per_product": product_category_pairs,
            "product_category_note": (
                "Trong dữ liệu tổng hợp, ProductName được gán độc lập với Category "
                "(một sản phẩm xuất hiện ở nhiều Category khác nhau)."
            ),
        },
    }

    # Luu file sach (bo 2 cot kiem tra trung gian)
    clean_df = df.drop(columns=["CalcTotal", "FormulaDiff"]).copy()
    clean_df.to_csv(CLEAN_PATH, index=False)

    # =========================================================================
    # TINH TOAN CHI TIET KPI CHO 10 CAU HOI (100% KHOP NHAU GIUA CODE & SLIDE)
    # =========================================================================
    n_orders = len(df)
    gross_rev = float(df["TotalAmount"].sum())
    deliv_rev = float(df.loc[df["OrderStatus"] == "Delivered", "TotalAmount"].sum())
    shipped_rev = float(df.loc[df["OrderStatus"] == "Shipped", "TotalAmount"].sum())
    pending_rev = float(df.loc[df["OrderStatus"] == "Pending", "TotalAmount"].sum())
    return_rev = float(df.loc[df["OrderStatus"] == "Returned", "TotalAmount"].sum())
    cancel_rev = float(df.loc[df["OrderStatus"] == "Cancelled", "TotalAmount"].sum())
    lost_rev = return_rev + cancel_rev
    total_ship = float(df["ShippingCost"].sum())

    # Q1: Overall KPIs
    status_tbl = (
        df.groupby("OrderStatus")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"), avg_order=("TotalAmount", "mean"))
        .sort_values("orders", ascending=False)
    )
    status_tbl["order_pct"] = (status_tbl["orders"] / n_orders * 100).round(2)
    status_tbl["rev_pct"] = (status_tbl["revenue"] / gross_rev * 100).round(2)

    q1 = {
        "total_orders": n_orders,
        "unique_customers": int(df["CustomerID"].nunique()),
        "unique_sellers": int(df["SellerID"].nunique()),
        "gross_revenue": round(gross_rev, 2),
        "delivered_revenue": round(deliv_rev, 2),
        "delivered_revenue_pct": round(deliv_rev / gross_rev * 100, 2),
        "lost_revenue_cancel_return": round(lost_rev, 2),
        "lost_revenue_pct": round(lost_rev / gross_rev * 100, 2),
        "cancel_revenue": round(cancel_rev, 2),
        "return_revenue": round(return_rev, 2),
        "total_shipping_cost": round(total_ship, 2),
        "shipping_share_of_rev_pct": round(total_ship / gross_rev * 100, 2),
        "avg_order_value": round(float(df["TotalAmount"].mean()), 2),
        "median_order_value": round(float(df["TotalAmount"].median()), 2),
        "avg_shipping_cost": round(float(df["ShippingCost"].mean()), 2),
        "status_breakdown": status_tbl.round(2).reset_index().to_dict(orient="records"),
    }

    # Q2: Yearly & Monthly trend
    yearly = (
        df.groupby("Year")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"), avg_order=("TotalAmount", "mean"))
        .reset_index()
    )
    yearly["rev_yoy_pct"] = (yearly["revenue"].pct_change() * 100).round(2)
    ym = (
        df.groupby("YearMonth")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"))
        .reset_index()
        .sort_values("YearMonth")
    )
    monthly_avg = (
        df.groupby("Month")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"))
        .reset_index()
    )
    monthly_avg["avg_orders_per_year"] = (monthly_avg["orders"] / 5.0).round(1)
    monthly_avg["avg_rev_per_year"] = (monthly_avg["revenue"] / 5.0).round(2)

    q2 = {
        "yearly": yearly.round(2).to_dict(orient="records"),
        "best_year_rev": yearly.loc[yearly["revenue"].idxmax()].round(2).to_dict(),
        "worst_year_rev": yearly.loc[yearly["revenue"].idxmin()].round(2).to_dict(),
        "best_month_rev": ym.loc[ym["revenue"].idxmax()].to_dict(),
        "worst_month_rev": ym.loc[ym["revenue"].idxmin()].to_dict(),
        "best_month_orders": ym.loc[ym["orders"].idxmax()].to_dict(),
        "worst_month_orders": ym.loc[ym["orders"].idxmin()].to_dict(),
        "monthly_seasonality": monthly_avg.round(2).to_dict(orient="records"),
        "monthly_rev_cv_pct": round(float(ym["revenue"].std() / ym["revenue"].mean() * 100), 2),
    }

    # Q3: Order status structure & stability across years
    status_by_year = (pd.crosstab(df["Year"], df["OrderStatus"], normalize="index") * 100).round(2)
    ct_status_yr = pd.crosstab(df["Year"], df["OrderStatus"])
    chi2_st, p_st, _, _ = stats.chi2_contingency(ct_status_yr)
    q3 = {
        "status_summary": status_tbl.round(2).reset_index().to_dict(orient="records"),
        "status_by_year_pct": status_by_year.reset_index().to_dict(orient="records"),
        "chi2_year_vs_status": {"chi2": round(float(chi2_st), 3), "p_value": round(float(p_st), 4)},
    }

    # Q4: Revenue by Category (6) + Brand (10) + Top 10 Products
    cat_tbl = (
        df.groupby("Category")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"), avg_order=("TotalAmount", "mean"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    cat_tbl["rev_pct"] = (cat_tbl["revenue"] / gross_rev * 100).round(2)
    prod_rev = (
        df.groupby(["ProductID", "ProductName"])
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"), avg_order=("TotalAmount", "mean"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    prod_rev["rev_pct"] = (prod_rev["revenue"] / gross_rev * 100).round(2)
    brand_rev = (
        df.groupby("Brand")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    brand_rev["rev_pct"] = (brand_rev["revenue"] / gross_rev * 100).round(2)

    q4 = {
        "categories": cat_tbl.round(2).to_dict(orient="records"),
        "top10_products": prod_rev.head(10).round(2).to_dict(orient="records"),
        "brands": brand_rev.round(2).to_dict(orient="records"),
        "category_gap_top_vs_bottom_usd": round(float(cat_tbl["revenue"].max() - cat_tbl["revenue"].min()), 2),
        "category_gap_pct": round(float((cat_tbl["revenue"].max() / cat_tbl["revenue"].min() - 1) * 100), 2),
    }

    # Q5: Revenue by Country
    co_tbl = (
        df.groupby("Country")
        .agg(orders=("OrderID", "count"), revenue=("TotalAmount", "sum"), avg_order=("TotalAmount", "mean"))
        .sort_values("revenue", ascending=False)
        .reset_index()
    )
    co_tbl["rev_pct"] = (co_tbl["revenue"] / gross_rev * 100).round(2)
    co_tbl["order_pct"] = (co_tbl["orders"] / n_orders * 100).round(2)
    q5 = {
        "countries": co_tbl.round(2).to_dict(orient="records"),
        "us_vs_rest_ratio": round(
            float(co_tbl.loc[co_tbl["Country"] == "United States", "revenue"].iloc[0])
            / float(co_tbl.loc[co_tbl["Country"] != "United States", "revenue"].sum()),
            2,
        ),
    }

    # Q6: Cancel & Return rate by Category
    q6_tbl = df.groupby("Category").agg(
        orders=("OrderID", "count"),
        cancelled=("OrderStatus", lambda s: int((s == "Cancelled").sum())),
        returned=("OrderStatus", lambda s: int((s == "Returned").sum())),
        lost_rev=("TotalAmount", lambda s: float(s[df.loc[s.index, "OrderStatus"].isin(["Cancelled", "Returned"])].sum())),
    ).reset_index()
    q6_tbl["cancel_pct"] = (q6_tbl["cancelled"] / q6_tbl["orders"] * 100).round(2)
    q6_tbl["return_pct"] = (q6_tbl["returned"] / q6_tbl["orders"] * 100).round(2)
    q6_tbl["combined_pct"] = ((q6_tbl["cancelled"] + q6_tbl["returned"]) / q6_tbl["orders"] * 100).round(2)
    q6_tbl = q6_tbl.sort_values("combined_pct", ascending=False)

    ct_cat_cr = pd.crosstab(df["Category"], df["OrderStatus"].isin(["Cancelled", "Returned"]))
    chi2_q6, p_q6, _, _ = stats.chi2_contingency(ct_cat_cr)
    q6 = {
        "overall_cancel_pct": round(float((df["OrderStatus"] == "Cancelled").mean() * 100), 2),
        "overall_return_pct": round(float((df["OrderStatus"] == "Returned").mean() * 100), 2),
        "overall_combined_pct": round(float(df["OrderStatus"].isin(["Cancelled", "Returned"]).mean() * 100), 2),
        "by_category": q6_tbl.round(2).to_dict(orient="records"),
        "chi2_test": {"chi2": round(float(chi2_q6), 3), "p_value": round(float(p_q6), 4)},
    }

    # Q7: Shipping cost by Country & vs Order Value
    ship_co = (
        df.groupby("Country")["ShippingCost"]
        .agg(
            orders="count",
            mean="mean",
            median="median",
            std="std",
            q25=lambda s: s.quantile(0.25),
            q75=lambda s: s.quantile(0.75),
            total="sum",
        )
        .sort_values("mean", ascending=False)
        .reset_index()
    )
    groups_ship = [g["ShippingCost"].values for _, g in df.groupby("Country")]
    f_ship, p_ship_anova = stats.f_oneway(*groups_ship)
    r_tot, p_tot = stats.pearsonr(df["TotalAmount"], df["ShippingCost"])
    r_sub, p_sub = stats.pearsonr(df["Subtotal"], df["ShippingCost"])
    rs_tot, ps_tot = stats.spearmanr(df["TotalAmount"], df["ShippingCost"])
    slope, intercept = np.polyfit(df["TotalAmount"], df["ShippingCost"], 1)

    # Chia nhom gia tri don de xem ty le phi ship / gia tri don
    bins = [0, 250, 500, 1000, 1500, 4000]
    labels = ["<$250", "$250–500", "$500–1K", "$1K–1.5K", ">$1.5K"]
    df["OrderBucket"] = pd.cut(df["TotalAmount"], bins=bins, labels=labels)
    ship_bucket = (
        df.groupby("OrderBucket", observed=False)
        .agg(
            orders=("OrderID", "count"),
            mean_ship=("ShippingCost", "mean"),
            median_ship=("ShippingCost", "median"),
            mean_ship_pct=("ShippingPct", "mean"),
            median_ship_pct=("ShippingPct", "median"),
        )
        .reset_index()
    )
    ship_bucket["OrderBucket"] = ship_bucket["OrderBucket"].astype(str)

    q7 = {
        "by_country": ship_co.round(3).to_dict(orient="records"),
        "anova_country_ship": {"f_stat": round(float(f_ship), 3), "p_value": round(float(p_ship_anova), 4)},
        "corr_total_amount_vs_ship": {"pearson_r": round(float(r_tot), 5), "p_value": round(float(p_tot), 4)},
        "corr_subtotal_vs_ship": {"pearson_r": round(float(r_sub), 5), "p_value": round(float(p_sub), 4)},
        "spearman_total_vs_ship": {"rho": round(float(rs_tot), 5), "p_value": round(float(ps_tot), 4)},
        "regression_line": {"slope": round(float(slope), 6), "intercept": round(float(intercept), 4)},
        "by_order_value_bucket": ship_bucket.round(2).to_dict(orient="records"),
        "free_shipping_orders": int((df["ShippingCost"] == 0).sum()),
    }

    # Q8: Payment method vs Cancel & Return
    q8_tbl = df.groupby("PaymentMethod").agg(
        orders=("OrderID", "count"),
        cancelled=("OrderStatus", lambda s: int((s == "Cancelled").sum())),
        returned=("OrderStatus", lambda s: int((s == "Returned").sum())),
        lost_rev=("TotalAmount", lambda s: float(s[df.loc[s.index, "OrderStatus"].isin(["Cancelled", "Returned"])].sum())),
    ).reset_index()
    q8_tbl["order_pct"] = (q8_tbl["orders"] / n_orders * 100).round(2)
    q8_tbl["cancel_pct"] = (q8_tbl["cancelled"] / q8_tbl["orders"] * 100).round(2)
    q8_tbl["return_pct"] = (q8_tbl["returned"] / q8_tbl["orders"] * 100).round(2)
    q8_tbl["combined_pct"] = ((q8_tbl["cancelled"] + q8_tbl["returned"]) / q8_tbl["orders"] * 100).round(2)
    q8_tbl = q8_tbl.sort_values("combined_pct", ascending=False)

    ct_pay_cr = pd.crosstab(df["PaymentMethod"], df["OrderStatus"].isin(["Cancelled", "Returned"]))
    chi2_q8, p_q8, _, _ = stats.chi2_contingency(ct_pay_cr)
    q8 = {
        "by_payment": q8_tbl.round(2).to_dict(orient="records"),
        "chi2_test": {"chi2": round(float(chi2_q8), 3), "p_value": round(float(p_q8), 4)},
    }

    # Q9: Top 5 Products with highest return rate (min orders threshold = 1000)
    min_orders_threshold = 1000
    q9_all = df.groupby(["ProductID", "ProductName"]).agg(
        orders=("OrderID", "count"),
        returned=("OrderStatus", lambda s: int((s == "Returned").sum())),
        cancelled=("OrderStatus", lambda s: int((s == "Cancelled").sum())),
        return_rev=("TotalAmount", lambda s: float(s[df.loc[s.index, "OrderStatus"] == "Returned"].sum())),
        total_rev=("TotalAmount", "sum"),
    ).reset_index()
    q9_all["return_pct"] = (q9_all["returned"] / q9_all["orders"] * 100).round(2)
    q9_all["cancel_pct"] = (q9_all["cancelled"] / q9_all["orders"] * 100).round(2)
    q9_elig = q9_all[q9_all["orders"] >= min_orders_threshold].sort_values(
        ["return_pct", "returned"], ascending=[False, False]
    )

    q9 = {
        "min_orders_threshold": min_orders_threshold,
        "eligible_products": int(len(q9_elig)),
        "total_products": int(len(q9_all)),
        "product_orders_min": int(q9_all["orders"].min()),
        "product_orders_max": int(q9_all["orders"].max()),
        "overall_return_pct": round(float((df["OrderStatus"] == "Returned").mean() * 100), 2),
        "top5_returned": q9_elig.head(5).round(2).to_dict(orient="records"),
        "top10_returned": q9_elig.head(10).round(2).to_dict(orient="records"),
        "bottom5_returned": q9_elig.tail(5).sort_values("return_pct").round(2).to_dict(orient="records"),
    }

    kpis = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
    }

    CLEAN_LOG_PATH.write_text(json.dumps(cleaning_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    KPI_PATH.write_text(json.dumps(kpis, ensure_ascii=False, indent=2), encoding="utf-8")

    return clean_df, cleaning_summary, kpis


if __name__ == "__main__":
    _, summary, kpis = run_cleaning_and_eda()
    print("Da xuat:", CLEAN_PATH)
    print("Da xuat:", CLEAN_LOG_PATH)
    print("Da xuat:", KPI_PATH)
    print("\n--- TOM TAT KPI CHINH ---")
    print("Q1:", json.dumps(kpis["q1"], ensure_ascii=False, indent=2))
    print("Q2 yearly:", json.dumps(kpis["q2"]["yearly"], ensure_ascii=False))
    print("Q2 best/worst month rev:", kpis["q2"]["best_month_rev"], "|", kpis["q2"]["worst_month_rev"])
    print("Q2 monthly_rev_cv_pct:", kpis["q2"]["monthly_rev_cv_pct"])
    print("Q4 categories:", json.dumps(kpis["q4"]["categories"], ensure_ascii=False))
    print("Q5 countries:", json.dumps(kpis["q5"]["countries"], ensure_ascii=False))
    print("Q6:", json.dumps(kpis["q6"], ensure_ascii=False))
    print("Q7:", json.dumps(kpis["q7"], ensure_ascii=False))
    print("Q8:", json.dumps(kpis["q8"], ensure_ascii=False))
    print("Q9 top5:", json.dumps(kpis["q9"]["top5_returned"], ensure_ascii=False, indent=2))
    print("Q9 bottom5:", json.dumps(kpis["q9"]["bottom5_returned"], ensure_ascii=False))
