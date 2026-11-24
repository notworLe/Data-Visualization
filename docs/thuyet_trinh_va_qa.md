# KỊCH BẢN THUYẾT TRÌNH (10–12 PHÚT) & BỘ CÂU HỎI PHẢN BIỆN Q&A

> **Mục tiêu thời lượng**: **11 phút 30 giây** (nằm gọn trong khung 10–12 phút của Slide 29 đề bài).
> **Chiến lược trình bày**: Đi nhanh phần bối cảnh & tổng quan (Câu 1, 2, 4, 5, 7) để dành thời lượng đào sâu **4 câu trọng tâm (Câu 3, 6, 8, 9)** và **Demo sống Dashboard HTML + 3 Đề xuất (Câu 10)**.

---

## 1. Bảng phân bổ thời gian & thứ tự lên nói (7 thành viên)

| Thứ tự | Thành viên | Slide phụ trách | Thời lượng | Nhịp trình bày |
|---|---|---|---|---|
| 1 | **TV1** | Slide 1, 2, 4 (Mở đầu + Câu 1) | **1 phút 30 giây** | Tự tin, nêu rõ bài toán & 4 con số KPI chính |
| 2 | **TV2** | Slide 3, 5 (Làm sạch + Câu 2) | **1 phút 30 giây** | Nhấn 4 phát hiện từ tệp thật & đáy tháng 2 |
| 3 | **TV3** | Slide 6 ⭐, 7 (Câu 3 trọng tâm + Câu 4) | **1 phút 45 giây** | **Nhấn sâu Câu 3** (thất thoát \$5,63M kéo dài 5 năm) |
| 4 | **TV4** | Slide 8, 10 (Câu 5 + Câu 7) | **1 phút 30 giây** | Nêu gọn 70% Mỹ & gánh nặng phí ship đơn `<$250` |
| 5 | **TV5** | Slide 9 ⭐, 11 ⭐ (Câu 6 + Câu 8 trọng tâm) | **2 phút 00 giây** | **Nhấn sâu**: tách Hủy vs Trả & tác động tiền mặt Credit Card |
| 6 | **TV6** | Slide 12 ⭐, 13 (Câu 9 trọng tâm + Demo Dashboard) | **2 phút 00 giây** | **Nhấn sâu Top 5 SKU** + mở trực tiếp `q10_dashboard.html` |
| 7 | **TV7** | Slide 14, 15 (3 Đề xuất + Kết luận & Hạn chế) | **1 phút 15 giây** | Chốt mạch câu chuyện gọn, rõ số liệu kỳ vọng |
| **Tổng** | **7 TV** | **15 Slides + Live Demo** | **11 phút 30 giây** | Còn dư 30 giây dự phòng chuyển mic/màn hình |

---

## 2. Kịch bản lời thoại chi tiết (Speaker Notes)

### [00:00 – 01:30] TV1 — Slide 1, 2 & 4 (Mở đầu + Câu 1)
- **Slide 1–2 (~40s)**: *"Xin chào Thầy/Cô và các bạn. Nhóm em thực hiện bài tập lớn trực quan hóa trên **Dataset 8 — Amazon Sales Dataset**, gồm 100.000 giao dịch từ năm 2020 đến 2024. Đứng ở góc nhìn ban quản lý vận hành TMĐT, mục tiêu của nhóm không chỉ là vẽ 10 biểu đồ rời rạc, mà kể một câu chuyện dữ liệu xuyên suốt: bức tranh doanh thu đang ra sao, chi phí vận chuyển có phải điểm nghẽn không, và làm thế nào để giảm tỉ lệ hủy và trả hàng. Nhóm cũng xin lưu ý ngay từ đầu: đây là dữ liệu tổng hợp (synthetic) trên Kaggle, nên kết quả chỉ mang tính phân tích học thuật, không phản ánh Amazon thực tế."*
- **Slide 4 — Câu 1 (~50s)**: *"Bắt đầu với **Câu 1 — Tổng quan KPI**, 100.000 đơn hàng tạo ra **\$91,83 triệu** doanh thu gộp, trong đó **\$68,37 triệu (74,5%)** đã giao thành công. Điểm gây chú ý ngay trên 4 thẻ KPI là: tổng phí vận chuyển chỉ khoảng **\$740,7 nghìn** — tương đương **0,81% doanh thu**; trong khi tổng giá trị bị mất do **Hủy và Trả hàng** lên tới **\$5,63 triệu (6,13%)** — gấp hơn 7,6 lần chi phí vận chuyển. Ngoài ra, thanh tỉ trọng phía dưới cho thấy tệp dữ liệu thật có **5 trạng thái**, bổ sung thêm `Pending` chiếm 4,10%. Xin mời TV2 trình bày bước làm sạch và xu hướng thời gian."*

