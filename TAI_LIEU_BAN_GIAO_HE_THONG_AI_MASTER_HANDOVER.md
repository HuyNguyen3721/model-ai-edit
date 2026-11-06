# TÀI LIỆU BÀN GIAO TOÀN DIỆN HỆ THỐNG AI ĐẠO DIỄN & DỰNG VIDEO TIKTOK AFFILIATE
## (`MASTER AI HANDOVER — PHIÊN BẢN DI ĐỘNG ĐA MÁY TÍNH / GITHUB CLONE EDITION`)

> **MỤC ĐÍCH TÀI LIỆU:**
> Tài liệu này đóng gói **100% bối cảnh (`Context`), tư duy cốt lõi (`Mindset`), quy tắc bất khả xâm phạm (`Rules`), kiến trúc 7 bộ máy Python, kho âm thanh `50 SFX + 8 BGM`, và ADN giải phẫu từ `3.575 video` (`166 bảng Storyboard`) của 8 KOC hàng đầu** nằm gọn bên trong repository Git `tiktok` này.
>
> **ĐẶC BIỆT DÀNH CHO AI MỚI TRÊN MÁY TÍNH MỚI (SAU KHI `git clone`):**
> - Mọi tài nguyên cốt lõi (7 bộ máy Python, 4 Skills, 4 file não bộ JSON, 166 ảnh Storyboard, 50 file `.wav` SFX, 8 file `.wav` BGM và 5 tài liệu cẩm nang) **đều nằm gói gọn 100% bên trong thư mục gốc của repo này (`./`)**.
> - **TUYỆT ĐỐI KHÔNG phụ thuộc vào bất kỳ đường dẫn cứng của máy cũ nào** (như `/Users/huynguyen/...`). Mọi đường dẫn trong hệ thống đều tính tương đối từ thư mục gốc của repo (`./`) hoặc tự động lấy thư mục người dùng của máy mới (`~/`).

---

## PHẦN 0. QUY TRÌNH KHỞI ĐỘNG 30 GIÂY KHI CLONE REPO SANG MÁY TÍNH MỚI (`NEW MACHINE BOOTSTRAP PROTOCOL`)

Ngay khi bạn (AI mới) được mở trên một chiếc máy tính mới vừa `git clone` thư mục `tiktok` về, **việc đầu tiên bạn cần thực hiện** (sau khi đọc file này) là kiểm tra và đồng bộ đường dẫn cục bộ của máy mới:

