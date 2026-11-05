---
name: tiktok-auto-edit-master
description: >-
  Use this skill when the user has filmed raw video clips (in ./raw_videos/ or a specified folder) and wants to automatically edit, cut, color-correct, add dynamic obstacle-free luxury typography, route 3-tier Native ASMR vs. Foley/Kinetic SFX, sync music beats, inject the draft directly into CapCut Desktop, run the 100-point QA & CHR Vietnam compliance audit, or request missing resources from the user.
---

# TikTok Auto-Edit Master (`Node 1 -> Node 7` — `/edit-video-capcut`)

Kích hoạt Skill này khi người dùng đã có video thô (1 video dài `>1 phút` hoặc nhiều clip ngắn trong `./raw_videos/`) và yêu cầu dựng thành dự án hoàn chỉnh trên **CapCut Desktop**.

## Quy Trình Chuỗi 7 Mắt Xích (`7-Node Model Chaining x 4-Step CoT`)

Tại mỗi mắt xích, AI bắt buộc suy luận theo 4 bước (`Quan sát định lượng` $\rightarrow$ `Truy xuất ký ức brain_memory & blueprint` $\rightarrow$ `Đối đầu giả thuyết` $\rightarrow$ `Khóa thông số JSON`) và lưu checkpoint qua `self_evolving_trainer.py`.

### Mắt Xích 1 (`Node 1`): Tự Động Gom File Về Thư Mục Dự Án Riêng, Kiểm Toán Tài Nguyên & Chủ Động Hỏi Ý Kiến Người Dùng
1. **Tự động chuyển ảnh/video từ Hộp thư chung (`./raw_photos/`, `./raw_videos/`) sang Thư mục riêng của Dự án (`./projects/<slug>/videos/`):**
   - Trước khi phân tích hay bơm đường dẫn vào CapCut Desktop, **BẮT BUỘC** chạy lệnh gom file tự động để người dùng **không bao giờ phải tự tay xóa file cũ** trong `./raw_videos/` và dự án trên CapCut Desktop **vĩnh viễn không bị lỗi `Media Lost`**:
     ```bash
     python3 /Users/huynguyen/Desktop/tiktok/self_evolving_trainer.py --ingest-project "<ten_du_an_slug>"
     ```
   - Kiểm tra xem dự án có sẵn file `./projects/<slug>/blueprint/<slug>_shooting_plan.json` (hoặc trong `./workspace/shooting_blueprints/`) từ `Node 0` không và nạp bộ nhớ tự học:
     ```bash
     python3 /Users/huynguyen/Desktop/tiktok/self_evolving_trainer.py --show-brain
     ```
2. Dùng `smart_raw_miner.py` và hàm `audit_raw_resources_and_generate_user_requests()` trong `pre_delivery_qa_auditor.py` để quét toàn bộ video trong `./projects/<slug>/videos/`:
   - Nếu phát hiện **thiếu cảnh cốt lõi** (ví dụ: không có cảnh chứng minh công dụng `One-Take`, clip dài `>3.2s` mà không có cảnh cận `Macro` cắt ngang, hoặc thiếu sáng nặng `YAVG < 85`), **hãy chủ động nhắn hỏi người dùng xem họ có muốn cung cấp thêm clip/ghi âm bổ sung không**, đồng thời đưa sẵn **Phương án chữa cháy (`AI Fallback Plan`)** nếu người dùng chọn dựng luôn!
   - Gọi hàm `learn_from_completed_shoot_and_edit()` trong `pre_production_shooting_planner.py` để cập nhật thói quen ánh sáng/âm thanh phòng quay của người dùng vào bộ nhớ.

### Mắt Xích 2 (`Node 2`): Kịch Bản, Phễu Chuyển Đổi GPM & Kiểm Duyệt Luật CHR Việt Nam
1. Trích xuất lời thoại kèm timestamp từng từ (`extract_word_timestamps_whisper` trong `smart_raw_miner.py`).
2. Kiểm tra nghiêm ngặt theo [Cẩm nang Toàn diện TikTok Affiliate (Việt Nam).md](../../Cẩm%20nang%20Toàn%20diện%20TikTok%20Affiliate%20(Việt%20Nam).md):
   - Loại bỏ/thay thế mọi từ khóa vi phạm y tế, cam kết tuyệt đối (`100%`, `trị dứt điểm`, `thần dược`), hoặc điều hướng ngoài nền tảng.
   - Đảm bảo cấu trúc 28s có đủ: **Hook (`0–3s`)** $\rightarrow$ **Demo thật (`3–18s`)** $\rightarrow$ **Điểm chuyển `Khen 8 - Chê 2` (`18–23s`)** $\rightarrow$ **Chỉ giỏ hàng vòng lặp `Seamless Loop CTA` (`23–28s`)**.

