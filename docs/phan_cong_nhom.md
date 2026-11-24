# BẢN PHÂN CÔNG NHÓM — BÀI TẬP LỚN TRỰC QUAN HÓA DỮ LIỆU

- **Đề tài**: Phân tích đơn hàng, vận chuyển và tối ưu tỉ lệ hủy/trả hàng — **Dataset 8: Amazon Sales Dataset (synthetic)**
- **Công cụ chung**: Python (`pandas`, `Matplotlib`, `Seaborn`, `Plotly HTML`) + Slide thuyết trình (PowerPoint/Canva)
- **Sản phẩm nộp**: Dữ liệu sạch/Code + 10 Biểu đồ PNG + Dashboard HTML + Slide thuyết trình (10–12 phút)
- **Tài liệu đặc tả chung**: [task/0001_task.md](../task/0001_task.md)

---

## 1. Đã điều chỉnh gì so với bảng dự tính ban đầu?

So với [du_tinh_phan_cong.png](../media/du_tinh_phan_cong.png), bảng phân công này giữ nguyên khung 7 người nhưng chỉnh **5 điểm quan trọng** để tránh lệch số và đúng yêu cầu chấm điểm:

1. **Bỏ phần viết báo cáo Word dài** (vì đề bài chỉ yêu cầu *Code/Dữ liệu sạch + 10 biểu đồ + Dashboard + Slide thuyết trình 10–12 phút*) → chuyển thời gian cho TV1 & TV7 sang **Style Guide, kịch bản nói và bộ Q&A phản biện**.
2. **Bổ sung khâu chốt chung ở Mốc 1**: TV1 + TV2 chốt *công thức KPI & Cleaning Log*, TV1 + TV7 chốt *Style Guide & Slide Master* trước khi vẽ biểu đồ.
3. **Cập nhật theo dữ liệu thật `Amazon.csv`**:
   - Câu 1 & 3 có **5 trạng thái đơn** (thêm `Pending` = 4.103 đơn, không chỉ 4 trạng thái như đề ghi).
   - Câu 4 chỉ có **6 `Category`** (vẽ đủ 6 Category + bổ sung Top 10 sản phẩm để đủ ý "10 nhóm").
   - Câu 5 & 7 dùng cột **`Country`** (5 quốc gia), không dùng `City`/`State` vì dữ liệu synthetic ghép sai bang/quốc gia.
   - Câu 9 mỗi sản phẩm đều có 1.910–2.098 đơn → đặt ngưỡng minh bạch `n >= 1.000` đơn.
4. **Tránh nút cổ chai tiến độ**: TV2 xuất dữ liệu sạch sớm nhất (Mốc 1); TV6 dựng khung Dashboard HTML ngay từ file sạch thay vì đợi TV1–5 xong hết mới làm.
5. **Bổ sung rõ người lo Kịch bản 10–12 phút (nhấn 4 câu trọng tâm) & Phản biện Q&A (25% điểm)**.

---

## 2. Bảng phân công tổng quan (7 thành viên)

| TV | Họ tên *(điền sau)* | Vai trò chính | Câu phụ trách | Sản phẩm bàn giao chính |
|---|---|---|---|---|
| **TV1** | | Trưởng nhóm · Tổng quan & Kiểm duyệt | **Câu 1** + Mở đầu | Chốt công thức KPI; Thẻ KPI tổng quan (Câu 1); rà soát khớp số liệu toàn nhóm |
| **TV2** | | Xử lý dữ liệu · Xu hướng thời gian | **Làm sạch** + **Câu 2** | `Amazon_clean.csv` + Nhật ký làm sạch (Cleaning Log); Biểu đồ xu hướng tháng/năm (Câu 2) |
| **TV3** | | Cơ cấu trạng thái & Sản phẩm | **Câu 3** + **Câu 4** | Biểu đồ cơ cấu 5 trạng thái (Câu 3); Doanh thu 6 nhóm hàng + Top 10 SP (Câu 4) |
| **TV4** | | Phân tích khu vực & Vận chuyển | **Câu 5** + **Câu 7** | Doanh thu theo 5 quốc gia + Bản đồ (Câu 5); Phí VC theo quốc gia & giá trị đơn (Câu 7) |
| **TV5** | | Phân tích sâu Hủy & Trả hàng | **Câu 6** + **Câu 8** | Tỉ lệ Hủy & Trả tách riêng theo nhóm SP (Câu 6) và theo phương thức thanh toán (Câu 8) |
| **TV6** | | Chi tiết sản phẩm & Dashboard | **Câu 9** + **Câu 10 (Dashboard)** | Dot plot + bảng Top 5 SP trả hàng cao nhất (Câu 9); Dashboard tương tác Plotly HTML (Câu 10) |
| **TV7** | | Storytelling, Slide & Phản biện | **Câu 10 (3 Đề xuất)** + **Slide & Script** | Slide Master; 3 đề xuất giảm hủy/trả gắn số liệu; nội dung Slide, kịch bản 10–12 phút & Q&A |