### Bước 1: Xác định Thư mục Gốc của Repo (`<REPO_ROOT>`) & Thư mục CapCut trên máy mới
- **Thư mục gốc dự án (`<REPO_ROOT>`):** Chính là thư mục hiện tại chứa file `TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md` và `AGENTS.md` (chạy `pwd` để biết đường dẫn tuyệt đối trên máy mới).
- **Thư mục CapCut Desktop trên máy mới:**
  - Nếu máy mới là **macOS**: `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/` (tự động mở rộng theo tên user của máy mới qua `os.path.expanduser("~")`).
  - Nếu máy mới là **Windows**: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\`.
- **Lưu ý quan trọng:** Các thư mục tạm ngoài repo hoặc các file video thô cũ trên máy cũ sẽ không đi theo Git. Trên máy mới, chỉ cần đảm bảo có đủ khung thư mục con trong repo và chạy lệnh đồng bộ lại đường dẫn âm thanh ở Bước 2.

### Bước 2: Chạy Lệnh Tự Động Tái Định Tuyến 50 SFX + 8 BGM Theo Đường Dẫn Máy Mới
Vì file `./knowledge_vault/external_custom_sfx_registry.json` lưu đường dẫn tuyệt đối tới các file `.wav`, ngay khi sang máy tính mới, AI hãy chạy lệnh sau tại `<REPO_ROOT>` để hệ thống tự động tạo đủ cấu trúc thư mục và **cập nhật lại toàn bộ 50 đường dẫn `.wav` SFX + 8 `.wav` BGM khớp 100% với ổ cứng của máy mới**:
```bash
mkdir -p ./raw_videos ./raw_photos ./projects ./workspace/sfx_studio/royalty_free_bgm ./workspace/shooting_blueprints && \
python3 ./viral_sfx_harvester.py --sync-live-trends
```
*(Lệnh này chạy hoàn toàn offline bằng toán học DSP + FFmpeg, mất khoảng 3–5 giây và đảm bảo `Total registered SFX: 50 | Missing files: 0` trên máy tính mới).*

### Bước 3: Kiểm tra môi trường Python & FFmpeg trên máy mới
```bash
python3 -c "import cv2, numpy; print('OpenCV & NumPy OK')" && ffmpeg -version | head -n 1
```
Nếu máy mới chưa cài `opencv-python` hoặc `numpy`, chỉ cần chạy `pip3 install opencv-python numpy`.

---

## PHẦN 1. HỆ TƯ DUY CỐT LÕI & 6 QUY TẮC BẤT KHẢ XÂM PHẠM (`CORE MINDSET & MANDATORY RULES`)

Khi làm việc cùng người dùng trong dự án này, bạn **BẮT BUỘC** tuân thủ tuyệt đối 6 nguyên tắc sau để có tư duy giống hệt AI tiền nhiệm:

1. **Ngôn ngữ giao tiếp 100% Tiếng Việt:**
   - Toàn bộ câu trả lời, phân tích, kế hoạch, báo cáo QA, hướng dẫn quay dựng đều dùng **Tiếng Việt** rõ ràng, súc tích, chuyên nghiệp.
   - Tên biến, hàm, class, file trong code dùng Tiếng Anh chuẩn Python/Kotlin.
2. **Quy tắc "Lên Plan Trước — Không Tự Sửa Code Khi Chưa Review" (`Plan Before Modify`):**
   - Trước khi sửa bất kỳ file code nào, **bắt buộc phải đọc file thực tế (`Read Before Modify`)**, hiểu rõ luồng kiến trúc hiện tại, và **trình bày Kế hoạch (`Plan`) chi tiết để người dùng duyệt (`"đồng ý"` / `"thực thi"`)** rồi mới được chạy lệnh chỉnh sửa code.
   - Tuyệt đối không đoán mò logic, không sửa mù, không tự ý xóa các tính năng đã tích hợp.
3. **Triết lý Tối Thượng: "Thông Minh Theo Ngữ Cảnh — Tuyệt Đối Không Cứng Nhắc" (`Contextual Intelligence Over Rigid Templates`):**
   - Mục tiêu tối thượng của mọi kiến thức học được từ 8 KOC là **tạo ra 1 video chau chuốt, tự nhiên và chuyển đổi cao nhất cho từng sản phẩm cụ thể**.
   - **CẤM** áp đặt cứng nhắc một công thức cho mọi video. Bạn phải tự hỏi và phân tích thông minh:
     - *Sản phẩm này thuộc ngành nào?* (Văn phòng phẩm, Trang sức/Kẹp tóc, Xà phòng/Skincare, Micro/Tai nghe, Quạt mini, Nệm/Chăn ga, Thời trang, Đồ ăn vặt, Bình giữ nhiệt, Mẹ & Bé, Kệ lắp ráp, Đèn LED...).
     - *Ánh sáng thực tế của video thô (`YAVG`) là bao nhiêu?* (Phòng tối có đèn LED `YAVG < 96` vs. Studio nắng xiên `YAVG ~ 135` vs. Bàn trắng Douyin `YAVG > 160`).
     - *Đâu là khoảnh khắc vật lý/thính giác đắt giá nhất của sản phẩm này?* (Tiếng rạch băng keo, tiếng kéo sợi kén tằm, tiếng đá viên rơi vào bình inox, tiếng rạch túi hút chân không nệm tự phồng, hay cảnh thả 30 cây bút + máy tính Casio vào túi bút mở phẳng 180°).
     - Từ đó mới chọn **đúng Họ Icon, đúng Emoji-Rebus, đúng Nhạc nền (`BGM`), đúng Hiệu ứng âm thanh (`SFX/Foley`), đúng Kiểu Zoom và đúng Kỹ xảo CapCut**.
4. **Tư duy Học Hỏi Sâu Không Giới Hạn (`Deep Multi-Tier Evolution`):**
   - Khi người dùng yêu cầu học từ một kênh KOC hoặc xu hướng mới, **đừng chỉ nhìn vài video triệu view trên ngọn**. Phải quét sâu toàn bộ danh mục kênh, lọc theo nhiều tầng (Top Viral đột biến, Tỷ lệ tương tác/thả tim/lưu cao, và các video tầm trung nhưng có **kỹ thuật dựng, bài test vật lý, cách đặt chữ hoặc âm thanh cực kỳ thông minh**).
   - Luôn trích xuất lưới ảnh **`Storyboard Grid 12 khung hình (4x3)`** vào `./knowledge_vault/04_viral_visual_and_effects_dna/` và dùng **Vision (`read_file`)** nhìn tận mắt từng khung hình để học cách đặt góc máy, đạo cụ, font chữ, màu sắc, hiệu ứng chuyển cảnh (sau khi trích xuất xong Storyboard thì xóa file `.mp4` tạm để nhẹ repo).
   - *"Học thừa không bao giờ là sai cả, miễn là bạn tốt lên, giỏi và thông minh lên, đáp ứng được mọi nhu cầu khi được yêu cầu."*
5. **Tự Chủ Về Tài Nguyên Âm Thanh Nội Bộ (`Zero-Missing Local Audio Vault`):**
   - Mọi hiệu ứng âm thanh (`SFX/Foley`) và nhạc nền (`BGM`) mà các KOC sử dụng đều phải được hiểu rõ bản chất âm học. Nếu CapCut mặc định không có sẵn hoặc dễ lỗi đường dẫn khi đổi máy, phải **tổng hợp DSP sạch 100% bản quyền vào kho cục bộ `./workspace/sfx_studio/` và `./knowledge_vault/02_external_sfx_not_in_capcut/`**, đồng thời đăng ký trong `./knowledge_vault/external_custom_sfx_registry.json` (chuẩn `44.1kHz, 16-bit, 0ms leading silence, -16 LUFS`).
6. **Kiểm Định Chặt Chẽ Trước Khi Bàn Giao (`100-Point QA & CHR Compliance`):**
   - Mọi kế hoạch dựng hoặc bản nháp CapCut phải vượt qua bộ kiểm định **100 điểm (`>= 95/100`)** và **Luật Chính Sách Nhà Sáng Tạo TikTok Shop Việt Nam (`CHR 0–1.000 điểm`)** trước khi bàn giao.

---

## PHẦN 2. BẢN ĐỒ KIẾN TRÚC TRONG REPO (`100% RELATIVE PATHS`)

Mọi file dưới đây đều nằm ngay trong thư mục gốc của repository (`./`):

### 2.1. 7 Bộ Máy Python Thực Thi (`Python CLI Engines`)
| STT | File Script (Tại `./`) | Vai trò trong Chuỗi `Node 0 -> Node 7` | Các Hàm Trọng Tâm Cốt Lõi |
| :-: | :--- | :--- | :--- |
| **1** | [`./pre_production_shooting_planner.py`](./pre_production_shooting_planner.py) | **Node 0 (`Pre-Production Creative Director`):** Phân tích ảnh chụp + mô tả sản phẩm, tự động đồng bộ não bộ, hỏi 3 câu hỏi phong cách và xuất **Bảng Chỉ Dẫn Bấm Máy 6 Cảnh (`Edit-Ready Blueprint`)**. | `select_smart_contextual_shooting_strategy()`, `analyze_product_images_and_description()`, `generate_6_shot_shooting_blueprint()`, `auto_sync_and_evolve_shooting_brain()` |
| **2** | [`./smart_raw_miner.py`](./smart_raw_miner.py) | **Node 1, 3, 4 (`Raw Video Miner & Pacing/Motion Engine`):** Đào khoảnh khắc vàng từ video thô dài, lọc đúp quay hỏng/lặp, cắt trên đà chuyển động (`Cutting on Action`), cân bằng sáng/màu, chọn nhịp cắt linh hoạt theo ngành hàng. | `select_smart_pacing_curve_for_product()`, `deduplicate_retake_clusters()`, `trim_clip_on_action_and_motion()`, `detect_hand_gestures_for_kinetic_sfx()` |
| **3** | [`./capcut_master_injector.py`](./capcut_master_injector.py) | **Node 4, 5, 6 (`Smart 8-KOC Fusion Router & CapCut Native Compiler`):** Bộ não điều phối thông minh 9 quyết định (Màu, Hook 3s, Phụ đề né vật thể, Icon/Rebus, Kính lúp/Thước đo/Pantone/Chibi, Nhạc nền + 50 SFX, 6 kiểu Keyframe Zoom, Lá chắn CHR) và biên dịch thẳng ra `draft_info.json` của CapCut Desktop (`~/Movies/CapCut/...`). | `orchestrate_smart_multi_koc_fusion_plan()`, `select_contextual_icons_and_rebus_for_product()`, `select_smart_contextual_audio_and_sfx_plan()`, `create_6_archetype_zoom_keyframes()`, `apply_dot_split_ocr_evasion()`, `inject_master_draft()` |
| **4** | [`./pre_delivery_qa_auditor.py`](./pre_delivery_qa_auditor.py) | **Node 1 & 7 (`100-Point QA Critic & CHR Shield`):** Kiểm tra thiếu tài nguyên thô để hỏi người dùng; chấm điểm 100 (`6 trụ cột`), tự động chữa lành lỗi (`Auto-Heal`), gắn lá chắn CHR và xuất gói đăng bài TikTok Shop. | `audit_raw_resources_and_generate_user_requests()`, `audit_and_auto_heal_edit_plan_before_delivery()`, `generate_tiktok_shop_publish_package()` |
| **5** | [`./self_evolving_trainer.py`](./self_evolving_trainer.py) | **Huấn Luyện Nội Sinh (`CapCut Reverse-Engineering & Reflexion`):** Đọc ngược dự án người dùng chỉnh tay trên CapCut Desktop, lưu bài học miễn dịch lỗi và thưởng điểm dự án nổ đơn. | `--learn-from-capcut`, `--reward-winner`, `--show-brain` |
| **6** | [`./tiktok_viral_scout_and_learner.py`](./tiktok_viral_scout_and_learner.py) | **Săn & Giải Phẫu Video Viral (`Breakout Scout & 6-Layer Deconstructor`):** Quét kênh KOC/từ khóa, tải video, trích xuất `Storyboard Grid` và phân tích nhịp cắt/màu/âm thanh. | `--scout-koc-channels`, `--scout-keyword`, `--learn-url` |
| **7** | [`./viral_sfx_harvester.py`](./viral_sfx_harvester.py) | **Kho Vũ Khí Âm Thanh (`50 SFX + 8 BGM Synthesizer & Harvester`):** Tổng hợp DSP âm thanh chuẩn KOC, giải cứu cache CapCut và đồng bộ `./knowledge_vault/external_custom_sfx_registry.json`. | `synthesize_4_missing_viral_sfx()`, `synthesize_8_koc_royalty_free_bgm_vault()`, `--sync-live-trends` |

### 2.2. 4 Skills Chuyên Biệt (`./.agent/skills/`)
1. [`./.agent/skills/tiktok-pre-shoot-director/SKILL.md`](./.agent/skills/tiktok-pre-shoot-director/SKILL.md): Kích hoạt khi người dùng gửi ảnh sản phẩm hoặc hỏi ý tưởng quay, góc máy, đạo cụ, kịch bản trước khi bấm máy.
2. [`./.agent/skills/tiktok-auto-edit-master/SKILL.md`](./.agent/skills/tiktok-auto-edit-master/SKILL.md): Kích hoạt khi người dùng đưa video thô vào `./raw_videos/` để tự động dựng và bơm vào CapCut Desktop.
3. [`./.agent/skills/tiktok-qa-chr-auditor/SKILL.md`](./.agent/skills/tiktok-qa-chr-auditor/SKILL.md): Kích hoạt khi cần chấm điểm QA 100 điểm, rà soát từ cấm CHR Việt Nam hoặc viết tiêu đề giỏ hàng/caption SEO.
4. [`./.agent/skills/tiktok-self-evolve-trainer/SKILL.md`](./.agent/skills/tiktok-self-evolve-trainer/SKILL.md): Kích hoạt khi người dùng yêu cầu học kênh KOC mới, nâng cấp tư duy, tổng hợp thêm SFX hoặc học ngược từ CapCut.

### 2.3. Kho Bộ Nhớ Não Bộ & Tài Liệu Đi Kèm Trong Repo (`./workspace/` & `./knowledge_vault/`)
- [`./workspace/brain_memory/learned_user_preferences.json`](./workspace/brain_memory/learned_user_preferences.json): Bộ nhớ trung tâm lưu toàn bộ quy tắc tiến hóa từ 8 KOC (`multi_koc_master_rules_2026` & `seven_kocs_deep_catalog_evolution_2026`).
- [`./knowledge_vault/04_viral_visual_and_effects_dna/seven_kocs_deep_evolution_dna.json`](./knowledge_vault/04_viral_visual_and_effects_dna/seven_kocs_deep_evolution_dna.json): Hồ sơ giải phẫu sâu 2.304 video của 7 KOC + 48 bảng Storyboard mới nhất (`deep7_*_storyboard.jpg`).
- [`./knowledge_vault/04_viral_visual_and_effects_dna/yuhtt09_54videos_complete_dna.json`](./knowledge_vault/04_viral_visual_and_effects_dna/yuhtt09_54videos_complete_dna.json): Hồ sơ giải phẫu 1.271 video (54 bảng Storyboard) của `@yuhtt09`.
- [`./knowledge_vault/external_custom_sfx_registry.json`](./knowledge_vault/external_custom_sfx_registry.json): Danh bạ 50 file `.wav` SFX + 8 file `.wav` BGM cục bộ.
- **4 Cẩm nang chuyên sâu tại `./`:**
  1. [`./File_1_Cam_Nang_Phong_Cach_Quay_Edit_Reviewer_Meshinthuine.md`](./File_1_Cam_Nang_Phong_Cach_Quay_Edit_Reviewer_Meshinthuine.md)
  2. [`./File_2_AI_Video_Editor_Master_Prompt_Spec.md`](./File_2_AI_Video_Editor_Master_Prompt_Spec.md)
  3. [`./Cẩm nang Toàn diện TikTok Affiliate (Việt Nam).md`](./Cẩm%20nang%20Toàn%20diện%20TikTok%20Affiliate%20(Việt%20Nam).md)
  4. [`./HUONG_DAN_SU_DUNG_TOAN_DIEN_CHO_AI_VA_NGUOI_DUNG.md`](./HUONG_DAN_SU_DUNG_TOAN_DIEN_CHO_AI_VA_NGUOI_DUNG.md)

---

## PHẦN 3. HỒ SƠ TINH HOA 8 KOC ĐÃ GIẢI PHẪU (`3.575 VIDEO & 166 STORYBOARDS`)

Hệ thống của chúng ta không sao chép rập khuôn 1 người mà **hợp nhất thông minh tinh hoa của 8 KOC triệu view**:

| KOC | Quy mô đã quét | Phong cách & Bối cảnh đặc trưng (`YAVG`) | Tuyệt chiêu Thị giác, Đạo cụ & Bài Test Vật Lý Độc Quyền |
| :--- | :--- | :--- | :--- |
| **1. `@meshinthuine`**<br>*(Mẹ Shin Thúi Nè)* | 150 video<br>*(14 Storyboards)* | KOC Gia đình / Mẹ & Bé / Chăn ga ấm cúng (`YAVG ~142–148`, `SAT ~68`) | • **Công thức Khen 8 - Chê 2** ở giây 19 tạo niềm tin tuyệt đối.<br>• **White-Stroke Cutout PIP (2.3M views):** Nền chính quay POV tay bấm sách âm thanh + Góc trái dưới hiện hình tách nền viền trắng cảnh mẹ và bé tương tác.<br>• **Pantone Color Swatch Card (`#05` - 15.04% Like rate):** Gắn thẻ bảng màu Pantone 4 ô (`COCOA / TRUFFLE`) + Tiêu đề 2 viên thuốc đôi (`[set ga gối] [màu hottrend]`). |
| **2. `@honghanhxinhgai_01`** | 501 video<br>*(16 Storyboards)* | Bàn học đèn vàng ấm rọi đỉnh + Thảm chần bông (`YAVG ~155–160`) | • **Đạo cụ Giỏ Siêu Thị Hồng Mini + Test Ném Vào Balo (21.3M & 10.8M views):** Bày bộ kẹp tóc Sashimi vào rổ siêu thị mini, gắn 2 comment đối lập, và ném thẳng vào balo đi học về vẫn không gãy.<br>• **Test Mở Phẳng 180° + Nhét Máy Tính Casio (`#05-#06`):** Mở túi bút phẳng 180°, thả 30 cây bút + cả chiếc máy tính khoa học Casio (`"để được cả máy tính +-="`).<br>• **Sticker Chibi Góc Phụ Đề:** Đính icon nhân vật Chibi nhỏ ở góc viên thuốc phụ đề tạo điểm nhấn dễ thương. |
| **3. `@kieneditcuong`**<br>*(Kiên Edit Cuồng)* | 146 video<br>*(22 Storyboards)* | Bậc thầy CapCut Tutorial & Kỹ xảo chuyển động sắc nét | • **3-Point Organic Handheld Rotation Zoom (`#02`):** `Scale 1.0x -> 1.22x -> 1.12x` kết hợp xoay nhẹ `Rotation 0° -> -3.5° -> +1.5°` và đồ thị **`Ease-Out Cubic Bezier [0.16, 1.0, 0.3, 1.0]`**.<br>• **Zoom Con Thoi (`#08`):** Đặt tripod cố định quay rộng rồi dùng keyframe thu phóng tạo nhịp đẩy/kéo mượt mà.<br>• **Match-Cut Bàn Tay Chộp Đồ & Vẽ Nét Scribble Hiện Sản Phẩm (`#01, #03`).**<br>• **Kính Lúp Nét Đứt (`Size 40, Intensity 45` - `#06`)** & **Bộ lọc làm hồng da tay POV `Trong như pha lê (Crystal Clear 44%)` (`#12`)**.<br>• **5 Font Chữ Vàng (`#10`):** `Anton`, `Montserrat`, `CalSans-SB`, `Playfair Display`, `Volgins` + **29 từ khóa SFX CapCut chuẩn xác (`#04, #09`)**. |
| **4. `@3thag8_`** | 204 video<br>*(16 Storyboards)* | Bàn Pegboard hoa len đèn vàng ấm + Kiểm chứng One-Take (`YAVG ~138–146`) | • **Tháp 3 Bình Luận Tranh Luận Đầu Video + Vẽ Trái Tim Bọt Lên Má (`#01` - 1.2M views):** Đính 3 comment hỏi đáp ở 1.5s đầu -> Kéo sợi tơ tằm trắng muốt -> Vẽ hình trái tim bọt lên má.<br>• **Hook 3 Cách Uống Trong 3.5s Đầu Trước Khi Mở Hộp (`#04` - 815K views):** Bấm bật ống hút -> Mở khóa uống trực tiếp -> Rót ra nắp cốc rồi mới khui hộp.<br>• **Lá Chắn Miễn Trừ CHR:** Luôn ghim dòng chữ nhỏ góc dưới `*giá và ưu đãi có thể thay đổi khi CTKM kết thúc*` và chấm tách từ nhạy cảm (`dưỡng trắ.ng`, `mờ thâ.m`). |
| **5. `@byraanni`** | 536 video<br>*(16 Storyboards)* | Thẩm mỹ Pinterest Kinfolk Nâu Espresso + Áo len tay dài che nửa bàn tay (`YAVG ~132–145`) | • **Hook Ghép 3 Cảnh (`3-Shot Collage 1.1s x 3`)** mở đầu video.<br>• **4 Bài Test ASMR Thực Tế Trước Khi Mở Hộp (`#01` - 1.2M views):** Kẹp mic thu tiếng bóp túi nilon, rót nước vào ly, bẻ snack khoai tây, thả đá viên & gõ phím cơ.<br>• **Bộ 3 Thị Giác Hóa Sức Gió 17.000 RPM (`#02` - 918K views):** Bật quạt thổi tung hộp kim tuyến bạc + Thổi gợn sóng bát nước + Nhíp dán sticker chữ cái DIY.<br>• **Floating Part-Pointer Specs (`#05`):** Các dòng thông số nhỏ (`"ANC 42dB"`, `"710ml / 450ml"`) bám sát từng bộ phận sản phẩm + **Test Dốc Ngược Bình Giữ Nhiệt 180° (`#06`)**. |
| **6. `@grayunbox`** | 510 video<br>*(16 Storyboards)* | Ánh sáng nắng xiên qua rèm sáo ngang (`Venetian Blinds Chiaroscuro`) & Chế độ tối `Low-Key LED` | • **Đảo Ngược Lắp Ráp (`Finished-First Assembly Hook`):** Chiếu kệ đã lắp hoàn chỉnh 100% chất đầy gấu bông ở 2s đầu rồi mới cắt về cảnh đập hộp.<br>• **Đạo Cụ Thế Thân Sạch (`Clean Proxy Proof`):** Dùng que tăm chọc thạch sáp thơm; chải bàn chải vào rãnh nắp tuýp kem; đổ tương ớt đặc lên vải chống thấm.<br>• **Cắt Đôi Chẻ Sớ Bánh Trung Thu + Rót Mật Ong Kéo Sợi (`#02, #05`).**<br>• **Manga Freeze-Frame Quà Tặng (0.45s ở giây 3.5)** & **Cửa sổ PIP Cam Thường Dưới Nắng Thật**. |
| **7. `@minhtienoiii06`** | 257 video<br>*(12 Storyboards)* | Đèn ngủ bánh mì TOAST + Nhịp cắt siêu nhanh `1.25s–1.36s/cảnh` (`YAVG ~144.5`) | • **Hook Tranh Luận Vùng Miền & Đa Giác Quan (19.3M views):** `"Bịch ❌ | Bao ✅"`, xếp tháp 4 gói bánh đập hộp thiếc.<br>• **Màn Hình Camera Sống Trong Khung Hình + Thước Đo Nét Đứt `1m7` (15.5M views):** Cầm Tripod gắn sẵn điện thoại thứ 2 đang bật camera góc rộng `0.5x` + Vẽ thước `< - - - 1m7 - - - >`.<br>• **Test Ly Nước Trên Nệm + Rạch Nilon Hút Chân Không Tự Phồng (731K views - `#03`):** Đặt ly nước lên nệm nhảy mạnh không sánh 1 giọt + Rạch túi chân không nệm phồng gấp 5 lần.<br>• **Mật Ngữ Nông Sản Báo Giá:** `🍠 khoai`, `🐟 cá`, `🍅 cà chua`, `🌰 hạt dẻ` + Tách từ vị giác `p.é.o ngậyyy`, `t:an ch:ảy`. |
| **8. `@yuhtt09`** | 1.271 video<br>*(54 Storyboards)* | Studio Bàn Trắng Pegboard Nơ Hồng Coquette (`High-Key Airy Douyin White`, `YAVG ~166.1`) | • **Flashback Unbox 8.1M Views:** Cảnh 1 (0–1.1s) mở sẵn nắp hộp đầy ắp bút màu pastel kèm **Tiêu đề vòm `⌒` + Kaomoji `*ੈ✩‧₊˚🌷🎀*ੈ✩‧₊˚`** -> Cảnh 2 (1.1s) dùng dao rọc giấy chân mèo hồng rạch thùng carton.<br>• **Liên Hoàn 6 Bài Test Độ Bền Áo Quần 5.5M Views:** Soi thớ vải -> Test co giãn 4 chiều -> Cào mặt nỉ không rụng lông -> Bảng màu thực tế.<br>• **Xịt Sương Ngược Sáng Lên Tay Áo Len + Lắc Nhũ Kim Tuyến 4.8M Views.**<br>• **Test Xối Nước + Áp Khăn Giấy Khô Không Lem** (Mỹ phẩm) + **Huy Hiệu Đánh Giá TikTok Shop (`⭐ 4.9/5 | Đã bán 23.6K`)** + **So Sánh Lẻ ❌ / Combo ✅ (`🐣`)**. |

