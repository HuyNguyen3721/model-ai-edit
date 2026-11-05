---
description: Kiểm duyệt độc lập dự án CapCut hoặc kịch bản theo Bảng Điểm 100 Chuyên Sâu & Luật CHR TikTok Affiliate Việt Nam (0-1.000 điểm), tự động sửa lỗi và xuất Gói Đăng Bài TikTok Shop.
---

Hãy kích hoạt ngay Skill `tiktok-qa-chr-auditor` (`.claude/skills/tiktok-qa-chr-auditor/SKILL.md`) với đối tượng kiểm tra: `$ARGUMENTS`.

1. Chạy `pre_delivery_qa_auditor.py` và `verify_and_auto_heal_draft()` trong `capcut_master_injector.py` để chấm điểm 7 hạng mục (Thang 100 điểm).
2. Quét sạch mọi từ khóa vi phạm và rủi ro trừ điểm CHR Việt Nam (`-10/-20/-40đ`), tự động thêm dòng miễn trừ trách nhiệm nếu là TPCN (`P7`).
3. Xuất Bảng Điểm QA chi tiết, danh sách các mục đã tự động sửa lỗi (`Auto-Healed`), đề xuất bổ sung tài nguyên (nếu có), và Gói Đăng Bài TikTok Shop (`Tiêu đề Thẻ Giỏ Hàng <= 30 ký tự` + `Caption SEO`).