### [01:30 – 03:00] TV2 — Slide 3 & 5 (Làm sạch + Câu 2)
- **Slide 3 (~45s)**: *"Cảm ơn TV1. Theo quy trình 7 bước của Chương 2, trước khi vẽ nhóm đã kiểm tra toàn bộ tệp thật bằng Python (`pandas`). Dữ liệu có **0 ô thiếu, 0 dòng trùng** và công thức tính `TotalAmount` khớp 100%. Kiểm định IQR phát hiện 1,36% đơn hàng giá trị cao (> \$2.863), nhưng đều là đơn mua 4–5 sản phẩm đắt tiền hợp lệ nên nhóm **giữ nguyên** theo nguyên tắc Chương 2. Đặc biệt, việc soi kỹ tệp thật giúp nhóm phát hiện 4 điểm quan trọng: có 5 trạng thái đơn, chỉ có 6 Category, cột City/State Mỹ bị ghép ngẫu nhiên với cả 5 quốc gia nên phải phân tích theo `Country`, và toàn bộ 10 biểu đồ của nhóm đều tuân thủ 5 hướng dẫn thiết kế Chương 2 với bảng màu **Start-with-gray**."*
- **Slide 5 — Câu 2 (~45s)**: *"Ở **Câu 2**, để tránh sai lệch từ biểu đồ 2 trục Y (dual-axis), nhóm tách **Doanh thu** và **Số đơn theo tháng** thành 2 biểu đồ đường xếp dọc cùng trục thời gian, kèm cột gốc 0 theo năm ở bên phải. Kết quả cho thấy quy mô rất ổn định suốt 5 năm: khoảng **\$18,2M–\$18,5M/năm** và **~20.000 đơn/năm**, đỉnh tháng ở **2024-05 (\$1,64M)** và đáy ở **2020-02 (\$1,34M)**. Đáng chú ý, **tháng 2 năm nào cũng tạo đáy** (vùng xám) — nguyên nhân là tháng 2 chỉ có 28–29 ngày trong khi dữ liệu tổng hợp sinh đều theo ngày. Do đó, đánh giá hiệu suất tháng nên dùng doanh thu bình quân/ngày. Tiếp theo xin mời TV3 đào sâu vào Câu 3 và Câu 4."*