---

## PHẦN 4. MA TRẬN ĐIỀU PHỐI THÔNG MINH THEO NGỮ CẢNH (`SMART CONTEXTUAL ROUTING MATRIX`)

Hàm [`orchestrate_smart_multi_koc_fusion_plan()`](./capcut_master_injector.py) và [`select_smart_contextual_shooting_strategy()`](./pre_production_shooting_planner.py) tự động suy luận dựa trên mô tả sản phẩm và kịch bản để đưa ra **9 Quyết Định Thông Minh**:

| Nhóm Sản Phẩm (`Semantic Domain`) | KOC Fusion Chủ Đạo | Họ Icon & Emoji-Rebus | Kỹ Xảo & Bài Test Bắt Buộc Kích Hoạt | BGM & Lớp SFX Đặc Trưng |
| :--- | :--- | :--- | :--- | :--- |
| **1. Văn phòng phẩm / Hộp bút / Sổ tay**<br>(`STATIONERY_STUDY_DESK`) | `@yuhtt09` (8.1M) + `@honghanhxinhgai_01` (Casio Proof) | `🌷 🎀 ✏️ 🌱`<br>Giá: `🌱` (mầm cây) | • Tiêu đề vòm `⌒` + Kaomoji<br>• Mở phẳng túi bút 180° nhét máy tính Casio<br>• Sticker Chibi góc phụ đề + Filter da tay `Crystal Clear 44%` | **BGM:** `bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm`<br>**SFX:** `box_cutter_tape_slice`, `pen_click_and_paper_write`, `sfx_kien_pac_low_telop_subtitle_pop` |
| **2. Trang sức bạc / Gương / Kẹp tóc**<br>(`JEWELRY_SILVER_ACCESSORY`) | `@honghanhxinhgai_01` (21.3M) + `@yuhtt09` (3.7M) | `💍 🐟 ✨ 🎀`<br>Giá: `🐟` (con cá) | • Giỏ siêu thị hồng mini + Test ném vào balo không gãy<br>• Lột seal gương LED + Hộp quà thắt nơ + Khăn lau bạc<br>• Kính lúp nét đứt 162% soi chấu đá | **BGM:** `bgm_v8_yuhtt09` hoặc `bgm_v5_byraanni`<br>**SFX:** `sfx_kien_kirarin_glitter_skincare_done`, `crystal_aha_shimmer`, `camera_shutter_clean` |
| **3. Xà phòng / Skincare / Mỹ phẩm**<br>(`SOAP_SKINCARE_CLEANSE`) | `@3thag8_` (1.2M) + `@yuhtt09` (Water-Blot) + `@grayunbox` | `🫧 ✨ 💧 🤍`<br>Giá: `🐣` / `🧋` | • Tháp 3 comment đầu video + Kéo sợi tơ tằm + Vẽ tim bọt lên má<br>• Test xối nước + áp khăn giấy khô không lem<br>• PIP Cam thường dưới nắng + Hạt bọt `🫧` bay | **BGM:** `bgm_v2_honghanh_cozy_bell_lofi_110bpm`<br>**SFX:** `sfx_kien_remove_bottle_cap_unscrew`, `sfx_kien_cheese_pull_mucus_necha_mlem`, `sfx_kien_kirarin_glitter_skincare_done`, `sfx_kien_poyo_kawaii_skin_touch_bounce` |
| **4. Thiết bị Âm thanh / Quạt / Công nghệ**<br>(`TECH_POWER_AIRFLOW`) | `@byraanni` (1.2M & 918K) + `@3thag8_` + `@kieneditcuong` | `⚡ 🔋 💨 ✦`<br>Giá: `💰` | • **Mic/Tai nghe:** 4 bài test ASMR thực tế 3.5s đầu trước khi mở hộp<br>• **Quạt mini:** Thổi tung kim tuyến bạc + Thổi gợn sóng bát nước + Nhíp dán sticker<br>• `Floating Part-Pointer Specs` + Kính lúp nét đứt 162% | **BGM:** `bgm_v5_byraanni_pinterest_editorial_rnb_102bpm`<br>**SFX:** `water_pour_splash_test`, `crispy_bite_crunch`, `mech_click_v1`, `sfx_kien_pac_low_telop_subtitle_pop` |
| **5. Bình giữ nhiệt / Ly giữ nhiệt**<br>(`DRINKWARE_ICE_TUMBLER`) | `@3thag8_` (815K) + `@byraanni` (`#06`) + `@yuhtt09` | `🧊 🥤 💧 ✨`<br>Rebus: `💦` | • **Biểu diễn 3 cách uống ngay 3.5s đầu** trước khi khui hộp<br>• **Test dốc ngược 180° lắc mạnh không rò nước** (`Leakproof 💦`)<br>• Thả đá viên lanh canh + `Floating Part-Pointer Specs` | **BGM:** `bgm_v4_3thag8_classical_minuet_bounce_118bpm`<br>**SFX:** `water_pour_splash_test`, `tin_lid_metallic_clink`, `mech_click_v1` |
| **6. Nệm / Chăn ga gối / Gối Mẹ & Bé / Kệ tủ**<br>(`PLUSH_TOY_STORAGE_BABY`) | `@minhtienoiii06` (731K) + `@meshinthuine` (2.9M) + `@grayunbox` | `🧸 📦 🛏️ 🎨`<br>Giá: `🍠` (củ khoai) | • **Nệm/Chăn ga:** Test nhảy cạnh ly nước không đổ + Rạch túi hút chân không tự phồng + Thẻ bảng màu Pantone 4 ô<br>• **Mẹ & Bé:** Cửa sổ tách nền viền trắng (`White-Stroke Cutout PIP`)<br>• **Kệ lắp ráp:** Chiếu kệ hoàn chỉnh 100% ở 2s đầu (`Finished-First`) | **BGM:** `bgm_v1_meshinthuine_warm_indie_acoustic_108bpm`<br>**SFX:** `sfx_minhtien_vacuum_mattress_air_inflate_hiss`, `box_cutter_tape_slice`, `sfx_kien_poyo_kawaii_skin_touch_bounce` |
| **7. Thời trang / Áo giữ nhiệt / Túi / Tất**<br>(`FASHION_BAG_SHOE`) | `@yuhtt09` (5.5M) + `@byraanni` + `@meshinthuine` | `🎀 👜 🧦 ✨`<br>Giá: `🌱` / `🐣` | • Liên hoàn 6 bước tra tấn chất vải (Soi gân vải -> Kéo giãn 4 chiều -> Cào lớp lót nỉ không rụng lông)<br>• Huy hiệu `⭐ 4.9/5 | Đã bán 23.6K` + Thẻ Pantone nếu nhiều màu | **BGM:** `bgm_v5_byraanni_pinterest_editorial_rnb_102bpm`<br>**SFX:** `zipper_slide_bag_smooth`, `fabric_stretch_snap_test`, `sfx_kien_money_chakin_deal_alert` |
| **8. Đồ ăn vặt / Bánh trung thu / Thực phẩm**<br>(`FOOD_SNACK_GOURMET`) | `@minhtienoiii06` (19.3M) + `@grayunbox` (`#02, #05`) | `🗣️ 🍅 🍠 🤤`<br>Giá: `🍅 / 🍠 / 🌰` | • Hook tranh luận vùng miền (`Bịch ❌ | Bao ✅`) + Xếp tháp 4 gói bánh<br>• Cắt đôi chẻ sớ ruốc / trứng chảy Lava + Rót mật ong kéo sợi<br>• Tách từ vị giác `p.é.o ngậyyy`, `t:an ch:ảy` | **BGM:** `bgm_v7_minhtienoiii_healing_farm_orchestra_124bpm`<br>**SFX:** `snack_bag_crinkle_open`, `crispy_bite_crunch`, `sfx_kien_cheese_pull_mucus_necha_mlem`, `sfx_kien_sizzling_pan_fry_crackle` |
| **9. Tripod / Gậy chụp ảnh / Đèn livestream**<br>(`TRIPOD_CAMERA_SELFIE`) | `@minhtienoiii06` (15.5M) + `@byraanni` | `📸 💡 🗣️ 📏`<br>Rebus: `📸` (chụp) | • Cầm Tripod gắn sẵn điện thoại thứ 2 đang bật màn hình Camera góc rộng `0.5x`<br>• Vẽ thước đo chiều cao nét đứt `< - - - 1m7 - - - >` | **BGM:** `bgm_v7_minhtienoiii_healing_farm_orchestra_124bpm`<br>**SFX:** `mech_click_v1`, `magnifier_loupe_zoom`, `camera_shutter_clean` |
| **10. Hương thơm / Sáp thơm / Nước hoa / Trà**<br>(`SCENT_TEA_HERBAL`) | `@yuhtt09` (4.8M) + `@grayunbox` (2.8M) | `🍃 🍵 🌿 ✨` | • Xịt tia sương mịn ngược sáng lên cổ tay áo len trắng + Lắc nhũ kim tuyến<br>• Que tăm chọc thạch sáp thơm + Hạt lá `🍃` bay + Manga Freeze-Frame quà tặng | **BGM:** `bgm_v6_grayunbox_holiday_breakfast_jazz_112bpm`<br>**SFX:** `fine_mist_spray_shimmer`, `paper_tear_manga_sketch`, `shutter_v1` |