---

## 3. Nhiệm vụ chi tiết từng thành viên

### TV1 — Trưởng nhóm & Tổng quan (Câu 1 + Mở đầu)
- **Việc cần làm**:
  - Phối hợp TV2 chốt công thức tính KPI chuẩn và chia cho cả nhóm ở Mốc 1.
  - Phối hợp TV7 chốt Style Guide (bảng màu, font, cỡ chữ) và điều phối deadline.
  - Thực hiện **Câu 1**: Thẻ KPI tổng quan (tổng số đơn, tổng doanh thu Gross & Delivered, tổng phí vận chuyển, tỉ lệ đủ **5 trạng thái**: `Delivered`, `Shipped`, `Pending`, `Returned`, `Cancelled`).
  - Viết phần **Mở đầu slide**: bối cảnh bài toán, nguồn Kaggle (`rohiteng/amazon-sales-dataset`), lưu ý dữ liệu tổng hợp (synthetic).
  - Kiểm tra chéo cuối cùng: đảm bảo số liệu giữa Câu 1–9, Dashboard và Slide khớp 100%.
- **Bàn giao**: Code/biểu đồ `q01_kpi.png` + Slide mở đầu + Checklist duyệt bài.

### TV2 — Làm sạch dữ liệu & Xu hướng thời gian (Cleaning + Câu 2)
- **Việc cần làm**:
  - **Ưu tiên làm sớm nhất (Mốc 1)**: Kiểm tra `data/raw/Amazon.csv` (missing, duplicates, kiểu `OrderDate`, kiểm chứng công thức `TotalAmount`, kiểm tra ngoại lệ theo quy tắc IQR, ghi nhận lỗi synthetic như `City/State` lệch `Country` và `ProductName` lệch `Category`).
  - Xuất `data/processed/Amazon_clean.csv` (có sẵn cột `Year`, `Month`, `YearMonth`) và bảng tóm tắt quy trình làm sạch (**Cleaning Log**).
  - Thực hiện **Câu 2**: Doanh thu và số đơn theo tháng và theo năm (2020–2024).
- **Lưu ý kỹ thuật**: **Không dùng biểu đồ 2 trục Y (dual-axis)** theo Chương 2 Slide 41 → dùng **2 biểu đồ đường xếp dọc cùng trục thời gian** (trên: Doanh thu, dưới: Số đơn) kèm biểu đồ cột tổng theo năm và chú thích tháng cao nhất/thấp nhất.
- **Bàn giao**: Script `01_clean_and_eda.py` + `Amazon_clean.csv` + `cleaning_summary.json` + `q02_trend.png`.

### TV3 — Cơ cấu trạng thái & Doanh thu sản phẩm (Câu 3 + Câu 4)
- **Việc cần làm**:
  - **Câu 3**: Cơ cấu **5 trạng thái đơn** (`Delivered`, `Shipped`, `Pending`, `Returned`, `Cancelled`). Để không lặp lại Câu 1, vẽ **cột chồng 100% theo năm (2020–2024)** kèm biểu đồ so sánh tỉ trọng **Số đơn** vs **Giá trị doanh thu thất thoát** (`Cancelled + Returned`).
  - **Câu 4**: Doanh thu theo nhóm sản phẩm. Vì dữ liệu thật chỉ có **6 `Category`**, vẽ **cột ngang xếp hạng đầy đủ 6 `Category`** và bổ sung một panel nhỏ **Top 10 `ProductName`** (hoặc 10 `Brand`) theo doanh thu để trả lời trọn vẹn yêu cầu đề.
- **Bàn giao**: Code + `q03_order_status.png` + `q04_category_revenue.png` + phần thuyết minh (số liệu, lý do chọn biểu đồ, kết luận, đề xuất).