### [03:00 – 04:45] TV3 — Slide 6 ⭐ (Trọng tâm 1/4) & Slide 7 (Câu 4)
- **Slide 6 — Câu 3 ⭐ (~1 phút 05s)**: *"Đến với **điểm nhấn trọng tâm đầu tiên — Câu 3 về cơ cấu trạng thái đơn**. Thay vì lặp lại 5 con số của Câu 1 bằng biểu đồ tròn, nhóm vẽ **cột chồng 100% theo từng năm** kết hợp **cột ngang xếp hạng** theo thang nhận thức Cleveland–McGill. Hình bên trái cho thấy một thực tế đáng lo ngại: tỉ lệ `Delivered` giữ quanh 74,6%, còn tổng `Hủy + Trả` đi ngang quanh **6,1% suốt 5 năm liền** ($p = 0,58$). Nói cách khác, khoản thất thoát **\$5,63 triệu** là **rò rỉ mang tính hệ thống chưa hề được khắc phục**. Đặc biệt nhìn sang biểu đồ phải: đơn `Cancelled` có giá trị trung bình cao nhất toàn sàn — **\$942/đơn** so với \$916 của đơn giao thành công. Vì vậy, chỉ cần siết khâu xác nhận cho các đơn hàng giá trị lớn (> \$900) sẽ giảm ngay thiệt hại đáng kể."*
- **Slide 7 — Câu 4 (~40s)**: *"Sang **Câu 4 — Doanh thu theo nhóm sản phẩm**, vì tệp thật chỉ có **6 Category** nên nhóm vẽ đầy đủ cả 6 nhóm ở bên trái và bổ sung **Top 10 sản phẩm** ở bên phải. Nhóm `Electronics` dẫn đầu với **\$15,58M (17,0%)**, nhưng cả 6 nhóm phân bố rất đều (chênh đỉnh–đáy chỉ 2,8%). Bên phải, `Memory Card 128GB` dẫn đầu sản phẩm (\$1,94M). Nhóm tô đỏ sản phẩm **`Dress Shirt`** vì nó đứng Top 6 doanh thu (\$1,90M) nhưng lát nữa ở Câu 9 các bạn sẽ thấy đây cũng là **Top 3 sản phẩm bị trả hàng nhiều nhất**! Mời TV4 tiếp tục với góc nhìn địa lý và vận chuyển."*

### [04:45 – 06:15] TV4 — Slide 8 (Câu 5) & Slide 10 (Câu 7)
- **Slide 8 — Câu 5 (~40s)**: *"Khác hẳn sự đồng đều của nhóm hàng, ở **Câu 5 — Doanh thu theo quốc gia**, thị trường phân hóa cực kỳ mạnh: **Hoa Kỳ chiếm tới 70,0% doanh thu (\$64,31M)** — gấp **2,34 lần** 4 nước còn lại cộng lại, theo sau là **Ấn Độ (15,1% · \$13,88M)**. Dot plot bên phải chỉ ra giá trị đơn trung bình (AOV) cả 5 nước gần như y hệt nhau quanh \$915–\$922, chứng tỏ chênh lệch hoàn toàn do quy mô số đơn. Vì thế, mọi giải pháp tối ưu vận hành cần ưu tiên triển khai trước tại Mỹ và Ấn Độ."*
- **Slide 10 — Câu 7 (~50s)**: *"Ở **Câu 7 — Chi phí vận chuyển**, Boxplot bên trái cho thấy biểu phí ở 5 nước gần như đồng nhất quanh **\$7,33–\$7,46/đơn** (ANOVA $p = 0,57$). Ở phía trên bên phải, vì có tới 100.000 điểm dễ gây đen đặc nếu vẽ scatter thường, nhóm dùng **biểu đồ mật độ Hexbin** kèm đường hồi quy: hệ số tương quan $r = 0,039$ cho thấy phí vận chuyển hầu như không phụ thuộc giá trị đơn. Điều này dẫn tới phát hiện kinh doanh quan trọng ở biểu đồ góc dưới phải: **đơn hàng nhỏ dưới \$250 phải chịu phí ship tới 6,86% giá trị đơn** — cao gấp **18 lần** đơn trên \$1.500 (0,38%). Do đó, chính sách miễn phí vận chuyển theo ngưỡng \$250 sẽ kích thích gộp đơn rất hiệu quả. Xin mời TV5 vào 2 câu trọng tâm tiếp theo về Hủy và Trả hàng."*