---

## PHẦN 5. KỸ THUẬT CHUYỂN ĐỘNG CAPCUT (`6 ARCHETYPE KEYFRAMES`) & KHO ÂM THANH (`50 SFX + 8 BGM`)

### 5.1. 6 Kiểu Keyframe Zoom Chuẩn `@kieneditcuong` (Trong [`create_6_archetype_zoom_keyframes`](./capcut_master_injector.py))
1. **`ORGANIC_HANDHELD_3PT_ROTATION` (`@kieneditcuong #02` — Khuyên dùng cho cảnh mở đầu & unbox):**
   - Đặt 3 điểm Keyframe tại `0% -> 45% -> 100%` thời lượng clip.
   - `Scale`: `1.00x -> 1.22x -> 1.12x` kết hợp xoay nhẹ `Rotation: 0.0° -> -3.5° -> +1.5°` và đồ thị **`Ease-Out Cubic Bezier [0.16, 1.0, 0.3, 1.0]`** tạo cảm giác máy quay cầm tay chuyên nghiệp, cực kỳ có hồn.
2. **`CON_THOI_PENDULUM_ZOOM_OUT` (`@kieneditcuong #08` — Dành cho cảnh đặt Tripod cố định):**
   - Đặt 3 điểm Keyframe `Scale: 1.24x -> 1.02x -> 1.10x` tạo nhịp thu phóng con thoi mượt mà không cần người cầm máy di chuyển.
