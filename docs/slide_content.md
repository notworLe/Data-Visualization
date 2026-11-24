# NỘI DUNG SLIDE THUYẾT TRÌNH (15 SLIDES — 10 ĐẾN 12 PHÚT)

> **Hướng dẫn dùng file này**: TV7 (và các thành viên) có thể dùng trực tiếp để đọc thuyết trình kèm notebook [Amazon_Sales_Presentation.ipynb](../notebooks/Amazon_Sales_Presentation.ipynb), hoặc copy từng khối nội dung vào PowerPoint/Canva và chèn đúng ảnh PNG (300 DPI) trong `outputs/charts/`. Mọi con số đã đối chiếu 100% với `data/processed/kpi_metrics.json`.
>
> **4 câu nhấn mạnh sâu trong bài nói** *(theo Slide 29 đề bài)*: **Câu 3** (Thất thoát \$5,63M kéo dài 5 năm) → **Câu 6** (Hủy/trả theo nhóm hàng) → **Câu 8** (Thanh toán & thiệt hại tiền mặt) → **Câu 9** (Top 5 sản phẩm trả cao nhất), dẫn trực tiếp tới **Câu 10** (Dashboard + 3 đề xuất).

---

## SLIDE 1 — TRANG BÌA (TV1)
- **Tiêu đề lớn**: PHÂN TÍCH ĐƠN HÀNG, VẬN CHUYỂN & TỐI ƯU TỈ LỆ HỦY/TRẢ HÀNG
- **Phụ đề**: Bài tập lớn Trực quan hóa dữ liệu · Dataset 8: Amazon Sales Dataset (Synthetic, 2020–2024)
- **Thông tin nhóm**: Nhóm […] (7 thành viên) · Công cụ: Python (`pandas`, `Matplotlib`, `Seaborn`, `Plotly HTML`)
- **Thiết kế gợi ý**: Nền trắng/xám sáng, nhấn 1 thanh dọc màu Teal `#0F766E` đồng bộ Style Guide toàn bài.

---

## SLIDE 2 — BỐI CẢNH, MỤC TIÊU & NGUỒN DỮ LIỆU (TV1)
- **Tiêu đề chủ động**: Bài toán vận hành trên 100.000 giao dịch TMĐT (2020–2024): Tập trung kiểm soát thất thoát hủy & trả hàng
- **Nội dung chính (3 khối ngắn)**:
  1. **Người xem & Mục tiêu** *(Chương 2.1)*: Ban quản lý vận hành & kinh doanh TMĐT — cần cái nhìn tổng quan doanh thu/chi phí vận chuyển và 3 giải pháp thực tế giảm tỉ lệ hủy, trả hàng.
  2. **Nguồn dữ liệu & Phạm vi**:
     - Kaggle: `rohiteng/amazon-sales-dataset` (`Amazon.csv`, 17,4 MB, cập nhật 11/2025).
     - Quy mô: **100.000 đơn hàng × 20 cột**, 43.233 khách hàng, 1.999 người bán, 50 sản phẩm, 6 nhóm hàng, 5 quốc gia, từ `01/01/2020` đến `29/12/2024`.
  3. **Lưu ý đạo đức & tính trung thực** *(Slide 5 & 23)*: Đây là **dữ liệu tổng hợp (synthetic)** phục vụ học thuật, **không phản ánh hoạt động thực tế của Amazon**.

---

## SLIDE 3 — QUY TRÌNH 7 BƯỚC, LÀM SẠCH & STYLE GUIDE (TV2)
- **Tiêu đề chủ động**: Dữ liệu sạch 0 lỗi thiếu/trùng, khớp công thức 100% — phát hiện 4 điểm khác biệt quan trọng khi mở tệp thật
- **Cột trái — Nhật ký làm sạch (`01_clean_and_eda.py`)**:
  - **Thiếu & Trùng lặp**: 0 giá trị thiếu, 0 dòng trùng, 0 ngày lỗi định dạng.
  - **Kiểm định công thức**: `TotalAmount = Quantity × UnitPrice × (1 - Discount) + Tax + ShippingCost` khớp **100%** (sai số làm tròn tối đa \$0,01).
  - **Ngoại lệ IQR** *(Chương 2 Slide 20)*: `TotalAmount` có **1.360 dòng (1,36% > \$2.863,08)** → **giữ nguyên** vì đều là đơn mua số lượng 4–5 với đơn giá cao hợp lệ.
  - **Chuẩn hóa KPI chung**: Gross Revenue = `sum(TotalAmount)`; tách riêng `Cancel %` và `Return %`.
