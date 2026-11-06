---
name: tiktok-qa-chr-auditor
description: >-
  Use this skill when the user wants to review, audit, or score a video edit plan, a CapCut Desktop draft, or a script against the 100-Point Professional Video QA Scorecard and the Vietnam TikTok Affiliate CHR Policy (0-1,000 points), auto-heal any defects, or generate an optimized TikTok Shop Product Anchor title and SEO caption.
---

# TikTok 100-Point QA & CHR Vietnam Compliance Auditor (`/kiem-duyet-video`)

> **TÀI LIỆU THAM CHIẾU BẮT BUỘC:** Đọc [TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md](../../TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md) và [Cẩm nang Toàn diện TikTok Affiliate (Việt Nam).md](../../Cẩm%20nang%20Toàn%20diện%20TikTok%20Affiliate%20(Việt%20Nam).md) để kiểm định đủ 6 trụ cột QA 100 điểm (bao gồm kiểm chứng Trí tuệ Ngữ cảnh Đa KOC `Pillar 4`, Lá chắn CHR biến động giá CTKM `@3thag8_`, nhãn độ tuổi Sữa trên 2 tuổi và 24 cụm từ tách dấu chấm/hai chấm OCR).

Kích hoạt Skill này khi người dùng muốn kiểm tra chất lượng một dự án video trước khi xuất bản, rà soát rủi ro vi phạm **Chính sách CHR TikTok Shop Việt Nam (`0–1.000 điểm`)**, hoặc tạo gói nội dung đăng bài chuẩn SEO.

## Quy Trình Kiểm Duyệt 3 Bước

### Bước 1: Chấm Điểm 7 Hạng Mục Chuyên Sâu (Thang 100 Điểm) & Tự Động Sửa Lỗi (`Auto-Heal`)
Sử dụng `pre_delivery_qa_auditor.py` và `capcut_master_injector.py` để kiểm tra:
1. **Nhịp độ & Giữ chân 3 giây đầu (`20đ`):** Clip mở đầu `<= 1.8s`, không có clip nào dài quá `2.8s` mà không đổi góc máy, không có khe hở đen (`0 micro-giây` gap) trên trục `V1`.
2. **Thẩm mỹ Chữ, Màu & Không đè sản phẩm (`15đ`):** Chữ có độ tương phản `WCAG >= 4.5:1`, tối đa `28 ký tự/dòng`, nằm trong vùng trống an toàn (`-0.58 <= y <= 0.72`), không đè lên sản phẩm hoặc khuôn mặt.
3. **Âm thanh 4 Tầng & Khớp Nhịp (`15đ`):** Giữ đúng `Native ASMR` ở các cảnh có `Crest Factor >= 11dB`, `Kinetic SFX` đặt sớm `-0.04s`, nhạc nền có `Dynamic Ducking` (`5%` khi có giọng nói).
4. **Cấu trúc Tâm lý & Chuyển đổi GPM (`15đ`):** Có điểm chuyển `Khen 8 - Chê 2` và hành động chỉ tay góc trái dưới kèm vòng lặp `Seamless Loop CTA`.
5. **Tuân thủ Tuyệt đối Chính sách CHR Việt Nam (`20đ`):**
   - Quét toàn bộ phụ đề, banner và lời thoại theo [Cẩm nang Toàn diện TikTok Affiliate (Việt Nam).md](../../Cẩm%20nang%20Toàn%20diện%20TikTok%20Affiliate%20(Việt%20Nam).md).
   - Tự động thay thế mọi từ khóa cấm y khoa/tuyệt đối (`100%`, `vĩnh viễn`, `trị dứt điểm`, `thần dược`) và từ khóa điều hướng ngoài nền tảng (`Zalo`, `Shopee`, `Facebook`).
   - Nếu là ngành hàng **TPCN (`P7`)**, bắt buộc tự động chèn dòng miễn trừ trách nhiệm: *"Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh"*.
6. **Đồng bộ Ánh sáng, Màu sắc & Chuyển động (`10đ`):** Chênh lệch độ sáng giữa các cảnh `< 15 đơn vị YAVG`.
7. **Tính toàn vẹn kỹ thuật CapCut Draft (`5đ`):** Chạy `verify_and_auto_heal_draft(draft_path)` để đảm bảo mọi đường dẫn media tồn tại 100% trên ổ cứng.

### Bước 2: Chủ Động Đề Xuất Bổ Sung Tài Nguyên (Nếu Cần Thiết)
Nếu phát hiện video có thể đạt hiệu quả chuyển đổi (`GPM`) cao hơn nhiều khi có thêm 1 clip cận cảnh hoặc 1 câu thoại đính chính, hãy xuất bảng **`[ĐỀ XUẤT BỔ SUNG TÀI NGUYÊN TỪ ĐẠO DIỄN AI]`** để hỏi ý kiến người dùng.

### Bước 3: Xuất Bảng Điểm QA & Gói Đăng Bài TikTok Shop
Gọi `generate_tiktok_shop_publish_package()` trong `pre_delivery_qa_auditor.py` và trình bày cho người dùng:
- **Điểm số QA cuối cùng (`>= 95/100`)** và danh sách các mục đã tự động sửa lỗi (`Auto-Healed Logs`).
- **Tiêu đề Thẻ Neo Giỏ Hàng Vàng (`Product Anchor Title <= 30 ký tự`)**.
- **Caption chuẩn SEO TikTok + Bộ 5 Hashtag mục tiêu**.
- **Khuyến nghị Chọn Ảnh Bìa (`Cover Thumbnail Frame`)** ở giây có độ nét và bố cục chữ đẹp nhất.