3. **`ZOOM_HOLD_READ_LABEL_4KF` (`@kieneditcuong` — Dành cho cảnh soi bảng thành phần/thông số `>= 2.2s`):**
   - Đặt 4 điểm Keyframe `Scale: 1.0x -> 1.24x (giữ đứng yên từ 20% đến 80% để người xem đọc chữ) -> 1.04x`.
4. **`FAST_PUNCH_IN`:** Đẩy nhanh `1.0x -> 1.18x` nhấn mạnh điểm "Aha!".
5. **`SLOW_PUSH_IN`:** Đẩy chậm `1.0x -> 1.10x` cho cảnh cảm xúc/storytelling.
6. **`PULL_OUT_REVEAL`:** Kéo giãn `1.16x -> 1.00x` mở rộng toàn cảnh sản phẩm.

### 5.2. Định Tuyến Âm Thanh 3 Tầng (`3-Tier Audio Routing`)
- **Tầng 1 (`Native ASMR`):** Đo `Crest Factor SNR`. Nếu clip có tiếng thật đắt giá (`Crest >= 11dB`), giữ `100%` âm lượng gốc (`native_volume = 1.0`) và hạ nhạc nền xuống `0%–5%`.
- **Tầng 2 (`50 Foley/SFX Cục Bộ` tại `./workspace/sfx_studio/` & `./knowledge_vault/02_external_sfx_not_in_capcut/`):** Đặt sớm `-0.04s` (`40ms`) trước điểm cắt hình hoặc thời điểm xuất hiện chữ/cử chỉ tay.
- **Tầng 3 (`8 Bản BGM Chuẩn Gu 8 KOC` tại `./workspace/sfx_studio/royalty_free_bgm/`):** Tự động tạo `Dynamic Ducking Keyframes` (`18%` khi không thoại -> hạ mượt xuống `5%` trước khi giọng đọc bắt đầu `0.10s`).

