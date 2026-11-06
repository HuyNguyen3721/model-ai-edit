---
name: tiktok-self-evolve-trainer
description: >-
  Use this skill when the user asks to train, upgrade, or evolve the AI video editor and shooting planner by learning from trending/viral TikTok review videos (clean-room mathematical & visual study without ripping copyrighted audio/video), synthesizing or harvesting copyright-safe sound effects into ./knowledge_vault/external_custom_sfx_registry.json, rescuing CapCut Desktop cache assets, learning from documents in ./knowledge_vault/05_documents_and_guides_inbox/, or reverse-engineering manual edits made by the user in CapCut Desktop with 4-Gate Anti-Degradation protection.
---

# TikTok Self-Evolving AI Trainer & Clean-Room Viral Learner (`/tu-nang-cap-ai`)

> **TÀI LIỆU THAM CHIẾU BẮT BUỘC:** Đọc [TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md](../../TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md). Khi quét kênh KOC hoặc xu hướng mới, **không chỉ nhìn vài video triệu view mà phải quét sâu toàn bộ danh mục kênh** (cả video triệu view, video tương tác/lưu cao lẫn video tầm trung có kỹ thuật dựng, bài test vật lý, font chữ hoặc âm thanh thông minh), trích xuất `Storyboard Grid 12 khung hình (4x3)` để đọc bằng Vision và tổng hợp thêm mọi SFX còn thiếu vào `./workspace/sfx_studio/` + `./knowledge_vault/external_custom_sfx_registry.json`.

Kích hoạt Skill này khi người dùng muốn **AI tự nâng cấp trí thông minh** (học hỏi từ video TikTok đang lên xu hướng/view đột biến, nạp âm thanh/hiệu ứng ngoài CapCut vào sổ đăng ký riêng, học thêm từ tài liệu mới, giải cứu kho CapCut Cache, hoặc học lỏm từ chính các thao tác chỉnh sửa của người dùng trên CapCut Desktop).

> **NGUYÊN TẮC BẢN QUYỀN & CHỐNG NGU ĐI (`100% CLEAN-ROOM & 4-GATE ANTI-DEGRADATION`):**
> 1. **Tuyệt đối KHÔNG cắt/lấy trực tiếp âm thanh hay hình ảnh từ video của người khác trên TikTok** để tránh vi phạm bản quyền (`Unoriginal Content / Copyright Strike`) và tránh dính giọng nói/nhạc nền rác của kênh khác.
> 2. Chỉ đọc video viral để học **Công thức Toán học & Bố cục Đạo diễn** (Nhịp cắt `Pacing Curve`, Góc quay `A1–A8`, Chuyển cảnh, Tỷ lệ cắt khớp Beat), lưu bản đồ phân cảnh vào `./knowledge_vault/04_viral_visual_and_effects_dna/` rồi **xóa ngay file video `.mp4` của bên thứ 3**.
> 3. Mọi âm thanh/hiệu ứng **KHÔNG CÓ sẵn trên CapCut** đều được tổng hợp mới `100%` bằng toán học DSP hoặc tải từ thư viện SFX rời hợp pháp, kiểm định qua **Cổng Độ Sạch Âm Học (`Crest Factor >= 5.0dB, <= 2.45s`)** và lưu vào file chứa riêng: **`./knowledge_vault/external_custom_sfx_registry.json`**.
> 4. Mọi nâng cấp não bộ đều đi qua **4 Cổng Chống Thoái Hóa (`4-Gate Anti-Degradation`)**: Lọc thẩm mỹ `>= 85/100 điểm`, Cập nhật kẹp biên `Clamped EMA 80/20`, và Tự động sao lưu phiên bản tại `./knowledge_vault/06_brain_version_snapshots/` (hỗ trợ `--rollback-brain`).

## Quy Trình 5 Bước Tự Nâng Cấp Toàn Diện