- **Cột phải — 4 phát hiện từ tệp thật & Style Guide**:
  - **4 phát hiện**: (1) Có **5 trạng thái** (thêm `Pending` = 4.103 đơn); (2) Chỉ có **6 `Category`** (bổ sung Top 10 SKU ở Câu 4); (3) `City/State` Mỹ bị ghép ngẫu nhiên với cả 5 nước → phân tích địa lý theo **`Country`**; (4) `ProductName` gán độc lập với `Category` (ghi vào hạn chế).
  - **5 hướng dẫn thiết kế** *(Chương 2.7)*: Cho thấy dữ liệu · Giảm nhiễu (`despine`) · Tiêu đề chủ động + nhãn trực tiếp · Tránh spaghetti/dual-axis · **Bắt đầu từ màu xám** (Xám `#94A3B8` nền, Teal `#0F766E` chính, Đỏ `#DC2626` cảnh báo).

---

## SLIDE 4 — CÂU 1: TỔNG QUAN KPI & TỈ LỆ TRẠNG THÁI ĐƠN (TV1)
- **Hình chèn**: `outputs/charts/q01_kpi.png`
- **Tiêu đề chủ động**: 100.000 đơn hàng tạo \$91,83M doanh thu gộp — nhưng \$5,63M (6,13%) bị thất thoát do hủy & trả hàng
- **Số liệu cụ thể**:
  - Tổng đơn: **100.000** · Doanh thu gộp: **\$91,83M** (AOV = **\$918,26**, trung vị **\$714,32**) · Thực giao (`Delivered`): **\$68,37M (74,46%)**.
  - Tổng phí vận chuyển: **\$740,7K** (TB **\$7,41/đơn**, chỉ chiếm **0,81%** doanh thu).
  - 5 trạng thái: `Delivered` **74,63%** (74.628) · `Shipped` **15,19%** (15.192) · `Pending` **4,10%** (4.103) · `Returned` **3,05%** (3.049) · `Cancelled` **3,03%** (3.028).
- **Lý do chọn biểu đồ**: Thẻ KPI (4 chỉ số cốt lõi đặt góc trên trái theo F-pattern Chương 1) kết hợp thanh tỉ trọng 100% có nhãn trực tiếp giúp đọc tổng quan trong 5 giây.
- **Kết luận**: Chi phí vận chuyển rất nhỏ (0,81% DT), trong khi thất thoát hủy/trả lên tới **\$5,63M** (gấp **7,6 lần** tổng chi phí vận chuyển).
- **Đề xuất hành động**: Đặt giảm tỉ lệ hủy/trả hàng làm ưu tiên số 1 thay vì cắt giảm đơn giá phí vận chuyển.

---

## SLIDE 5 — CÂU 2: XU HƯỚNG DOANH THU & SỐ ĐƠN THEO THÁNG VÀ NĂM (TV2)
- **Hình chèn**: `outputs/charts/q02_trend.png`
- **Tiêu đề chủ động**: Doanh thu ổn định quanh \$18,4M/năm (~20.000 đơn/năm); đáy lặp lại mỗi tháng 2 do hiệu ứng ít ngày
- **Số liệu cụ thể**:
  - Theo năm: Cao nhất **2020** (**\$18,53M** · 20.066 đơn) và **2023** (**\$18,51M** · 20.096 đơn); thấp nhất **2024** (**\$18,17M** · 19.870 đơn; chênh đỉnh–đáy chỉ 1,96%).
  - Theo 60 tháng: Đỉnh doanh thu **2024-05** (**\$1,64M** · 1.753 đơn), đỉnh số đơn **2020-08** (**1.783 đơn**); đáy ở **2020-02** (**\$1,34M** · 1.490 đơn). Hệ số biến thiên CV chỉ **4,21%**.
  - Trung bình tháng 2 (5 năm): **\$1,39M/tháng**, thấp hơn ~10–12% so với các tháng 31 ngày (\$1,55M–\$1,58M).