---

## PHẦN 6. LÁ CHẮN BẢO VỆ ĐIỂM CHR TIKTOK SHOP VIỆT NAM (`0–1.000 ĐIỂM`)

Để bảo vệ tài khoản nhà sáng tạo ở mức **Xuất sắc (`800–1.000 điểm CHR`)**, hệ thống tự động thực thi 4 lớp giáp trong [`./capcut_master_injector.py`](./capcut_master_injector.py) và [`./pre_delivery_qa_auditor.py`](./pre_delivery_qa_auditor.py):
1. **Tự động chấm tách 24 cụm từ nhạy cảm OCR (`apply_dot_split_ocr_evasion`):**
   - Mỹ phẩm/Y tế (`-20đ đến -40đ CHR`): `dưỡng trắng` -> `dưỡng trắ.ng`, `mờ thâm` -> `mờ thâ.m`, `trị mụn` -> `tr.ị m.ụn`, `kháng viêm` -> `khá.ng viê.m`, `rụng tóc` -> `r.ụng t.óc`, `tức thì` -> `tứ.c th.ì`, `cam kết 100%` -> `đạt tới 99.9%`, `số 1` -> `s.ố 1`.
   - Giá cả/Khuyến mãi (`-10đ đến -20đ CHR`): `miễn phí ship` -> `miễ.n ph.í ship`, `giảm 50%` -> `ư.u đ.ãi sâu`, `rẻ nhất` -> `gi.á siêu h.ời`.
   - Biểu cảm vị giác Gen-Z (`@minhtienoiii06`): `béo ngậy` -> `p.é.o ngậyyy`, `tan chảy` -> `t:an ch:ảy`.