### TV4 — Phân tích khu vực & Chi phí vận chuyển (Câu 5 + Câu 7)
- **Việc cần làm**:
  - **Câu 5**: Doanh thu theo khu vực khách hàng — dùng cột **`Country` (5 quốc gia)**. Vẽ **cột ngang xếp hạng** (ưu tiên đọc chính xác chênh lệch, Mỹ chiếm ~70%) kết hợp **bản đồ Choropleth (Plotly/ảnh tĩnh)** để minh họa phân bố địa lý.
  - **Câu 7**: Gồm 2 ý rõ ràng:
    - *(7a)* Chi phí vận chuyển theo quốc gia: dùng **Boxplot / Boxenplot** (`Seaborn`) cho thấy trung vị, tứ phân vị và mức chênh lệch giữa 5 nước.
    - *(7b)* Chi phí vận chuyển theo giá trị đơn (`TotalAmount`): do có 100.000 điểm dễ chồng đặc (*overplotting*), dùng **Hexbin / Scatter có `alpha` thấp (hoặc mẫu phân tầng)** kèm đường hồi quy và hệ số tương quan $r$.
- **Bàn giao**: Code + `q05_region_revenue.png` + `q07_shipping_cost.png` + phần thuyết minh đầy đủ.

### TV5 — Phân tích sâu Hủy & Trả hàng (Câu 6 + Câu 8) *(Trọng tâm thuyết trình)*
- **Việc cần làm**:
  - **Câu 6**: Tỉ lệ hủy và trả hàng theo **6 nhóm sản phẩm (`Category`)** — **tách rõ `Cancel Rate %` và `Return Rate %`** (dùng cột nhóm xếp hạng hoặc dumbbell chart, kèm đường trung bình chung).
  - **Câu 8**: Hình thức thanh toán (`6 PaymentMethod`) và tỉ lệ hủy/trả hàng — **cột nhóm xếp hạng** tách `Cancel %` và `Return %`, tô màu cảnh báo phương thức rủi ro cao nhất.
  - Làm việc trực tiếp với TV6 và TV7 để cung cấp số liệu cốt lõi cho 3 đề xuất ở Câu 10.
- **Bàn giao**: Code + `q06_cancel_return_category.png` + `q08_payment_cancel_return.png` + phần thuyết minh đầy đủ.

### TV6 — Số liệu cụ thể sản phẩm & Dashboard tổng hợp (Câu 9 + Câu 10 Dashboard)
- **Việc cần làm**:
  - **Câu 9**: Top 5 sản phẩm có tỉ lệ trả hàng cao nhất. Nêu rõ quy tắc đặt ngưỡng số đơn tối thiểu (vd: `n >= 1.000` đơn; giải thích thực tế 50 sản phẩm đều có 1.910–2.098 đơn nên đủ độ tin cậy). Vẽ **Dot plot (Lollipop) kèm bảng số liệu cụ thể** (Tên SP, Số đơn, Số đơn trả, Tỉ lệ trả %, Giá trị hoàn trả).
  - **Câu 10 (Dashboard)**: Dựng **Dashboard tương tác HTML bằng Plotly** (dùng `Amazon_clean.csv`, không cần chờ TV1–5 gửi ảnh). Bố cục theo nguyên tắc Shneiderman: hàng trên cùng là KPI (góc trên trái), giữa là xu hướng + cơ cấu hủy/trả, dưới là Top sản phẩm rủi ro + bản đồ/quốc gia; có hover tooltip, chú thích trực tiếp và nút lọc tương tác.
- **Bàn giao**: Code + `q09_top5_return.png` + `outputs/dashboard/q10_dashboard.html` (kèm ảnh chụp chèn slide).

### TV7 — Storytelling, 3 Đề xuất, Slide & Phản biện (Câu 10 Đề xuất + Slide + Script/Q&A)
- **Việc cần làm**:
  - **Mốc 1**: Thiết kế **Slide Master** thống nhất font & bảng màu với `style_guide.py` (cùng TV1).
  - **Mốc 2–3**: Tổng hợp số liệu từ TV5 & TV6 để xây dựng **3 đề xuất giảm hủy/trả hàng khả thi** (mỗi đề xuất gắn rõ: *Vấn đề từ số liệu câu nào → Hành động cụ thể → Tác động kỳ vọng*).
  - Biên tập trọn bộ **Slide thuyết trình** và viết **Kịch bản thuyết trình 10–12 phút** (cấu trúc nhấn mạnh 4 câu trọng tâm + chia lời thoại từng người) cùng **Bộ câu hỏi phản biện Q&A** (giải thích cách chọn biểu đồ theo Chương 1–2 và nguồn/cách tính số liệu).
  - Ghi rõ **Hạn chế của dữ liệu synthetic** ở slide cuối (tăng điểm phản biện).
- **Bàn giao**: Slide hoàn chỉnh + `docs/slide_content.md` + `docs/thuyet_trinh_va_qa.md`.

---