- **Lý do chọn biểu đồ**: Biểu đồ đường phù hợp chuỗi thời gian liên tục (60 tháng); **tách 2 panel xếp dọc** để tránh lỗi **2 trục Y (dual-axis)** *(Chương 2 Slide 41)*, kết hợp cột gốc 0 cho tổng theo năm.
- **Kết luận**: Doanh thu gần như đi ngang suốt 5 năm và không có đột biến mùa lễ Q4 (đặc trưng dữ liệu tổng hợp phân bố đều theo ngày).
- **Đề xuất hành động**: Chuẩn hóa KPI theo **doanh thu bình quân mỗi ngày** (để đánh giá tháng 2 công bằng) và tập trung cải thiện biên lợi nhuận/giữ đơn thay vì chờ tăng trưởng tự nhiên theo mùa.

---

## SLIDE 6 — CÂU 3 ⭐ (TRỌNG TÂM 1/4): CƠ CẤU TRẠNG THÁI ĐƠN QUA 5 NĂM (TV3)
- **Hình chèn**: `outputs/charts/q03_order_status.png`
- **Tiêu đề chủ động**: Cơ cấu 5 trạng thái bất biến suốt 5 năm — riêng đơn hủy có giá trị trung bình cao nhất (\$942/đơn)
- **Số liệu cụ thể**:
  - `Delivered` dao động rất hẹp từ **74,42% (2023)** đến **74,95% (2020)**; tổng `Hủy + Trả` cố định quanh **5,83%–6,16%/năm** ($\chi^2 = 14,19, p = 0,585$).
  - `Cancelled`: 3.028 đơn (3,03%) nhưng AOV cao nhất (**\$941,59** so với \$916,18 của `Delivered`) → mất **\$2,85M (3,10% DT)**.
  - `Returned`: 3.049 đơn (3,05%, AOV \$911,99) → mất **\$2,78M (3,03% DT)**.
- **Lý do chọn biểu đồ**: Cột chồng 100% theo năm mở rộng chiều thời gian (tránh lặp Câu 1) + cột ngang xếp hạng đọc độ dài chính xác hơn donut/pie theo **thang Cleveland–McGill** *(Chương 1)*.
- **Kết luận**: Thất thoát **\$5,63M** không phải sự cố nhất thời mà là **rò rỉ mang tính hệ thống kéo dài 5 năm**, nghiêm trọng hơn ở nhóm đơn hủy giá trị cao.
- **Đề xuất hành động**: Thiết lập quy trình xác nhận ưu tiên cho **đơn hàng giá trị cao (> \$900)** trước khi xuất kho nhằm chặn nhóm hủy gây thiệt hại lớn nhất.

---

## SLIDE 7 — CÂU 4: DOANH THU THEO NHÓM SẢN PHẨM & TOP 10 SKU (TV3)
- **Hình chèn**: `outputs/charts/q04_category_revenue.png`
- **Tiêu đề chủ động**: Electronics dẫn đầu 6 nhóm hàng (\$15,58M); Top 10 sản phẩm đóng góp \$1,88M–\$1,94M mỗi SKU
- **Số liệu cụ thể**:
  - **6 `Category`** phân bố cực kỳ cân bằng (chênh đỉnh–đáy chỉ **\$420,3K / +2,77%**):
    1. `Electronics`: **\$15,58M** (16,97% · 16.853 đơn) · 2. `Sports & Outdoors`: **\$15,35M** (16,71%) · 3. `Books`: **\$15,26M** (16,62%) · 4. `Clothing`: **\$15,25M** (16,61%) · 5. `Toys & Games`: **\$15,22M** (16,57%) · 6. `Home & Kitchen`: **\$15,16M** (16,51%).
  - **Top 5 SKU doanh thu cao nhất**: `Memory Card 128GB` (**\$1,94M**), `LED Desk Lamp` (**\$1,92M**), `Mechanical Keyboard` (**\$1,91M**), `Electric Kettle` (**\$1,91M**), `Smartwatch` (**\$1,90M**). Đáng chú ý: **`Dress Shirt`** đứng Top 6 doanh thu (**\$1,90M**) nhưng cũng nằm **Top 3 trả hàng**!
- **Lý do chọn biểu đồ**: Cột ngang xếp hạng (trục bắt đầu từ 0) giúp nhãn tên dài dễ đọc và so sánh độ dài chuẩn xác; bổ sung panel Top 10 sản phẩm để giải quyết trọn vẹn yêu cầu đề khi tệp chỉ có 6 Category.
- **Kết luận**: Doanh thu không phụ thuộc vào một nhóm hàng đơn lẻ, tạo nền tảng danh mục cân bằng để tối ưu từng nhóm SKU chủ lực.
- **Đề xuất hành động**: Rà soát ngay các SKU vừa có doanh thu cao vừa có rủi ro hoàn trả lớn (điển hình `Dress Shirt`) để bảo toàn doanh thu ròng.