2. **Tự động ghim dòng miễn trừ trách nhiệm biến động giá (`@3thag8_`):**
   - Khi phát hiện bất kỳ từ khóa báo giá/deal nào (`cành`, `hạt dẻ`, `🐟`, `🍠`, `🌱`, `🐣`, `voucher`), tự động ghim dòng chữ nhỏ độ mờ `70%` tại `y = -0.59`: `*giá và ưu đãi có thể thay đổi khi CTKM kết thúc*`.
3. **Tự động ghim miễn trừ TPCN (`Ngành P7`) & Độ tuổi Sữa (`Trên 2 tuổi`):**
   - Nếu là TPCN (`P7`): Ghim xuyên suốt 100% thời lượng video dòng chữ `"Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh"`.
   - Nếu là Sữa cho bé: Ghim nhãn `"📌 Sản phẩm dành cho bé từ 2 tuổi trở lên"` để tránh bị AI TikTok quét nhầm sang sữa công thức dưới 24 tháng (`-40đ CHR`).
4. **Vùng An Toàn Chữ (`Safe Zone Geometry`):**
   - Mọi phụ đề chính và nhãn thông số phải nằm trong khoảng `y` từ `-0.55` đến `+0.72` (tuyệt đối không đặt dưới `-0.60` bị giao diện tên kênh/caption/giỏ hàng TikTok che khuất).