### [06:15 – 08:15] TV5 — Slide 9 ⭐ (Trọng tâm 2/4) & Slide 11 ⭐ (Trọng tâm 3/4)
- **Slide 9 — Câu 6 ⭐ (~1 phút)**: *"Để tìm đúng thuốc chữa cho khoản thất thoát \$5,63M, ở **Câu 6** nhóm **tách riêng tỉ lệ Hủy (xảy ra trước giao) và tỉ lệ Trả (xảy ra sau giao)** cho từng nhóm hàng. Trên biểu đồ cột nhóm ngang, **`Home & Kitchen`** có tổng tỉ lệ Hủy+Trả cao nhất (**6,27%**) và tỉ lệ Trả hàng cao nhất (**3,21%**), gây thất thoát lớn nhất là **\$984 nghìn**. Trong khi đó, **`Electronics`** lại dẫn đầu riêng về tỉ lệ **Hủy đơn (3,23% — 544 đơn)** nhưng có tỉ lệ Trả thấp nhất (2,82%). Tuy kiểm định Chi-bình phương ($p = 0,84$) cho thấy chênh lệch tỉ lệ giữa các nhóm là hẹp — tức vấn đề trải đều toàn sàn — nhưng tách rõ hai chỉ số giúp ta biết cần tập trung chống *trả hàng* cho `Home & Kitchen` và chống *hủy trước giao* cho `Electronics`."*
- **Slide 11 — Câu 8 ⭐ (~1 phút)**: *"Tương tự ở **Câu 8 — Hình thức thanh toán**, nhóm đặt hai biểu đồ cạnh nhau để thấy một góc nhìn quản trị rất thú vị. Nếu chỉ nhìn **tỉ lệ phần trăm** bên trái, **`Cash on Delivery (COD)`** có tỉ lệ hủy cao nhất (**3,17%**), còn `Net Banking` và `Amazon Pay` trả hàng cao nhất (~3,15%), trong khi **`UPI`** an toàn nhất (tổng chỉ 5,85%). Nhưng khi nhìn sang **thiệt hại tiền mặt thực tế** bên phải: vì **`Credit Card`** chiếm 35% tổng số đơn nên gây thất thoát lớn nhất — tới **\$1,99 triệu**; cộng thêm **`Debit Card`** (\$1,12M) thì riêng 2 phương thức thẻ chiếm **55,1% tổng tiền mất (\$3,10M)**, gấp hơn 11 lần COD (\$279K)! Vì vậy, ngoài xác thực OTP cho COD, doanh nghiệp bắt buộc phải tối ưu quy trình xác nhận và đổi trả trên luồng thẻ. Xin mời TV6 chốt lại điểm nóng sản phẩm ở Câu 9 và demo Dashboard."*

### [08:15 – 10:15] TV6 — Slide 12 ⭐ (Trọng tâm 4/4) & Slide 13 (Demo Dashboard)
- **Slide 12 — Câu 9 ⭐ (~1 phút)**: *"Đi sâu xuống cấp độ từng sản phẩm ở **Câu 9**, để tránh nhiễu từ các mã hàng bán quá ít, nhóm đặt ngưỡng tối thiểu **1.000 đơn/sản phẩm** (kiểm tra thực tế cả 50 sản phẩm đều đạt từ 1.910–2.098 đơn). Nhóm chọn **Dot plot (Lollipop)** thay cho biểu đồ cột vì các tỉ lệ trả nằm sát nhau từ 3,5% đến 4,0% — khoảng cách từ đường trung bình toàn sàn **3,05%** hiện lên cực kỳ rõ. **Top 5 sản phẩm trả hàng cao nhất** gồm: đứng đầu là **`Yoga Mat` (3,97% · 81 đơn · \$72,7K)** — cao hơn gần 1,8 lần sản phẩm thấp nhất (`Bluetooth Speaker` 2,20%); tiếp theo là **`Noise Cancelling Headphones` (3,79%)**, **`Dress Shirt` (3,59% · \$76,6K)**, **`Cookware Set` (3,55%)** và **`Webcam Full HD` (3,53%)**. Tổng 5 SKU này gây **\$334 nghìn** hoàn trả, đặc biệt **`Dress Shirt`** còn có tỉ lệ hủy 3,74% (tổng hủy+trả lên tới 7,33%)."*
- **Slide 13 — Demo Dashboard HTML (~1 phút)**: *(Chuyển cửa sổ trình duyệt sang `outputs/dashboard/q10_dashboard.html`)* *"Toàn bộ 9 phân tích trên được nhóm tích hợp thành một **Dashboard tương tác bằng Plotly HTML** thiết kế theo nguyên tắc Shneiderman: hàng trên cùng góc trái là 4 thẻ KPI tổng quan; ở giữa là biểu đồ xu hướng có **dropdown chọn từng năm** và **thanh trượt range slider** *(thao tác bấm chọn năm 2024 rồi quay lại Tất cả)* cùng **bản đồ Choropleth 5 quốc gia** *(di chuột vào Mỹ & Ấn Độ cho thấy tooltip)*; phía dưới là các biểu đồ chẩn đoán Hủy/Trả, Top 10 SKU và khung 3 đề xuất hành động. Xin mời TV7 tổng kết 3 đề xuất và hạn chế của bài."*