---

## SLIDE 8 — CÂU 5: DOANH THU THEO KHU VỰC KHÁCH HÀNG (TV4)
- **Hình chèn**: `outputs/charts/q05_region_revenue.png` *(kèm bản đồ tương tác `outputs/dashboard/q05_country_map.html`)*
- **Tiêu đề chủ động**: Hoa Kỳ chiếm áp đảo 70,0% tổng doanh thu (\$64,31M) — gấp 2,34 lần 4 thị trường còn lại cộng lại
- **Số liệu cụ thể**:
  - 1. **United States**: **\$64,31M** (**70,03%** · 70.058 đơn · AOV \$917,95)
  - 2. **India**: **\$13,88M** (**15,11%** · 15.051 đơn · AOV \$921,92 — cao nhất)
  - 3. **Canada**: **\$5,32M** (5,80% · 5.818 đơn) · 4. **United Kingdom**: **\$4,53M** (4,93% · 4.943 đơn) · 5. **Australia**: **\$3,79M** (4,13% · 4.130 đơn).
- **Lý do chọn biểu đồ**: Cột ngang xếp hạng (trục từ 0) thể hiện chính xác độ chênh lệch gấp 17 lần giữa Mỹ và Úc (tốt hơn bản đồ đơn lẻ vốn dễ bị diện tích địa lý làm nhiễu — Chương 2 Slide 38), kết hợp Dot plot AOV và bản đồ Choropleth tương tác.
- **Kết luận**: AOV giữa 5 quốc gia gần như bằng nhau (\$915–\$922) → chênh lệch doanh thu 100% đến từ quy mô số đơn; rủi ro phụ thuộc thị trường Mỹ rất cao (70%).
- **Đề xuất hành động**: Ưu tiên thử nghiệm các chương trình chống hủy/trả tại **Mỹ & Ấn Độ** (chiếm **85,1% tổng quy mô**) để tối đa hóa tác động, đồng thời đẩy mạnh tăng lượng đơn ở Canada/UK/Úc.

---

## SLIDE 9 — CÂU 6 ⭐ (TRỌNG TÂM 2/4): TỈ LỆ HỦY & TRẢ HÀNG THEO NHÓM SẢN PHẨM (TV5)
- **Hình chèn**: `outputs/charts/q06_cancel_return_category.png`
- **Tiêu đề chủ động**: Home & Kitchen dẫn đầu tổng Hủy+Trả (6,27% · \$984K); Electronics dẫn đầu riêng tỉ lệ Hủy (3,23%)
- **Số liệu cụ thể** *(TB toàn sàn: Hủy 3,03% · Trả 3,05% · Gộp 6,08%)*:
  - **Cao nhất tổng Hủy+Trả**: `Home & Kitchen` (**6,27%** = Hủy 3,06% + Trả **3,21%** cao nhất · thất thoát **\$984,1K**).
  - **Cao nhất tỉ lệ Hủy**: `Electronics` (**3,23%** = 544 đơn hủy), nhưng có tỉ lệ Trả thấp nhất (**2,82%**).
  - Các nhóm còn lại: `Books` (6,11% · \$931,5K), `Toys & Games` (6,09% · \$963,4K), `Sports & Outdoors` (6,04% · \$911,4K), thấp nhất `Clothing` (5,91% · \$920,7K).
  - Kiểm định thống kê: $\chi^2 = 2,05, p = 0,842$ → chênh lệch biên độ hẹp, vấn đề xảy ra trên toàn danh mục.
- **Lý do chọn biểu đồ**: Cột nhóm ngang tách riêng `Cancel %` và `Return %` (thay vì gộp chung) vì hủy đơn xảy ra *trước giao* còn trả hàng xảy ra *sau giao*; kết hợp panel tiền thất thoát để thấy rõ trọng lượng tài chính.
- **Kết luận**: Cần chiến lược **2 mũi nhọn**: đánh mặt bằng chung toàn sàn, đồng thời ưu tiên giảm **trả hàng** ở `Home & Kitchen` và giảm **hủy trước giao** ở `Electronics`.
- **Đề xuất hành động**: Siết kiểm tra đóng gói chống vỡ/mô tả kích thước cho `Home & Kitchen` và rút ngắn thời gian xác nhận/xuất kho cho `Electronics`.