### Bước 1: Săn Lùng & Giải Phẫu Sạch 6 Lớp Video TikTok Đang Lên Xu Hướng (`Clean-Room Study`)
1. Chạy công cụ săn video đột biến (`Breakout Viral Index - BVI` dựa trên `Outlier Views/Followers >= 2.5x`, `Velocity >= 2.000 views/h`, và `Saves/Collects cao`):
   - **Nếu săn theo từ khóa/ngành hàng:**
     ```bash
     python3 ./tiktok_viral_scout_and_learner.py \
       --scout-keyword "<từ_khóa_review_ngành_hàng>" \
       --archetype <P1-P7> \
       --max-videos 3
     ```
   - **Nếu săn từ các kênh KOC mẫu (như `@meshinthuine`):**
     ```bash
     python3 ./tiktok_viral_scout_and_learner.py \
       --scout-koc-channels "meshinthuine" \
       --archetype <P1-P7> \
       --max-videos 3
     ```
   - **Nếu người dùng đưa link TikTok cụ thể để học công thức:**
     ```bash
     python3 ./tiktok_viral_scout_and_learner.py \
       --learn-url "<url_tiktok>" \
       --archetype <P1-P7>
     ```
2. **Đọc Bản Đồ Phân Cảnh Bằng Thị Giác Đa Phương Thức (`Vision Storyboard Inspection`):**
   - Dùng công cụ `read_file` mở tấm ảnh `./knowledge_vault/04_viral_visual_and_effects_dna/viral_<id>_storyboard_grid.jpg` để quan sát chuỗi góc quay (`A1–A8`), bố cục chủ thể và vị trí đặt chữ.

### Bước 2: Đồng Bộ Kho Âm Thanh Ngoài CapCut (`external_custom_sfx_registry.json`) & Giải Cứu CapCut Cache
Chạy lệnh tổng hợp bộ SFX nguyên bản 100% không bản quyền (`Clean-Room DSP Synthesis`), giải cứu kho `CapCut Cache` vào `./knowledge_vault/01_capcut_rescued_assets/`, và cập nhật 2 sổ đăng ký riêng (`external_custom_sfx_registry.json` & `learned_effects_and_transitions_registry.json`):
```bash
python3 ./viral_sfx_harvester.py --sync-live-trends
```
Nếu cần tìm thêm một hiệu ứng âm thanh rời hợp pháp theo từ khóa và nạp vào ngăn riêng `02_external_sfx_not_in_capcut`:
```bash
python3 ./viral_sfx_harvester.py \
  --search-trend "<ten_sfx_ngan>" \
  --category "custom_sfx" \
  --subfolder "<hook_attention|kinetic_motion|asmr_foley|pivot_khen_che|transition_hit|cta_cart_chime>"
```

### Bước 3: Tự Động Đọc & Học Từ Các Tài Liệu Mới Trong `./knowledge_vault/05_documents_and_guides_inbox/`
Quét mọi tài liệu `.md`, `.txt`, `.docx` mới được người dùng thêm vào và lưu quy tắc vào `./knowledge_vault/learned_document_rules_registry.json`:
```bash
python3 ./self_evolving_trainer.py --learn-from-docs
```

### Bước 4: Học Ngược Từ Các Chỉnh Sửa Tay Của Người Dùng Trên CapCut & Dự Án Nổ Đơn (Kẹp Biên 80/20)
1. **Nếu người dùng vừa tự tay tinh chỉnh lại một dự án trên CapCut Desktop:**
   ```bash
   python3 ./self_evolving_trainer.py --learn-from-capcut "<Tên_Project_CapCut>"
   ```
2. **Nếu người dùng báo một dự án đạt nhiều view hoặc nổ đơn lớn (`GPM Winner`):**
   ```bash
   python3 ./self_evolving_trainer.py \
     --reward-winner "<Tên_Project_CapCut>" \
     --archetype <P1-P7> \
     --views <số_view> \
     --orders <số_đơn>
   ```
3. *(Nếu phát hiện thông số sau khi học bị lệch ý muốn, khôi phục tức thì về bản thông minh nhất trước đó bằng lệnh: `python3 ./self_evolving_trainer.py --rollback-brain`)*

### Bước 5: Auto-Update Trực Tiếp Vào Bộ Đề Xuất Quay (`Node 0`) & Bộ Edit (`Node 1–7`)
```bash
python3 ./pre_production_shooting_planner.py \
  --description "Đồng bộ hóa não bộ tự học" \
  --archetype <P1-P7> \
  --ask-questions > /dev/null && \
python3 ./self_evolving_trainer.py --show-brain
```
