---
description: Đọc ảnh chụp sản phẩm + mô tả, hỏi 3 câu chốt phong cách và xuất Bản Thiết Kế 6 Cảnh Cần Quay khớp 100% với bộ Edit tự động (Node 0).
---

Hãy kích hoạt ngay Skill `tiktok-pre-shoot-director` (`.claude/skills/tiktok-pre-shoot-director/SKILL.md`) với tham số đầu vào từ người dùng: `$ARGUMENTS`.

1. Nếu người dùng truyền đường dẫn ảnh hoặc có ảnh mới trong `./raw_photos/`, hãy đọc trực tiếp bức ảnh bằng Vision để phân tích hình dáng, bề mặt bao bì, màu sắc và rủi ro chính sách CHR Việt Nam.
2. Chạy `python3 /Users/huynguyen/Desktop/tiktok/pre_production_shooting_planner.py --ask-questions` (tự động `Auto-Update` từ não bộ `brain_memory/`).
3. Hỏi người dùng 3 câu chốt phong cách (`Vibe V1-V4`, `Talent T1-T3`, `Props B1-B3`) rồi xuất **Bản Thiết Kế 6 Cảnh Cần Quay (`Edit-Ready Shooting Blueprint`)** kèm lời thoại gợi ý 28s và khóa file `./workspace/shooting_blueprints/<slug>_shooting_plan.json`!
