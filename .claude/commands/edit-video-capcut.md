---
description: Tự động đào đãi vàng từ video thô (>1 phút hoặc nhiều clip), cắt ghép, phối màu, đặt chữ sang trọng né vật thể, xử lý âm thanh ASMR/Kinetic SFX/Nhạc Beat và bơm thẳng vào CapCut Desktop (Node 1 -> Node 7).
---

Hãy kích hoạt ngay Skill `tiktok-auto-edit-master` (`.claude/skills/tiktok-auto-edit-master/SKILL.md`) với yêu cầu: `$ARGUMENTS`.

Thực thi đầy đủ chuỗi **7 Mắt Xích (`7-Node Model Chaining x 4-Step CoT`)**:
1. Kiểm toán tài nguyên trong `./raw_videos/` (`smart_raw_miner.py` & `pre_delivery_qa_auditor.py`). Nếu thiếu cảnh quan trọng, chủ động nhắn hỏi người dùng kèm phương án chữa cháy (`Fallback`).
2. Kiểm duyệt kịch bản CHR Việt Nam (`0–1.000 điểm`), cắt trên đà chuyển động, cân bằng sáng/màu, định tuyến âm thanh 3 tầng (`Native ASMR` vs `Kinetic/Foley SFX`), chọn chế độ Nhạc nền & Beat-Sync (`M1–M4`), hút màu chữ thực tế và đặt chữ né 100% sản phẩm (`capcut_master_injector.py`).
3. Tự chấm điểm QA trên thang 100 (`>= 95/100 điểm`), tự động `Auto-Heal` mọi lỗi, bơm bản nháp vào `/Users/huynguyen/Movies/CapCut/User Data/Projects/com.lveditor.draft/` và xuất Gói Đăng Bài TikTok Shop!
