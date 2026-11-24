# Bài Tập Lớn — Trực Quan Hóa Dữ Liệu (Dataset 8: Amazon Sales)

Dự án phân tích vận hành đơn hàng, chi phí vận chuyển và tối ưu tỉ lệ hủy/trả hàng trên tập dữ liệu **Amazon Sales Dataset (synthetic, 100.000 giao dịch, 2020–2024)**, thực hiện bằng hệ sinh thái Python (`pandas`, `Matplotlib`, `Seaborn`, `Plotly HTML`) theo chuẩn Chương 1–3.

## Cấu trúc thư mục

```text
Data-Visualization/
├── data/
│   ├── raw/Amazon.csv                     # Dữ liệu gốc Kaggle (rohiteng/amazon-sales-dataset)
│   └── processed/
│       ├── Amazon_clean.csv               # Dữ liệu đã chuẩn hóa ngày & cột dẫn xuất
│       ├── cleaning_summary.json          # Nhật ký kiểm tra & làm sạch dữ liệu (IQR, công thức, synthetic notes)
│       └── kpi_metrics.json               # Toàn bộ số liệu chính xác cho Câu 1–10
├── notebooks/
│   └── Amazon_Sales_Presentation.ipynb    # Notebook vừa code vừa thuyết trình như slide (15 slides, chạy sẵn output)
├── src/
│   ├── style_guide.py                     # Style Guide Start-with-gray dùng chung toàn nhóm
│   ├── 01_clean_and_eda.py                # Làm sạch dữ liệu & xuất KPI chuẩn
│   ├── 02_charts_q1_to_q9.py              # Sinh 10 ảnh PNG 300 DPI (Câu 1–9 + bản tĩnh Dashboard Câu 10)
│   ├── 03_dashboard_q10.py                # Sinh Dashboard tương tác Plotly HTML & Bản đồ Choropleth Câu 5
│   └── build_notebook.py                  # Tự động tạo & chạy lại notebook thuyết trình
├── outputs/
│   ├── charts/                            # q01_kpi.png ... q10_dashboard_preview.png (300 DPI)
│   └── dashboard/
│       ├── q10_dashboard.html             # Dashboard tổng hợp tương tác (mở bằng trình duyệt)
│       └── q05_country_map.html           # Bản đồ Choropleth tương tác Câu 5
├── docs/
│   ├── phan_cong_nhom.md                  # Bản phân công chi tiết 7 thành viên
│   ├── slide_content.md                   # Nội dung hoàn chỉnh 15 slides thuyết trình
│   └── thuyet_trinh_va_qa.md              # Kịch bản thuyết trình 10–12 phút & 12 câu hỏi phản biện Q&A
└── task/0001_task.md                      # Đặc tả yêu cầu & dàn ý dự án
```

## Cách chạy lại toàn bộ mã nguồn

```bash
pip install pandas numpy matplotlib seaborn scipy plotly
python src/01_clean_and_eda.py
python src/02_charts_q1_to_q9.py
python src/03_dashboard_q10.py
```

Sau khi chạy xong, mở trực tiếp `outputs/dashboard/q10_dashboard.html` trên trình duyệt (Chrome/Edge) để trải nghiệm Dashboard tương tác.

> **Nguồn & Lưu ý**: Dữ liệu từ Kaggle (`rohiteng/amazon-sales-dataset`, cập nhật 11/2025). Đây là dữ liệu tổng hợp (*synthetic*), kết quả chỉ phục vụ mục đích học thuật và không phản ánh hoạt động thực tế của Amazon.