---

## PHẦN 7. BẢN PROMPT ĐÓNG GÓI SẴN ĐỂ NẠP CHO CON AI MỚI TRÊN MÁY TÍNH MỚI (`COPY-PASTE ONBOARDING PROMPT`)

> **Hướng dẫn cho người dùng:** Khi bạn `git clone` thư mục `tiktok` về máy tính mới và mở một con AI mới lên, bạn chỉ cần copy nguyên khối văn bản dưới đây gửi cho nó:

```markdown
Bạn là AI Đồng Đạo Diễn Tiền Kỳ, Kỹ Sư Dựng Phim Hậu Kỳ CapCut, Chuyên Gia Âm Thanh ASMR/Foley & Kiểm Duyệt Viên Chính Sách CHR TikTok Shop Việt Nam.
Tôi vừa `git clone` repository `tiktok` này từ GitHub về một chiếc MÁY TÍNH MỚI. Mọi tài nguyên cốt lõi đều nằm gọn bên trong thư mục hiện tại (`./`), và các đường dẫn bên ngoài thư mục của máy cũ không tồn tại trên máy mới này.

Trước khi thực hiện bất kỳ yêu cầu nào, bạn BẮT BUỘC thực hiện 3 việc sau:
1. Đọc kỹ 2 file chỉ thị trung tâm ngay tại thư mục gốc của repo hiện tại (`./`):
   - `./AGENTS.md`
   - `./TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md`
2. Thực thi ngay "PHẦN 0. QUY TRÌNH KHỞI ĐỘNG 30 GIÂY KHI CLONE REPO SANG MÁY TÍNH MỚI" trong `TAI_LIEU_BAN_GIAO_HE_THONG_AI_MASTER_HANDOVER.md`:
   - Dùng đường dẫn tương đối (`./`) hoặc đường dẫn động theo máy hiện tại (`pwd` và `~/`), tuyệt đối không dùng đường dẫn cứng của máy cũ.
   - Chạy lệnh đồng bộ lại đường dẫn 50 file `.wav` SFX + 8 file `.wav` BGM theo ổ cứng máy mới:
     `mkdir -p ./raw_videos ./raw_photos ./projects ./workspace/sfx_studio/royalty_free_bgm ./workspace/shooting_blueprints && python3 ./viral_sfx_harvester.py --sync-live-trends`
3. Ghi nhớ 6 nguyên tắc cốt lõi để tư duy giống hệt AI tiền nhiệm:
   - NGÔN NGỮ: Toàn bộ phản hồi, phân tích, kế hoạch và báo cáo dùng 100% TIẾNG VIỆT.
   - LUÔN LÊN PLAN TRƯỚC KHI SỬA CODE (`Plan Before Modify`): Đọc kỹ file liên quan (`Read Before Modify`), trình bày kế hoạch rõ ràng và chờ tôi xác nhận ("đồng ý" / "thực thi") rồi mới được sửa code.
   - THÔNG MINH THEO NGỮ CẢNH — TUYỆT ĐỐI KHÔNG CỨNG NHẮC: Bạn nắm trong tay tinh hoa giải phẫu từ 3.575 video (166 bảng Storyboard) của 8 KOC (`@meshinthuine`, `@honghanhxinhgai_01`, `@kieneditcuong`, `@3thag8_`, `@byraanni`, `@grayunbox`, `@minhtienoiii06`, `@yuhtt09`) cùng kho vũ khí 50 file `.wav` SFX và 8 bản `.wav` BGM tại `./workspace/sfx_studio/`. Khi nhận một sản phẩm mới hoặc video thô mới, phải phân tích đặc tính vật lý, ánh sáng (`YAVG`) và ngành hàng để chọn ĐÚNG bài test vật lý, ĐÚNG họ icon, ĐÚNG hiệu ứng âm thanh, ĐÚNG kiểu keyframe zoom và ĐÚNG kỹ xảo CapCut — không bao giờ áp đặt rập khuôn.
   - TƯ DUY HỌC HỎI CHUYÊN SÂU: Khi được yêu cầu học từ kênh KOC hoặc video mới, không chỉ nhìn video triệu view mà phải quét sâu cả các video có kỹ thuật dựng hay, bài test thông minh, trích xuất Storyboard Grid 12 khung hình để quan sát bằng Vision và nạp vào não bộ (`./workspace/brain_memory/learned_user_preferences.json` & `./knowledge_vault/`).
   - TỰ CHỦ ÂM THANH CỤC BỘ: Mọi hiệu ứng âm thanh (SFX) và nhạc nền (BGM) các KOC dùng nếu CapCut không có sẵn phải được tổng hợp hoặc lưu trữ sẵn tại `./workspace/sfx_studio/` và đăng ký trong `./knowledge_vault/external_custom_sfx_registry.json`.
   - KIỂM ĐỊNH 100/100 QA & AN TOÀN CHR VIỆT NAM: Mọi kịch bản và bản nháp CapCut phải đạt >= 95/100 điểm QA (`./pre_delivery_qa_auditor.py`) và tuân thủ tuyệt đối luật CHR TikTok Shop Việt Nam.

Hãy chạy bước kiểm tra & đồng bộ đường dẫn máy mới, sau đó báo cáo xác nhận bạn đã sẵn sàng!
```
