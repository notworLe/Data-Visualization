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

## Cách mở Dashboard HTML tương tác (Demo khi thuyết trình)

Dự án có 2 file HTML tương tác:
- **Dashboard tổng hợp (Câu 10 — Slide 13)**: `outputs/dashboard/q10_dashboard.html`
- **Bản đồ Choropleth theo quốc gia (Câu 5 — Slide 8)**: `outputs/dashboard/q05_country_map.html`

**3 cách mở nhanh trên Windows:**
1. **File Explorer (nhanh nhất)**: Vào thư mục `outputs/dashboard/`, nhấp đúp `q10_dashboard.html` (hoặc chuột phải → *Open with* → Chrome / Edge).
2. **PowerShell** (chạy từ thư mục gốc dự án):
   ```powershell
   start outputs/dashboard/q10_dashboard.html
   start outputs/dashboard/q05_country_map.html
   ```
3. **VS Code**: Chuột phải file HTML ở cây thư mục → *Reveal in File Explorer* → nhấp đúp mở bằng trình duyệt *(hoặc dùng extension Live Preview / Open in Browser)*.

**Mẹo demo trước lớp:**
- Nhấn `F11` trên Chrome/Edge để phóng toàn màn hình.
- Thao tác trực tiếp: chọn năm ở **dropdown góc phải** biểu đồ xu hướng, kéo **Range Slider**, và **di chuột (hover)** lên bản đồ thế giới / các cột để hiện số liệu chi tiết.
- *Lưu ý*: File HTML nạp `plotly.js` qua CDN nên máy trình chiếu cần có kết nối Internet (nếu cần chạy offline hoàn toàn, đổi `include_plotlyjs="cdn"` thành `include_plotlyjs=True` trong `src/03_dashboard_q10.py` rồi chạy lại).

## Cách xem Notebook trình chiếu & Docs thuyết trình

- Mở `notebooks/Amazon_Sales_Presentation.ipynb` bằng VS Code hoặc JupyterLab (15 slides đã chạy sẵn bảng số liệu, 10 biểu đồ PNG và biểu đồ Plotly tương tác).
- Đọc lời thoại 11 phút 30 giây & 12 câu Q&A phản biện tại `docs/thuyet_trinh_va_qa.md`, nội dung chi tiết từng slide tại `docs/slide_content.md`.

## Cách chạy lại toàn bộ mã nguồn

```bash
pip install pandas numpy matplotlib seaborn scipy plotly nbformat nbclient ipykernel
python src/01_clean_and_eda.py
python src/02_charts_q1_to_q9.py
python src/03_dashboard_q10.py
python src/build_notebook.py
```

> **Nguồn & Lưu ý**: Dữ liệu từ Kaggle (`rohiteng/amazon-sales-dataset`, cập nhật 11/2025). Đây là dữ liệu tổng hợp (*synthetic*), kết quả chỉ phục vụ mục đích học thuật và không phản ánh hoạt động thực tế của Amazon.