### Mắt Xích 3 (`Node 3`): Cắt Cảnh Trên Đà Chuyển Động & Đồng Bộ Ánh Sáng/Màu Sắc
1. Dùng `mine_golden_segments_from_long_raw_videos()` trong `smart_raw_miner.py` để:
   - Khử toàn bộ các đúp quay hỏng/lặp lời (`deduplicate_retake_clusters`).
   - Cắt cảnh đúng trên đà chuyển động tay (`trim_clip_on_action_and_motion`), tạo `J-Cut` âm thanh đi trước hình `0.15s` và `Micro Slow-Mo 0.88x` cho cảnh Reveal kết quả.
   - Chuẩn hóa độ sáng (`YAVG -> 135`) và nhiệt độ màu đồng nhất giữa mọi clip (`compute_clip_exposure_and_wb_adjustments`).

### Mắt Xích 4 (`Node 4`): Đạo Diễn Âm Thanh 4 Tầng (ASMR Thật + Kinetic SFX + Nhạc Beat Thông Minh)
1. **Định tuyến âm thanh gốc 3 tầng (`evaluate_and_route_clip_audio` trong `capcut_master_injector.py`):**
   - Nếu tiếng thật từ sản phẩm đắt giá (`Crest Factor >= 11dB`, không bị giọng nói đè): Kích hoạt **`CHẾ ĐỘ 1: GIỮ 100% NATIVE ASMR (+3.5dB)`**.
   - Nếu vừa nói vừa thao tác: Kích hoạt **`CHẾ ĐỘ 2: HYBRID VOICE + SUBTLE SFX`**.
   - Nếu tiếng gốc ồn/phô (`Noise Floor > -35dB`): Kích hoạt **`CHẾ ĐỘ 3: MUTE 100% & THAY BẰNG FOLEY SFX`**.
2. **Bắt 6 cử chỉ chuyển động (`detect_kinetic_movement_sfx_triggers` trong `smart_raw_miner.py`):** Tự động gắn SFX (`Whoosh / Pop / Boing / Ding / Click`) nổ sớm `-0.04s` (`40ms`) trước đỉnh chuyển động.
3. **Chọn chiến lược Nhạc nền & Cắt theo Beat (`select_smart_bgm_and_beat_editing_strategy`):** Chọn đúng 1 trong 4 chế độ (`M1 Full Beat-Sync` / `M2 Selective Hook & CTA Sync` / `M3 Aesthetic Chill` / `M4 Pure ASMR`) và tạo đường cong `Dynamic Ducking Keyframes` (`18%` khi nghỉ thoại $\rightarrow$ `5%` khi có giọng đọc).

### Mắt Xích 5 (`Node 5`): Thẩm Mỹ Chữ Sang Trọng, Đồng Bộ Màu Video & Né Vật Thể 100%
1. Dùng `compute_dynamic_video_matched_text_style()` và `find_obstacle_free_text_coordinates()` trong `capcut_master_injector.py`:
   - Hút mã màu Hex thực tế từ từng cảnh video (`HSV Harmonies`), kiểm tra độ tương phản `WCAG >= 4.5:1`.
   - Tự động tính `font_size` theo mật độ ký tự (`<= 28 ký tự/dòng`) và đặt tọa độ `(x, y)` vào khoảng trống an toàn — **tuyệt đối không đè lên sản phẩm/khuôn mặt và không chạm vùng cấm UI TikTok (`y < -0.58`)**.

### Mắt Xích 6 & 7 (`Node 6 & 7`): Bơm CapCut Draft, Tự Kiểm Duyệt 100 Điểm & Bàn Giao
1. Chạy `audit_and_auto_heal_edit_plan_before_delivery()` trong `pre_delivery_qa_auditor.py` để tự chấm điểm trên thang 100 và tự sửa lỗi (`Auto-Heal`) cho đến khi đạt **`>= 95/100 điểm`**.
2. Gọi `inject_master_draft()` và `verify_and_auto_heal_draft()` trong `capcut_master_injector.py` để bơm dự án vào `/Users/huynguyen/Movies/CapCut/User Data/Projects/com.lveditor.draft/<Project_Name>/` và lưu bản chụp `save_initial_ai_draft_snapshot()` phục vụ việc học ngược sau này.
3. Xuất **Bảng Điểm QA 100 Điểm** + **Gói Đăng Bài TikTok Shop (`generate_tiktok_shop_publish_package`: Tiêu đề Thẻ Giỏ Hàng `<= 30 ký tự`, Caption SEO, Hashtag, Miễn trừ TPCN nếu có)** cho người dùng!