## 4. Quy chuẩn chung (Bắt buộc áp dụng cho mọi câu hỏi)

### 4.1. Style Guide thống nhất (theo 5 hướng dẫn Chương 2)
- **Bảng màu *Start with gray***:
  - Nền dữ liệu mặc định (xám): `#B0B8C1`
  - Màu nhấn chính (Teal): `#0F766E`
  - Màu cảnh báo / Hủy & Trả hàng (Đỏ cam): `#DC2626`
  - Màu nhấn phụ (Vàng hổ phách — dùng cho `Pending`/trung bình): `#D97706`
  - Chữ chính / Tiêu đề: `#1F2937` · Chú thích phụ: `#6B7280`
- **Bố cục chuẩn**: Nền trắng, tắt khung trên & phải (`sns.despine()`), tắt lưới hoặc lưới mảnh màu nhạt, trục biểu đồ cột luôn bắt đầu từ `0`, xuất ảnh `dpi=300` với `bbox_inches="tight"`.
- **Chữ gắn với hình**: Tiêu đề nêu **kết luận** (active title), phụ đề ghi đơn vị/phạm vi, nhãn số đặt **trực tiếp** lên cột/đường, góc dưới ghi nguồn `Nguồn: Kaggle Amazon Sales Dataset (synthetic, n=100.000)`.

### 4.2. Mẫu nộp bài cho mỗi câu hỏi (TV1–TV6 đều điền đủ 4 mục)
1. **Số liệu cụ thể**: Các con số chính (tổng, trung bình, %, xếp hạng, chênh lệch).
2. **Biểu đồ PNG (300 DPI)** + đoạn code tái lập.
3. **Lý do chọn biểu đồ** (1–2 câu dẫn chiếu Chương 1–2, vd: vì sao chọn cột ngang/dot plot thay vì pie/cột đứng).
4. **Insight hành động**: 1 tiêu đề chủ động + 1 câu kết luận có số liệu + 1 đề xuất hành động.

---

## 5. Lộ trình phối hợp 3 mốc (Tránh dồn việc phút chót)

| Mốc | Nội dung hoàn thành | Người thực hiện |
|---|---|---|
| **Mốc 1 — Chuẩn hóa nền** | Chốt công thức KPI · Làm sạch & xuất `Amazon_clean.csv` + Cleaning Log · Chốt `style_guide.py` & Slide Master | TV1, TV2, TV7 |
| **Mốc 2 — Phân tích & Vẽ 10 câu** | Hoàn thành biểu đồ + thuyết minh Câu 1–9 · Dựng khung Dashboard HTML Câu 10 | TV1–TV6 (song song) · TV7 lên khung slide |
| **Mốc 3 — Ghép bài & Tập nói** | Hoàn thiện Dashboard + 3 đề xuất · Kiểm tra chéo 100% số liệu · Hoàn chỉnh Slide, Script 10–12 phút & duyệt Q&A | Cả nhóm (TV1, TV6, TV7 chốt cuối) |

---

## 6. Phân bổ thuyết trình 10–12 phút (Gợi ý)

| Phần | Thời lượng | Nội dung trọng tâm | Người nói gợi ý |
|---|---|---|---|
| 1. Mở đầu & Làm sạch | 1,5 phút | Bối cảnh, nguồn synthetic, tóm tắt làm sạch & lưu ý dữ liệu thật | TV1 + TV2 |
| 2. Tổng quan & Xu hướng (Câu 1, 2, 3) | 2,0 phút | KPI chính, xu hướng 2020–2024, cơ cấu 5 trạng thái (**nhấn thất thoát hủy/trả**) | TV2 + TV3 |
| 3. Sản phẩm, Khu vực & Vận chuyển (Câu 4, 5, 7) | 2,0 phút | Top nhóm hàng, 5 quốc gia, phân phối phí vận chuyển | TV3 + TV4 |
| 4. **Đào sâu Hủy & Trả hàng — Câu 6, 8, 9 (Trọng tâm)** | **3,5 phút** | **Nhấn sâu**: nhóm hàng, thanh toán và Top 5 sản phẩm trả hàng cao nhất | TV5 + TV6 |
| 5. **Demo Dashboard HTML & 3 Đề xuất (Câu 10)** | **2,5 phút** | Demo trực tiếp file HTML tương tác + 3 đề xuất khả thi & hạn chế dữ liệu | TV6 + TV7 |
| **Tổng cộng** | **11,5 phút** | Vừa khít khung **10–12 phút**, dư thời gian chuyển cảnh | **Cả 7 thành viên đều có phần** |