---

## SLIDE 10 — CÂU 7: CHI PHÍ VẬN CHUYỂN THEO KHU VỰC & GIÁ TRỊ ĐƠN (TV4)
- **Hình chèn**: `outputs/charts/q07_shipping_cost.png`
- **Tiêu đề chủ động**: Phí ship cố định quanh \$7,4/đơn ở mọi nước (p = 0,57) và gần độc lập với giá trị đơn (r = 0,04) — đơn nhỏ <\$250 chịu gánh nặng gấp 18 lần
- **Số liệu cụ thể**:
  - **Theo quốc gia**: Trung bình **\$7,33** (UK) đến **\$7,46** (Canada); trung vị \$7,14–\$7,38; Q1 ≈ \$3,7, Q3 ≈ \$11,2 (ANOVA $F = 0,733, p = 0,569$ → đồng nhất). Tổng phí lớn nhất ở Mỹ (\$519,1K).
  - **Theo giá trị đơn**: Tương quan Pearson $r = 0,039$ (độ dốc \$0,0002/\$1 đơn) — gần như không phụ thuộc giá trị đơn.
  - **Gánh nặng theo phân khúc**: Đơn **`<\$250`** (17.941 đơn) trả phí TB \$6,77 nhưng chiếm tới **6,86% giá trị đơn** — cao gấp **18 lần** đơn **`>\$1.500`** (TB \$7,57 nhưng chỉ chiếm **0,38%**).
- **Lý do chọn biểu đồ**: Boxplot (`Seaborn`) tóm tắt đủ 5 số phân phối theo nhóm quốc gia; **Hexbin mật độ** thay cho Scatter thô để chống chồng điểm trên 100.000 dòng, kèm cột gốc 0 cho tỉ lệ phí/giá trị đơn.
- **Kết luận**: Biểu phí phẳng (\$0–\$15) tạo bất lợi rõ rệt cho nhóm đơn hàng nhỏ `<\$250`.
- **Đề xuất hành động**: Áp dụng **ngưỡng miễn phí vận chuyển (Free-ship) từ \$250** để khuyến khích khách gộp giỏ hàng, vừa tăng AOV vừa giảm tâm lý hủy đơn nhỏ vì phí ship.

---

## SLIDE 11 — CÂU 8 ⭐ (TRỌNG TÂM 3/4): HÌNH THỨC THANH TOÁN & RỦI RO HỦY/TRẢ (TV5)
- **Hình chèn**: `outputs/charts/q08_payment_cancel_return.png`
- **Tiêu đề chủ động**: COD có tỉ lệ hủy cao nhất (3,17%), nhưng Credit Card gây thất thoát lớn nhất (\$1,99M · 35,3% toàn sàn)
- **Số liệu cụ thể**:
  - **Theo tỉ lệ %** ($\chi^2 = 2,48, p = 0,779$):
    - Tỉ lệ **Hủy** cao nhất: **`Cash on Delivery` (3,17%)** · `Credit Card` (3,09%) · `Amazon Pay` (3,07%).
    - Tỉ lệ **Trả** cao nhất: **`Net Banking` (3,15%)** · `Amazon Pay` (3,14%).
    - Thấp nhất tổng Hủy+Trả: **`UPI` (5,85%)** (cao nhất: `Amazon Pay` **6,21%**, `Credit Card` **6,16%**).
  - **Theo tiền thất thoát thực tế**:
    - **`Credit Card`** (35,0% tổng đơn): **\$1,99M** (2.158 đơn) — lớn nhất toàn sàn.
    - **`Debit Card`** (20,0% đơn): **\$1,12M** (1.202 đơn). Riêng **2 loại thẻ chiếm 55,1% tổng tiền thất thoát (\$3,10M)**!
    - `COD` chỉ chiếm 4,9% đơn → thất thoát \$279,3K.