### [10:15 – 11:30] TV7 — Slide 14 & 15 (3 Đề xuất + Kết luận & Hạn chế)
- **Slide 14 (~45s)**: *"Từ toàn bộ bằng chứng dữ liệu, nhóm đề xuất **3 giải pháp trọng tâm có thể triển khai ngay**:*
  1. *Thứ nhất, **siết QC đóng gói và chuẩn hóa mô tả/bảng size cho Top 5 SKU trả cao** (`Yoga Mat`, `Dress Shirt`...) và nhóm `Home & Kitchen` (\$984K) — chỉ cần giảm 20% hoàn trả ở Top 5 đã cứu trực tiếp ~\$67K.*
  2. *Thứ hai, **phân luồng thanh toán & xác thực đơn rủi ro**: áp dụng OTP cho `COD` (hủy 3,17%) và đơn giá trị lớn >\$900 (AOV đơn hủy cao nhất \$942), đồng thời tối ưu cơ chế đổi nhanh thay hoàn tiền trên `Credit/Debit Card` (\$3,10M thất thoát) — giảm 0,5 điểm % tỉ lệ hủy toàn sàn sẽ thu hồi ~\$460K.*
  3. *Thứ ba, **triển khai chính sách gộp đơn Free-ship ngưỡng \$250** để gỡ gánh nặng phí vận chuyển 6,86% ở đơn nhỏ và đẩy nhanh xác nhận kho cho nhóm `Electronics` (hủy 3,23%)."*
- **Slide 15 (~30s)**: *"Cuối cùng, nhóm minh bạch 3 hạn chế của tập dữ liệu tổng hợp: không có tính mùa vụ thật, có nhiễu ghép `City/State` với `Country` và `ProductName` với `Category`, đồng thời thiếu cột lý do trả hàng thực tế — đây là các biến cần bổ sung nếu triển khai trong doanh nghiệp thật. Toàn bộ mã Python, dữ liệu sạch và Dashboard HTML đã sẵn sàng kiểm chứng. Nhóm xin cảm ơn Thầy/Cô và các bạn đã lắng nghe, rất mong nhận được câu hỏi phản biện ạ!"*

---

## 3. Bộ 12 Câu hỏi Phản biện Q&A "Tủ" (Chuẩn bị theo Slide 4 & 29)

### Nhóm A — Về số liệu & làm sạch (30% điểm)
1. **Hỏi: Đề bài chỉ nhắc 4 trạng thái (`Delivered, Cancelled, Shipped, Returned`), sao nhóm lại có thêm `Pending`?**
   - *Đáp*: Slide 24 đề bài dặn rõ *"hãy mở dữ liệu để đối chiếu"*. Khi kiểm tra tệp thật `Amazon.csv`, cột `OrderStatus` có đúng 5 giá trị, trong đó `Pending` có **4.103 đơn (4,10%, \$3,74M)**. Nếu bỏ qua hoặc tự ý xóa sẽ làm sai tổng 100.000 đơn và sai tỉ trọng 100%.
