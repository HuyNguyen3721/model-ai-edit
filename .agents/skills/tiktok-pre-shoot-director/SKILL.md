---
name: tiktok-pre-shoot-director
description: >-
  Use this skill when the user provides product photos, product descriptions, or asks for filming ideas, camera angles, script suggestions, or what video resources to shoot before filming a TikTok Affiliate review video. It activates Node 0 (Pre-Production AI Creative Director), auto-updates from learned viral patterns, asks 3 style confirmation questions, and generates a 6-shot Edit-Ready Shooting Blueprint.
---

# TikTok Pre-Shoot Creative Director (`Node 0` — `/len-kich-ban-quay`)

Kích hoạt Skill này ngay khi người dùng gửi **ảnh chụp sản phẩm** và/hoặc **mô tả sản phẩm** dự định quay video review TikTok Affiliate.

## Quy Trình Thực Thi Bắt Buộc (4 Bước)

### Bước 1: Đọc Ảnh Sản Phẩm Bằng Thị Giác Đa Phương Thức & Auto-Update Não Bộ
1. Nếu người dùng gửi kèm file ảnh (trong `./raw_photos/` hoặc đính kèm trực tiếp), hãy dùng công cụ `read_file` để quan sát trực tiếp bức ảnh:
   - Xác định chất liệu vỏ/bề mặt (bóng kính dễ lóa đèn hay nhám lì), màu sắc chủ đạo (`Hex Palette`), hình dáng và kích thước khi cầm trên tay.
   - Đọc chữ trên bao bì để phát hiện sớm rủi ro **Chính sách CHR Việt Nam (`0–1.000 điểm`)** (ví dụ: TPCN `P7`, Sữa công thức dưới 24 tháng `P4`, Mỹ phẩm đặc trị `P1`, hoặc logo thương hiệu lớn `P3`).
2. Chạy lệnh phân tích quang học + tự động đồng bộ tri thức mới nhất từ não bộ (`auto_sync_and_evolve_shooting_brain`) và sinh bộ câu hỏi tương tác:
   ```bash
   python3 /Users/huynguyen/Desktop/tiktok/pre_production_shooting_planner.py \
     --images "<đường_dẫn_ảnh_cách_nhau_dấu_phẩy>" \
     --description "<mô_tả_sản_phẩm>" \
     --ask-questions
   ```

### Bước 2: Báo Cáo Nhanh Kết Quả Nhận Diện & Hỏi 3 Câu Chốt Phong Cách
Trình bày ngắn gọn cho người dùng:
- **Mã ngành hàng (`P1–P7`)**, **Khoảnh khắc Móc câu Thị giác (`Visual Aha! Hook`)**, **Tiếng động Thật đắt giá (`Native ASMR Trigger`)**, và **Cảnh báo đỏ CHR (những cảnh tuyệt đối không được bấm máy)**.
- Đặt **3 câu hỏi trắc nghiệm ngắn gọn** (ưu tiên dùng công cụ `ask_question` nếu có, hoặc trình bày rõ ràng kèm nhãn `(Khuyên dùng)`):
  1. **🎭 Câu 1 — Chọn Phong Cách Video (`Vibe`):** `V1 (KOC Đời thường Mẹ Shin Thúi Nè - Khen 8 Chê 2)` / `V2 (Sang trọng Aesthetic & Pure ASMR)` / `V3 (Test thực chiến One-Take)` / `V4 (Đập hộp nhịp nhanh Beat-Sync)`.
  2. **🗣️ Câu 2 — Chọn Hình Thức Lên Hình & Thu Âm (`Talent`):** `T1 (Lộ mặt nói + POV tay)` / `T2 (Chỉ quay 2 bàn tay POV + Thu ASMR thật, lồng tiếng sau)` / `T3 (Quay hình im lặng, lồng tiếng & SFX sau)`.
  3. **🏠 Câu 3 — Bối Cảnh & Đạo Cụ Có Sẵn (`Props`):** `B1 (Có mẫu cũ / vết bẩn thật để so sánh Trước-Sau)` / `B2 (Chỉ có sản phẩm mới trên bàn sạch)` / `B3 (Quay trực tiếp tại nơi sử dụng)`.
*(Lưu ý: Nếu người dùng nói "Tự quyết định cho tôi", hãy bỏ qua bước chờ trả lời và dùng ngay phương án `(Khuyên dùng)` đã được `Auto-Update` từ não bộ!)*

### Bước 3: Xuất Bản Thiết Kế 6 Cảnh Cần Quay Chuẩn Bộ Edit (`Edit-Ready Shooting Blueprint`)
Ngay khi người dùng chọn xong (hoặc yêu cầu tự chọn), chạy lệnh:
```bash
python3 /Users/huynguyen/Desktop/tiktok/pre_production_shooting_planner.py \
  --images "<đường_dẫn_ảnh>" \
  --description "<mô_tả_sản_phẩm>" \
  --vibe <V1|V2|V3|V4> \
  --talent <T1|T2|T3> \
  --props <B1|B2|B3> \
  --project-slug "<ten_du_an_khong_dau>"
```

### Bước 4: Trình Bày Bảng Hướng Dẫn Bấm Máy 6 Cảnh Cho Người Dùng
Hiển thị rõ ràng cho người dùng:
1. **Danh sách 6 Clip cần bấm máy (`RAW_01_HOOK` $\rightarrow$ `RAW_06_SEAMLESS_LOOP_CTA`)**: Chỉ rõ Góc quay (`A1–A8`), Thời lượng bấm máy (`4–15s`), Hành động tay đầu/cuối cảnh (để khớp thuật toán `Cutting on Action` và `Kinetic SFX`), Khoảng trống cần chừa trên khung hình (để đặt chữ không đè lên sản phẩm), và Chỉ dẫn giữ im lặng 2.5s ở Cảnh 3 để thu `100% Native ASMR`.
2. **Gợi ý Điểm Trừ Nhẹ Hợp Lý (`Khen 8 - Chê 2`)** và **Lời thoại mẫu 28 giây** có vòng lặp `Seamless Loop`.
3. Thông báo đã khóa bản thiết kế tại `./workspace/shooting_blueprints/<project_slug>_shooting_plan.json` để khi người dùng quay xong bỏ video vào `./raw_videos/`, Bộ Edit Tự Động sẽ lắp ráp khớp 100%!