- **Lý do chọn biểu đồ**: Cột nhóm ngang tách `Cancel %` vs `Return %` đặt cạnh cột **Tiền thất thoát ($M)** giúp người ra quyết định thấy đủ cả *rủi ro tương đối (%)* lẫn *tác động tuyệt đối ($)*.
- **Kết luận**: Nếu chỉ nhìn tỉ lệ % dễ tập trung sai chỗ vào mỗi COD; thực tế cải thiện luồng **Credit/Debit Card** mới tạo ra tác động tiền mặt lớn nhất.
- **Đề xuất hành động**: Áp dụng xác thực OTP cho `COD` (giảm hủy ảo) đồng thời tối ưu bước rà soát đơn/đổi hàng thay hoàn tiền trên `Credit Card` & `Debit Card`, khuyến khích `UPI` (rủi ro thấp nhất 5,85%).

---

## SLIDE 12 — CÂU 9 ⭐ (TRỌNG TÂM 4/4): TOP 5 SẢN PHẨM TRẢ HÀNG CAO NHẤT (TV6)
- **Hình chèn**: `outputs/charts/q09_top5_return.png`
- **Tiêu đề chủ động**: Yoga Mat (3,97%) dẫn đầu Top 5 sản phẩm trả hàng nhiều nhất — gây \$334K giá trị hoàn trả
- **Quy tắc lọc minh bạch**: Đặt ngưỡng tối thiểu **`n >= 1.000` đơn/SKU** để loại nhiễu mẫu nhỏ; thực tế **50/50 sản phẩm đều đạt** (1.910–2.098 đơn/SKU).
- **Bảng số liệu cụ thể Top 5** *(TB toàn sàn: 3,05% · Thấp nhất: `Bluetooth Speaker` 2,20%)*:
  1. **`Yoga Mat` (`P00024`)**: **3,97%** (81 / 2.041 đơn · hoàn trả **\$72.690** — cao hơn TB sàn +0,92 đpt).
  2. **`Noise Cancelling Headphones` (`P00012`)**: **3,79%** (77 / 2.031 đơn · hoàn trả **\$65.089**).
  3. **`Dress Shirt` (`P00030`)**: **3,59%** (72 / 2.007 đơn · hoàn trả **\$76.637** · *kèm hủy 3,74% → tổng 7,33%*).
  4. **`Cookware Set` (`P00023`)**: **3,55%** (73 / 2.058 đơn · hoàn trả **\$62.937**).
  5. **`Webcam Full HD` (`P00041`)**: **3,53%** (71 / 2.013 đơn · hoàn trả **\$56.648**).
  - **Tổng Top 5**: **374 đơn trả** · **\$334.001** (chiếm **12,0%** tổng giá trị trả toàn sàn dù chỉ là 10% SKU).
- **Lý do chọn biểu đồ**: **Dot plot (Lollipop)** + bảng số liệu chi tiết *(Chương 2 Slide 29)* — lý tưởng khi các giá trị tỉ lệ nằm sát nhau (3,5%–4,0%) và cần so trực tiếp với đường trung bình 3,05%.
- **Kết luận**: Có sự phân hóa gần **1,8 lần** giữa SKU trả cao nhất (`Yoga Mat` 3,97%) và thấp nhất (`Bluetooth Speaker` 2,20%); `Dress Shirt` là điểm nóng kép cần xử lý ngay.
- **Đề xuất hành động**: Kiểm định chất lượng lô hàng, bổ sung hướng dẫn chọn size/thông số chi tiết và video thực tế cho Top 5 SKU này.

---

## SLIDE 13 — CÂU 10 (PHẦN A): DEMO DASHBOARD TƯƠNG TÁC HTML (TV6)
- **Hình chèn (dự phòng)**: `outputs/charts/q10_dashboard_preview.png`
- **Demo trực tiếp khi thuyết trình**: Mở `outputs/dashboard/q10_dashboard.html` bằng Chrome/Edge.
- **Tiêu đề chủ động**: Dashboard tương tác Plotly HTML: Từ tổng quan KPI đến chi tiết điểm nóng hủy/trả hàng trong 1 màn hình
- **Điểm nổi bật về thiết kế** *(Chương 1 & Chương 3.4)*:
  - Tuân thủ **nguyên tắc Shneiderman**: Hàng trên là 4 thẻ KPI tổng quan → giữa là Xu hướng (có **dropdown lọc năm** & **range slider**) + Bản đồ Choropleth thế giới → dưới là 4 biểu đồ chẩn đoán Hủy/Trả + Khung 3 đề xuất hành động.
  - Mọi biểu đồ đều có **hover tooltip** chi tiết, zoom/pan và giữ thống nhất bảng màu *Start-with-gray* toàn dự án.

---