2. **Hỏi: Công thức doanh thu nhóm dùng là gì? Tại sao tính tổng doanh thu có cả đơn `Cancelled` và `Returned`?**
   - *Đáp*: Nhóm kiểm chứng `TotalAmount = Quantity × UnitPrice × (1 - Discount) + Tax + ShippingCost` khớp 100%. Để tránh hiểu nhầm, nhóm luôn nêu song song **2 con số**: Doanh thu gộp (Gross = **\$91,83M** trên 100.000 đơn) và Doanh thu thực giao (`Delivered` = **\$68,37M**, 74,46%), tách riêng phần thất thoát Hủy+Trả (**\$5,63M**).
3. **Hỏi: Có 1.360 ngoại lệ `TotalAmount` theo quy tắc IQR (1,36%), sao nhóm không xóa đi cho "sạch"?**
   - *Đáp*: Theo **Chương 2 Slide 20**, ngoại lệ chỉ xóa/sửa nếu là *lỗi nhập liệu*; nếu là *giá trị thật nhưng hiếm* thì **phải giữ và giải thích**. Nhóm đã kiểm tra 1.360 đơn này đều có `Quantity = 4–5` và `UnitPrice = $500–$600` hoàn toàn hợp lý, xóa đi sẽ làm hụt mất doanh thu thật của các đơn hàng lớn.
4. **Hỏi: Tại sao tháng 2 năm nào cũng tụt sâu trong Câu 2? Có phải khách hàng ít mua sau Tết không?**
   - *Đáp*: Không phải yếu tố hành vi tiêu dùng. Do dữ liệu tổng hợp sinh giao dịch đều theo từng ngày trong năm (~54,8 đơn/ngày), nên tháng 2 chỉ có **28–29 ngày** (ít hơn 2–3 ngày tức ~9–10% so với tháng 31 ngày), dẫn tới tổng doanh thu tháng 2 luôn giảm tương ứng ~10%.
5. **Hỏi: Tại sao Câu 5 nhóm dùng `Country` mà không phân tích xuống `City` hay `State` cho chi tiết?**
   - *Đáp*: Khi kiểm tra chất lượng dữ liệu, nhóm phát hiện cả 5 quốc gia (kể cả Ấn Độ, Úc, Anh) đều ghép với đúng 13 mã bang Mỹ như `TX, CA, DC` (ví dụ dòng đầu tiên: `Washington, DC, India`). Vì cột `City/State` bị lỗi logic của dữ liệu tổng hợp, chỉ dùng `Country` mới đảm bảo tính trung thực.
6. **Hỏi: Kiểm định Chi-bình phương ở Câu 6 ($p=0,84$) và Câu 8 ($p=0,78$) cho thấy không có khác biệt có ý nghĩa thống kê, vậy tại sao nhóm vẫn đưa ra đề xuất?**
   - *Đáp*: Chính kết quả $p > 0,05$ mang lại một **insight quản trị trung thực**: tỉ lệ hủy/trả (~6,08%) không chỉ tập trung cục bộ ở 1 nhóm duy nhất mà là **vấn đề hệ thống trên toàn sàn**. Vì thế, thay vì chỉ xử lý 1 nhóm nhỏ như COD (chỉ 4,9% đơn), nhóm ưu tiên đề xuất theo **tác động tiền mặt tuyệt đối** (`Credit + Debit Card` = \$3,10M, `Home & Kitchen` = \$984K) kết hợp xử lý các điểm nóng SKU cụ thể như `Yoga Mat` (3,97%) và `Dress Shirt` (7,33% gộp).

### Nhóm B — Về chọn biểu đồ & thiết kế (45% điểm)
7. **Hỏi: Vì sao Câu 2 không vẽ chung Doanh thu và Số đơn lên 1 biểu đồ đường 2 trục Y cho gọn?**
   - *Đáp*: Theo **Chương 2 Slide 41**, biểu đồ 2 trục Y (dual-axis) dễ đánh lừa thị giác về độ dốc và mối quan hệ giữa hai đại lượng khác đơn vị. Việc tách thành 2 panel xếp dọc chung trục thời gian (small multiples) vừa giữ rõ xu hướng song hành, vừa tuyệt đối trung thực.