## SLIDE 14 — CÂU 10 (PHẦN B): 3 ĐỀ XUẤT GIẢM HỦY & TRẢ HÀNG GẮN SỐ LIỆU (TV7)
- **Tiêu đề chủ động**: 3 giải pháp trọng tâm giúp kiểm soát rò rỉ \$5,63M doanh thu hủy & trả hàng
- **Trình bày dạng 3 cột hành động**:
  1. **Siết chuẩn chất lượng & mô tả cho Top 5 SKU trả cao & nhóm `Home & Kitchen`**
     - *Bằng chứng*: Top 5 SKU gây **\$334K** hoàn trả (`Yoga Mat` 3,97%, `Dress Shirt` 3,59% & hủy 3,74%); `Home & Kitchen` mất **\$984K** (6,27%).
     - *Hành động*: Chuẩn hóa bảng size/thông số, kiểm tra QC đóng gói chống hư hỏng, ưu tiên kiểm soát nhà bán có tỉ lệ hoàn cao.
     - *Kỳ vọng*: Giảm 20% hoàn trả ở Top 5 SKU → thu hồi **~\$67K** trực tiếp.
  2. **Phân luồng xác thực thanh toán theo rủi ro & giá trị đơn**
     - *Bằng chứng*: `COD` hủy cao nhất (**3,17%**); đơn hủy có AOV cao nhất (**\$942**); `Credit + Debit Card` chiếm **55,1% (\$3,10M)** tổng thiệt hại.
     - *Hành động*: Bắt buộc xác thực OTP/nhắc lịch giao cho đơn `COD` và đơn `> \$900`; bổ sung cơ chế đổi sản phẩm nhanh thay hoàn tiền cho giao dịch thẻ; khuyến khích `UPI` (rủi ro thấp nhất 5,85%).
     - *Kỳ vọng*: Giảm 0,5 điểm % tỉ lệ hủy toàn sàn → cứu **~\$460K** doanh thu.
  3. **Gói gộp đơn Free-ship ngưỡng \$250 & rút ngắn xử lý trước giao**
     - *Bằng chứng*: Đơn `< \$250` gánh phí vận chuyển **6,86% giá trị đơn** (gấp 18× đơn lớn); `Electronics` có tỉ lệ hủy trước giao cao nhất (**3,23%**).
     - *Hành động*: Áp dụng miễn phí vận chuyển từ ngưỡng \$250 để tăng AOV đơn nhỏ + hiển thị cam kết thời gian giao chính xác trước khi thanh toán.
     - *Kỳ vọng*: Giảm hủy trước xuất kho & giảm gánh nặng chi phí trên đơn nhỏ.

---

## SLIDE 15 — KẾT LUẬN, HẠN CHẾ & CẢM ƠN (TV7)
- **Tiêu đề chủ động**: Kết luận tổng thể & Minh bạch hạn chế của tập dữ liệu tổng hợp
- **3 điểm chốt lại**:
  1. Quy mô lớn và ổn định (**100.000 đơn · \$91,83M**), tập trung mạnh tại **Mỹ (70%)**, phí ship rất thấp (**0,81% DT**).
  2. Bài toán lớn nhất nằm ở **\$5,63M (6,08%)** thất thoát hủy & trả kéo dài 5 năm không đổi — cần xử lý đồng thời cả mặt bằng chung (luồng thẻ, đơn >\$900) lẫn điểm nóng SKU (`Yoga Mat`, `Dress Shirt`...).
  3. Toàn bộ quy trình làm sạch, 10 biểu đồ PNG và Dashboard Plotly HTML đều tái lập 100% bằng Python.
- **Minh bạch hạn chế dữ liệu (điểm cộng lớn khi phản biện)**:
  - Dữ liệu **tổng hợp (synthetic)**: không có mùa vụ thật, `City/State` (Mỹ) ghép ngẫu nhiên với cả 5 nước, `ProductName` gán độc lập `Category`, và không có cột *lý do trả hàng / thời gian giao thực tế*.
  - Do chênh lệch tỉ lệ hủy/trả giữa các nhóm nhỏ ($p > 0,05$), khi áp dụng thực tế doanh nghiệp cần kết hợp dữ liệu lý do hoàn hàng & đánh giá khách hàng.
- **Lời cảm ơn**: *Cảm ơn Thầy/Cô và các bạn đã lắng nghe — Nhóm xin sẵn sàng trao đổi & phản biện!*