8. **Hỏi: Câu 3 đề gợi ý biểu đồ Donut/Cột chồng 100%, vì sao nhóm không dùng Donut?**
   - *Đáp*: Theo **thang nhận thức Cleveland–McGill (Chương 1 Slide 7)**, mắt người đọc *vị trí và độ dài* chính xác hơn *góc và diện tích*. Ở đây có 5 trạng thái với 2 lát nhỏ sát nhau (`Returned` 3,05% và `Cancelled` 3,03%) rất khó phân biệt trên Donut. Cột chồng 100% theo năm + cột ngang xếp hạng vừa dễ đọc hơn, vừa cho thấy thêm tính ổn định suốt 5 năm.
9. **Hỏi: Đề bài Câu 4 hỏi "10 nhóm sản phẩm lớn nhất", sao nhóm chỉ vẽ 6 nhóm?**
   - *Đáp*: Tệp thật `Amazon.csv` chỉ có đúng **6 `Category`**. Để vừa trung thực dữ liệu vừa đáp ứng trọn ý đề bài, nhóm vẽ đủ cả 6 Category ở panel trái và bổ sung **Top 10 `ProductName`** ở panel phải (đồng thời có số liệu 10 `Brand` trong `kpi_metrics.json`).
10. **Hỏi: Vì sao Câu 7 nhóm dùng Hexbin thay cho Scatter plot gợi ý trong đề?**
    - *Đáp*: Với **100.000 quan sát**, vẽ Scatter plot thông thường sẽ tạo thành một mảng đen đặc (overplotting), người xem không thấy vùng nào tập trung mật độ đơn hàng cao. **Hexbin** chia lưới mật độ vẫn giữ nguyên hai trục biến số x–y và đường hồi quy tuyến tính ($r = 0,039$), giúp thấy rõ mật độ đơn tập trung ở vùng `< \$1.500`.
11. **Hỏi: Vì sao Câu 9 chọn Dot plot (Lollipop) mà không dùng biểu đồ cột đứng?**
    - *Đáp*: Theo **Chương 2 Slide 29** (*Cột hay dot plot?*), khi các giá trị nằm rất gần nhau (3,53%–3,97%) và ta cần nhấn vào độ lệch so với mốc tham chiếu trung bình toàn sàn (3,05%), biểu đồ cột bắt buộc bắt đầu từ 0 sẽ khiến các cột trông gần bằng nhau. Dot plot không bắt buộc trục bắt đầu từ 0 nên phóng rõ thứ hạng và độ chênh lệch một cách trung thực.
12. **Hỏi: Nhóm áp dụng 5 hướng dẫn thiết kế Chương 2 cụ thể ở điểm nào, và tại sao kết hợp cả Matplotlib/Seaborn với Plotly?**
    - *Đáp*:
      - **5 hướng dẫn**: (1) Cho thấy dữ liệu (hiện đủ số liệu, giữ trục cột từ 0); (2) Giảm nhiễu (`sns.despine()`, không 3D, không nền gradient); (3) Gắn chữ với hình (100% tiêu đề chủ động nêu kết luận, nhãn số trực tiếp, chú thích đỉnh/đáy); (4) Tránh spaghetti (tách panel Câu 2); (5) **Bắt đầu từ màu xám** (nền xám `#94A3B8`, chỉ tô nhấn Teal `#0F766E` cho điểm chính và Đỏ `#DC2626` cho cảnh báo hủy/trả).
      - **Kết hợp thư viện** *(theo Case study Slide 14 bài giảng 5 thư viện Python)*: `Matplotlib`/`Seaborn` kiểm soát chi tiết từng pixel để xuất ảnh PNG 300 DPI chuẩn slide; còn `Plotly` mạnh về tương tác web (hover, dropdown, range slider, Choropleth) để xuất file HTML độc lập làm Dashboard demo trực tiếp.
