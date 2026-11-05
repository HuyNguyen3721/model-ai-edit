#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRE-PRODUCTION AI CREATIVE DIRECTOR & SMART SHOOTING BLUEPRINT (NODE 0)
Đầu vào:
  - 1 hoặc nhiều ảnh chụp sản phẩm thực tế (--images)
  - Mô tả sản phẩm, điểm mạnh, giá bán, tệp khách hàng (--description)
Chức năng:
  1. Giải phẫu hình ảnh sản phẩm (Màu sắc bao bì, Độ phản sáng, Ngành hàng P1-P7, Rủi ro CHR)
  2. Tra cứu Bộ Nhớ Tự Học (learned_viral_patterns.json & gold_winning_templates.json)
  3. Sinh Bộ 3 Câu Hỏi Chọn Phong Cách trước khi quay (--ask-questions)
  4. Sinh Bản Đề Xuất 6 Cảnh Cần Quay (Resource Checklist) khớp 100% với Bộ Edit Tự Động (Node 1-7)
"""

import os
import re
import json
import time
import shutil
import argparse
import subprocess
from typing import Dict, Any, List, Optional

PROJECTS_ROOT_DIR = "./projects"
RAW_PHOTOS_INBOX = "./raw_photos"
RAW_VIDEOS_INBOX = "./raw_videos"
BLUEPRINT_DIR = "./workspace/shooting_blueprints"
BRAIN_DIR = "./workspace/brain_memory"
LEARNED_VIRAL_PATTERNS_FILE = os.path.join(BRAIN_DIR, "learned_viral_patterns.json")
GOLD_WINNERS_FILE = os.path.join(BRAIN_DIR, "gold_winning_templates.json")


def setup_and_ingest_project_photos(project_slug: str, explicit_images: List[str]) -> Dict[str, Any]:
    """
    CƠ CHẾ QUẢN LÝ THƯ MỤC DỰ ÁN TỰ ĐỘNG & HỘP THƯ ĐẾN TỰ DỌN (AUTO-ARCHIVE INBOX):
    1. Tạo ngăn chứa riêng biệt cho từng sản phẩm tại:
       - `./projects/<project_slug>/photos/`
       - `./projects/<project_slug>/videos/`
       - `./projects/<project_slug>/blueprint/`
    2. Nếu người dùng bỏ ảnh vào `./raw_photos/` (mà không cần xóa hay tạo thư mục),
       hệ thống tự động di chuyển (Auto-Move) toàn bộ ảnh từ `./raw_photos/` sang
       `./projects/<project_slug>/photos/` để `./raw_photos/` luôn sạch trống cho lần sau!
    """
    proj_root = os.path.abspath(os.path.join(PROJECTS_ROOT_DIR, project_slug))
    photos_dir = os.path.join(proj_root, "photos")
    videos_dir = os.path.join(proj_root, "videos")
    bp_dir = os.path.join(proj_root, "blueprint")
    for d in (photos_dir, videos_dir, bp_dir, RAW_PHOTOS_INBOX, RAW_VIDEOS_INBOX):
        os.makedirs(d, exist_ok=True)

    inbox_abs = os.path.abspath(RAW_PHOTOS_INBOX)
    candidate_imgs: List[str] = [p for p in explicit_images if os.path.exists(p)]

    # Nếu không truyền đường dẫn cụ thể, tự động quét mọi ảnh đang nằm trong ./raw_photos/
    if not candidate_imgs and os.path.exists(inbox_abs):
        for fn in sorted(os.listdir(inbox_abs)):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".heic")):
                candidate_imgs.append(os.path.join(inbox_abs, fn))

    isolated_photos: List[str] = []
    for src_path in candidate_imgs:
        src_abs = os.path.abspath(src_path)
        dst_path = os.path.join(photos_dir, os.path.basename(src_abs))
        if os.path.commonpath([src_abs, inbox_abs]) == inbox_abs:
            # Ảnh nằm trong hộp thư ./raw_photos/ -> Tự động Move sang thư mục riêng của Dự Án
            if src_abs != dst_path:
                shutil.move(src_abs, dst_path)
            isolated_photos.append(dst_path)
        else:
            if src_abs != dst_path and not os.path.exists(dst_path):
                shutil.copy2(src_abs, dst_path)
            isolated_photos.append(dst_path if os.path.exists(dst_path) else src_abs)

    # Nếu trước đó dự án đã có ảnh trong ./projects/<project_slug>/photos/ thì lấy ra dùng
    if not isolated_photos and os.path.exists(photos_dir):
        for fn in sorted(os.listdir(photos_dir)):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".heic")):
                isolated_photos.append(os.path.join(photos_dir, fn))

    return {
        "project_slug": project_slug,
        "project_root_dir": proj_root,
        "isolated_photos_dir": photos_dir,
        "isolated_videos_dir": videos_dir,
        "isolated_blueprint_dir": bp_dir,
        "project_photos": isolated_photos
    }


# ==============================================================================
# 1. CƠ SỞ DỮ LIỆU ĐẶC TÍNH QUAY & DỰNG THEO 7 NGÀNH HÀNG (P1 - P7)
# ==============================================================================

PRODUCT_ARCHETYPE_SHOOTING_RULES: Dict[str, Dict[str, Any]] = {
    "P1": {
        "name": "Mỹ Phẩm, Skincare & Chăm Sóc Cá Nhân",
        "keywords": ["kem", "serum", "sữa rửa mặt", "toner", "chống nắng", "son", "dầu gội", "tẩy trang", "mặt nạ", "skincare", "dưỡng ẩm", "mụn", "trắng da"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cận cảnh Macro 15cm giọt serum chảy trên da hoặc đầu ngón tay tán chất kem tan mướt dưới ánh sáng tạt 45 độ",
        "native_asmr_trigger": "Tiếng bóp vòi pump 'xịt/tạch', tiếng xoáy nắp lọ thủy tinh, tiếng vỗ nhẹ chất kem lên mu bàn tay",
        "honest_con_suggestions": [
            "Mùi thảo mộc tự nhiên lúc mới mở nắp hơi rõ trong 3 giây đầu (do không dùng hương liệu nhân tạo), nhưng thoa lên 10 giây là bay hết",
            "Vỏ lọ làm dày dặn cầm hơi đầm tay khi mang đi du lịch, bù lại rơi không sợ vỡ",
            "Chất kem đặc nên chỉ cần lấy bằng hạt đậu là đủ, lấy nhiều quá sẽ lâu thấm hơn"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG quay cảnh so sánh làn da đã qua chỉnh sửa filter làm mịn với làn da mộc.",
            "❌ KHÔNG nói các từ y khoa tuyệt đối khi thu âm: 'trị dứt điểm mụn/nám 100%', 'thần dược', 'trắng bật 5 tông tức thì'."
        ],
        "default_bgm_mode": "M3_AESTHETIC_CHILL_SYNTH"
    },
    "P2": {
        "name": "Đồ Gia Dụng Thông Minh, Nhà Bếp & Vệ Sinh",
        "keywords": ["máy xay", "nồi", "chảo", "cây lau", "bình giữ nhiệt", "máy hút bụi", "kệ", "tẩy", "rửa", "gia dụng", "bếp", "hộp đựng", "dao", "kéo"],
        "recommended_vibe": "V3",
        "visual_aha_hook": "Cảnh thực chiến ngay giây đầu tiên: nhấn nút máy xay nhuyễn trong 2 giây hoặc lau 1 đường sạch bóng vết bẩn cứng đầu",
        "native_asmr_trigger": "Tiếng nút bấm cơ học 'tạch', tiếng động cơ chạy êm nhưng khỏe, tiếng gõ móng tay lên thân inox/nhựa ABS dày dặn",
        "honest_con_suggestions": [
            "Dây điện đi kèm hơi ngắn (khoảng 80cm) nên phải đặt gần ổ cắm, bù lại công suất máy rất khỏe",
            "Đóng gói 2 lớp xốp hơi kỹ quá nên lúc khui hộp hơi mỏi tay, nhưng nhờ vậy giao xa không móp méo",
            "Lưỡi dao/bề mặt rất sắc bén nên lúc tháo ra vệ sinh mọi người nhớ cẩn thận tay"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG cắt ghép ngắt cảnh giữa lúc 'Đang bẩn' và 'Đã sạch' (Dễ bị AI TikTok phạt -10đ lỗi Phóng đại hiệu quả). Bắt buộc quay liền mạch One-Take!",
            "❌ KHÔNG để vật sắc nhọn (dao/kéo) chĩa thẳng vào ống kính ở 3 giây đầu mà không có ngữ cảnh nấu ăn."
        ],
        "default_bgm_mode": "M2_SELECTIVE_HOOK_AND_CTA_SYNC"
    },
    "P3": {
        "name": "Thời Trang, Phụ Kiện, Giày Dép & Túi Xách",
        "keywords": ["áo", "quần", "váy", "đầm", "túi", "giày", "dép", "kính", "mũ", "thắt lưng", "vớ", "tất", "khoác", "form"],
        "recommended_vibe": "V4",
        "visual_aha_hook": "Cảnh biến hình (Transition) mặc lên người xoay 1 vòng hoặc kéo giãn hết cỡ chất vải để chứng minh độ đàn hồi không bai dão",
        "native_asmr_trigger": "Tiếng kéo khóa zip kim loại mượt mà, tiếng xé túi zip đóng gói, tiếng miết tay lên thớ vải dày dặn",
        "honest_con_suggestions": [
            "Lúc mới mở túi vẫn còn 1-2 sợi chỉ thừa nhỏ ở mặt trong đường vắt sổ, cắt nhẹ là đẹp",
            "Form may chuẩn nên ai thích mặc rộng thoải mái hoặc có bụng dưới thì nên nhích lên 1 size nhé",
            "Màu ngoài đời trầm hơn ảnh hãng chụp studio khoảng 5% nhưng nhìn thực tế lại sang và tây hơn"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG để lộ logo các thương hiệu xa xỉ lớn (Gucci, Chanel, LV, Nike...) trên nền hoặc trên sản phẩm nếu không có giấy ủy quyền (-40đ CHR).",
            "❌ KHÔNG quay góc máy quá nhạy cảm khi thử đồ (tránh lỗi Hở hang -20đ CHR)."
        ],
        "default_bgm_mode": "M1_FULL_BEAT_SYNC"
    },
    "P4": {
        "name": "Mẹ & Bé, Đồ Chơi Giáo Dục & Chăm Sóc Gia Đình",
        "keywords": ["bé", "bỉm", "tã", "sữa", "bình sữa", "đồ chơi", "khăn ướt", "ăn dặm", "mẹ bầu", "trẻ em", "gặm nướu", "xe đẩy"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cảnh test độ an toàn/mềm mại trực tiếp trên tay mẹ (đổ nước thử độ thấm hút của bỉm hoặc bóp thử độ mềm không góc cạnh của đồ chơi)",
        "native_asmr_trigger": "Tiếng bóp đồ chơi/nhựa silicone đàn hồi, tiếng xé miếng dán êm ái, tiếng lắc nhẹ",
        "honest_con_suggestions": [
            "Thiết kế màu pastel dịu mắt nên không quá sặc sỡ như hàng chợ, nhưng nhựa nguyên sinh cực kỳ an toàn không mùi",
            "Nắp đậy khóa chống tràn hơi chặt với người lần đầu mở, nhưng nhờ vậy bé có ném cũng không đổ"
        ],
        "chr_forbidden_scenes": [
            "❌ CẢNH BÁO ĐỎ CHR (-40đ): TUYỆT ĐỐI KHÔNG quay cảnh trẻ vị thành niên/em bé xuất hiện một mình trong khung hình mà không có người lớn đi kèm!",
            "❌ CẢNH BÁO ĐỎ LUẬT VIỆT NAM: Tuyệt đối KHÔNG nhận quay quảng cáo Sữa công thức cho trẻ dưới 24 tháng tuổi, Bình bú và Vú ngậm nhân tạo."
        ],
        "default_bgm_mode": "M4_PURE_ASMR_VOICE_DRIVEN"
    },
    "P5": {
        "name": "Thực Phẩm, Đồ Ăn Vặt, Đặc Sản & Đồ Uống",
        "keywords": ["bánh", "kẹo", "trà", "cà phê", "khô gà", "khô bò", "hạt", "sốt", "mì", "ăn vặt", "ngũ cốc", "socola", "mật ong"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cận cảnh bẻ đôi chiếc bánh/miếng thịt thấy rõ nhân chảy hoặc thớ sợi bên trong kèm biểu cảm cắn miếng đầu tiên",
        "native_asmr_trigger": "Tiếng nhai giòn rụm 'rộp rộp' sát mic 15cm, tiếng bật nắp lon 'xì', tiếng rót đá lạnh lách cách",
        "honest_con_suggestions": [
            "Vị làm theo gu ít ngọt (giảm khoảng 30% đường) nên ai hảo ngọt đậm sẽ thấy hơi thanh, nhưng ăn hoài không ngấy",
            "Gói zip mở ra thơm quá dễ ăn hết veo trong 1 buổi tối nên hơi hao ví"
        ],
        "chr_forbidden_scenes": [
            "❌ Bắt buộc quay thấy rõ hạn sử dụng và bao bì nhãn mác sạch sẽ trên vỏ hộp.",
            "❌ Không cam kết công dụng chữa bệnh hay giảm cân cấp tốc khi ăn thực phẩm thông thường."
        ],
        "default_bgm_mode": "M4_PURE_ASMR_VOICE_DRIVEN"
    },
    "P6": {
        "name": "Phụ Kiện Công Nghệ, Điện Tử, Đèn & Thiết Bị Số",
        "keywords": ["tai nghe", "loa", "sạc", "cáp", "ốp lưng", "đèn", "chuột", "bàn phím", "giá đỡ", "gimbal", "mic", "pin dự phòng"],
        "recommended_vibe": "V3",
        "visual_aha_hook": "Cảnh test tính năng ăn tiền nhất ngay 1.5s đầu (bật đèn sáng rực trong phòng tối, test thu âm khử ồn trước/sau, hoặc thả rơi test chống sốc)",
        "native_asmr_trigger": "Tiếng gõ phím cơ 'thocky', tiếng nắp hộp tai nghe đóng 'tách' nam châm, tiếng cắm cáp sạc chắc nịch",
        "honest_con_suggestions": [
            "Chất liệu vỏ nhám mờ nhìn rất sang nhưng nếu tay ra mồ hôi dầu sẽ hơi lưu dấu nhẹ, lau qua là sạch",
            "Sách hướng dẫn đi kèm chữ hơi nhỏ, nhưng thực ra chỉ cần cắm vào / bật Bluetooth là tự nhận ngay"
        ],
        "chr_forbidden_scenes": [
            "❌ Không dùng tên thương hiệu Apple/Samsung làm tên sản phẩm nếu chỉ là phụ kiện bên thứ 3 (phải nói rõ 'Dùng cho máy...')."
        ],
        "default_bgm_mode": "M2_SELECTIVE_HOOK_AND_CTA_SYNC"
    },
    "P7": {
        "name": "Thực Phẩm Bảo Vệ Sức Khỏe (TPCN) & Vitamin",
        "keywords": ["viên uống", "collagen", "vitamin", "bổ sung", "canxi", "omega", "kẽm", "sắt", "đề kháng", "thực phẩm bảo vệ sức khỏe"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cận cảnh viên uống/gói bột hòa tan trong cốc nước trong suốt kết hợp quay rõ tem nhãn chính hãng",
        "native_asmr_trigger": "Tiếng mở nắp lọ bảo hiểm, tiếng khuấy thìa vào ly thủy tinh",
        "honest_con_suggestions": [
            "Vì là dòng bổ sung từ từ nên phải kiên trì uống đều đặn sau bữa ăn chứ không thể ngày một ngày hai mà thấy ngay được",
            "Viên uống kích thước chuẩn nên nhớ uống kèm nhiều nước ấm cho dễ nuốt nhé"
        ],
        "chr_forbidden_scenes": [
            "❌ CẢNH BÁO ĐỎ CHR (-20đ đến -40đ): TUYỆT ĐỐI KHÔNG nói từ 'Thuốc', 'Chữa bệnh', 'Điều trị'.",
            "❌ BẮT BUỘC phải đọc hoặc để dòng chữ miễn trừ: 'Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh'."
        ],
        "default_bgm_mode": "M3_AESTHETIC_CHILL_SYNTH"
    }
}


# ==============================================================================
# 2. PHÂN TÍCH ẢNH CHỤP SẢN PHẨM & MÔ TẢ (VISUAL + DESCRIPTION PROFILER)
# ==============================================================================

def analyze_product_photos_and_description(
    image_paths: List[str],
    description: str,
    override_archetype: Optional[str] = None
) -> Dict[str, Any]:
    """
    1. Phân loại ngành hàng (P1-P7) từ mô tả & ảnh.
    2. Đo độ sáng (YAVG), độ bão hòa (SATAVG) và tính chất phản quang của sản phẩm từ ảnh chụp thực tế.
    3. Tra cứu kho não bộ tự học (`learned_viral_patterns.json`) để lấy công thức nhịp cắt đang viral.
    """
    desc_lower = description.lower()
    detected_arch = override_archetype or "P2"
    if not override_archetype:
        best_hits = 0
        for code, info in PRODUCT_ARCHETYPE_SHOOTING_RULES.items():
            hits = sum(1 for kw in info["keywords"] if kw in desc_lower)
            if hits > best_hits:
                best_hits = hits
                detected_arch = code

    arch_rules = PRODUCT_ARCHETYPE_SHOOTING_RULES.get(detected_arch, PRODUCT_ARCHETYPE_SHOOTING_RULES["P2"])

    # Đo thông số quang học từ ảnh chụp sản phẩm đầu tiên bằng FFmpeg
    img_metrics = {
        "valid_images": [p for p in image_paths if os.path.exists(p)],
        "avg_luminance_yavg": 135.0,
        "avg_saturation_satavg": 85.0,
        "surface_glare_warning": False,
        "lighting_advice": "Ánh sáng tự nhiên cạnh cửa sổ hoặc đèn Softbox chếch góc 45 độ."
    }

    if img_metrics["valid_images"]:
        first_img = img_metrics["valid_images"][0]
        cmd = [
            "ffmpeg", "-hide_banner", "-i", first_img,
            "-vf", "signalstats,metadata=print:file=-",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        y_match = re.search(r"lavfi\.signalstats\.YAVG=([0-9.]+)", res.stdout)
        ymax_match = re.search(r"lavfi\.signalstats\.YMAX=([0-9.]+)", res.stdout)
        sat_match = re.search(r"lavfi\.signalstats\.SATAVG=([0-9.]+)", res.stdout)

        if y_match:
            img_metrics["avg_luminance_yavg"] = round(float(y_match.group(1)), 1)
        if sat_match:
            img_metrics["avg_saturation_satavg"] = round(float(sat_match.group(1)), 1)
        if ymax_match and float(ymax_match.group(1)) >= 250.0:
            img_metrics["surface_glare_warning"] = True
            img_metrics["lighting_advice"] = (
                "⚠️ Phát hiện bao bì/bề mặt sản phẩm trong ảnh có độ bóng phản quang cao (YMAX >= 250). "
                "Khi quay video, hãy đặt đèn lệch góc 45 độ so với ống kính, KHÔNG chiếu đèn thẳng trực diện để tránh bị lóa trắng mất chữ trên nhãn!"
            )

    # Tra cứu & Tự động nâng cấp (Auto-Update) từ 4 nguồn trong Bộ Nhớ Tự Học
    viral_trend_hint = auto_sync_and_evolve_shooting_brain(detected_arch, arch_rules)

    return {
        "product_description": description,
        "detected_archetype": detected_arch,
        "archetype_name": arch_rules["name"],
        "image_optical_analysis": img_metrics,
        "visual_aha_hook": viral_trend_hint.get("evolved_visual_hook", arch_rules["visual_aha_hook"]),
        "native_asmr_trigger": arch_rules["native_asmr_trigger"],
        "honest_con_suggestions": arch_rules["honest_con_suggestions"],
        "chr_forbidden_scenes": arch_rules["chr_forbidden_scenes"],
        "recommended_vibe": viral_trend_hint.get("evolved_recommended_vibe", arch_rules["recommended_vibe"]),
        "recommended_talent_mode": viral_trend_hint.get("evolved_talent_mode", "T1"),
        "default_bgm_mode": viral_trend_hint.get("evolved_bgm_mode", arch_rules["default_bgm_mode"]),
        "viral_trend_hint": viral_trend_hint
    }


def auto_sync_and_evolve_shooting_brain(archetype: str, base_arch_rules: Dict[str, Any]) -> Dict[str, Any]:
    """
    CƠ CHẾ AUTO-UPDATE TỨC THÌ (ZERO-LATENCY SELF-EVOLVING SHOOTING BRAIN):
    Tự động chạy ngầm trước MỌI LẦN đề xuất quay để tổng hợp tri thức mới nhất từ 4 nguồn:
      1. `learned_viral_patterns.json` (Các video TikTok đột biến vừa được AI săn & mổ xẻ 6 lớp)
      2. `gold_winning_templates.json` (Các dự án nổ đơn/triệu view của chính bạn)
      3. `learned_user_preferences.json` (Thói quen cắt ghép, đặt chữ, chỉnh nhạc của bạn trên CapCut)
      4. `reflexion_lessons.jsonl` (Các lỗi từng gặp khi quay/dựng ở các video trước để nhắc nhở phòng tránh)
    Lưu kết quả tiến hóa vào `./workspace/brain_memory/learned_shooting_rules_by_archetype.json`.
    """
    os.makedirs(BRAIN_DIR, exist_ok=True)
    evolved_rules_file = os.path.join(BRAIN_DIR, "learned_shooting_rules_by_archetype.json")
    user_prefs_file = os.path.join(BRAIN_DIR, "learned_user_preferences.json")
    reflexion_file = os.path.join(BRAIN_DIR, "reflexion_lessons.jsonl")

    evolved_state: Dict[str, Any] = {
        "archetype": archetype,
        "last_auto_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "target_hook_dur_sec": 1.5,
        "target_avg_cut_sec": 1.85,
        "cuts_in_first_3_sec": 2,
        "evolved_recommended_vibe": base_arch_rules.get("recommended_vibe", "V1"),
        "evolved_talent_mode": "T1",
        "evolved_bgm_mode": base_arch_rules.get("default_bgm_mode", "M3_AESTHETIC_CHILL_SYNTH"),
        "evolved_visual_hook": base_arch_rules.get("visual_aha_hook", ""),
        "recommended_transition": "Clean Action Cut + Punch-In Zoom 1.15x ở cảnh 2",
        "personal_filming_reminders": [],
        "user_preferred_subtitle_y": -0.52,
        "learned_sources_count": 0
    }

    # Nguồn 1: Học từ các video TikTok Viral Đột Biến (`learned_viral_patterns.json`)
    if os.path.exists(LEARNED_VIRAL_PATTERNS_FILE):
        try:
            with open(LEARNED_VIRAL_PATTERNS_FILE, "r", encoding="utf-8") as f:
                patterns = json.load(f)
            arch_patterns = [p for p in patterns if p.get("product_archetype") == archetype]
            if not arch_patterns and patterns:
                arch_patterns = patterns[-3:]
            if arch_patterns:
                # Ưu tiên video có điểm Đột biến BVI cao nhất
                arch_patterns.sort(
                    key=lambda x: x.get("breakout_metrics", {}).get("bvi_score_100", 50.0),
                    reverse=True
                )
                top_viral = arch_patterns[0]
                p_dna = top_viral.get("layer1_pacing_dna", {})
                v_dna = top_viral.get("layer2_and_3_visual_transitions_dna", {})
                a_dna = top_viral.get("layer5_audio_and_beat_dna", {})

                evolved_state["target_hook_dur_sec"] = round(float(p_dna.get("hook_first_shot_dur_sec", 1.5)), 2)
                evolved_state["target_avg_cut_sec"] = round(float(p_dna.get("avg_shot_dur_sec", 1.85)), 2)
                evolved_state["cuts_in_first_3_sec"] = int(p_dna.get("cuts_in_first_3_sec", 2))
                evolved_state["learned_sources_count"] += len(arch_patterns)

                trans_sig = v_dna.get("transitions_signature", [])
                if trans_sig:
                    evolved_state["recommended_transition"] = " + ".join(trans_sig[:2])

                # Tự động cập nhật Vibe & BGM Mode theo tỷ lệ cắt khớp Beat của xu hướng mới nhất
                beat_ratio = float(a_dna.get("beat_sync_ratio_pct", 0.0))
                if beat_ratio >= 60.0:
                    evolved_state["evolved_recommended_vibe"] = "V4"
                    evolved_state["evolved_bgm_mode"] = "M1_FULL_BEAT_SYNC"
                elif beat_ratio >= 40.0:
                    evolved_state["evolved_bgm_mode"] = "M2_SELECTIVE_HOOK_AND_CTA_SYNC"
        except Exception:
            pass

    # Nguồn 2: Học từ các Dự án Nổ Đơn / Triệu View của chính bạn (`gold_winning_templates.json`)
    if os.path.exists(GOLD_WINNERS_FILE):
        try:
            with open(GOLD_WINNERS_FILE, "r", encoding="utf-8") as f:
                winners = json.load(f)
            arch_winners = [w for w in winners if w.get("product_archetype") == archetype]
            if arch_winners:
                arch_winners.sort(key=lambda x: x.get("gpm_efficiency_index", 0.0), reverse=True)
                best_win = arch_winners[0].get("winning_dna", {})
                evolved_state["target_hook_dur_sec"] = round(
                    (evolved_state["target_hook_dur_sec"] + float(best_win.get("hook_first_clip_dur_sec", 1.5))) / 2.0,
                    2
                )
                evolved_state["target_avg_cut_sec"] = round(
                    (evolved_state["target_avg_cut_sec"] + float(best_win.get("avg_clip_dur_sec", 1.85))) / 2.0,
                    2
                )
                evolved_state["learned_sources_count"] += len(arch_winners)
        except Exception:
            pass

    # Nguồn 3: Học từ Thói quen chỉnh sửa CapCut & Gu cá nhân của bạn (`learned_user_preferences.json`)
    if os.path.exists(user_prefs_file):
        try:
            with open(user_prefs_file, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            clip_delta = float(prefs.get("preferred_clip_duration_delta_sec", 0.0))
            evolved_state["target_avg_cut_sec"] = round(
                max(1.1, min(2.7, evolved_state["target_avg_cut_sec"] + clip_delta)), 2
            )
            evolved_state["user_preferred_subtitle_y"] = float(prefs.get("preferred_subtitle_y", -0.52))
            if prefs.get("preferred_talent_mode"):
                evolved_state["evolved_talent_mode"] = prefs["preferred_talent_mode"]
            if prefs.get("filming_habit_notes"):
                evolved_state["personal_filming_reminders"].extend(prefs["filming_habit_notes"])
        except Exception:
            pass

    # Nguồn 4: Học từ Ký ức Miễn dịch Lỗi (`reflexion_lessons.jsonl`) để cảnh báo trước khi bấm máy
    if os.path.exists(reflexion_file):
        try:
            with open(reflexion_file, "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
            for ln in lines[-5:]:
                lesson = json.loads(ln)
                issue = lesson.get("issue_detected", "")
                fix = lesson.get("preventive_rule_for_next_run", "")
                if issue or fix:
                    evolved_state["personal_filming_reminders"].append(
                        f"[Bài học từ video trước - {lesson.get('stage', 'QA')}]: {issue} -> Khi quay nhớ: {fix}"
                    )
        except Exception:
            pass

    # Lưu lại trạng thái đã tiến hóa của từng ngành hàng
    all_arch_rules: Dict[str, Any] = {}
    if os.path.exists(evolved_rules_file):
        try:
            with open(evolved_rules_file, "r", encoding="utf-8") as f:
                all_arch_rules = json.load(f)
        except Exception:
            all_arch_rules = {}
    all_arch_rules[archetype] = evolved_state
    with open(evolved_rules_file, "w", encoding="utf-8") as f:
        json.dump(all_arch_rules, f, ensure_ascii=False, indent=2)

    return evolved_state


def learn_from_completed_shoot_and_edit(project_slug: str, raw_clips_dir: str) -> Dict[str, Any]:
    """
    HỌC NGƯỢC TỪ THỰC TẾ BẤM MÁY CỦA BẠN SAU MỖI DỰ ÁN:
    Đối chiếu các file video thô bạn vừa quay với Bản Thiết Kế Quay (`shooting_plan.json`)
    để biết:
      - Ánh sáng phòng quay của bạn đang dư hay thiếu sáng?
      - Tiếng ASMR thật bạn thu có bị ồn nền (Noise Floor) không?
      - Bạn thích quay thời lượng mỗi clip dài bao nhiêu giây?
    Tự động cập nhật vào `learned_user_preferences.json` để lần đề xuất quay sau thông minh hơn!
    """
    os.makedirs(BRAIN_DIR, exist_ok=True)
    user_prefs_file = os.path.join(BRAIN_DIR, "learned_user_preferences.json")
    prefs: Dict[str, Any] = {}
    if os.path.exists(user_prefs_file):
        try:
            with open(user_prefs_file, "r", encoding="utf-8") as f:
                prefs = json.load(f)
        except Exception:
            prefs = {}

    notes: List[str] = prefs.get("filming_habit_notes", [])
    if os.path.exists(raw_clips_dir):
        mp4s = [os.path.join(raw_clips_dir, fn) for fn in os.listdir(raw_clips_dir) if fn.endswith((".mp4", ".mov", ".MP4", ".MOV"))]
        if mp4s:
            sample_clip = mp4s[0]
            cmd = [
                "ffmpeg", "-hide_banner", "-t", "3", "-i", sample_clip,
                "-vf", "signalstats,metadata=print:file=-", "-f", "null", "-"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            y_vals = [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", res.stdout)]
            avg_y = sum(y_vals) / max(1, len(y_vals)) if y_vals else 130.0
            if avg_y < 105.0:
                msg = f"Góc quay quen thuộc của bạn hơi thiếu sáng (YAVG={avg_y:.1f} < 110). Lần tới hãy bật thêm 1 đèn phụ chếch 45 độ trước khi bấm máy!"
                if msg not in notes:
                    notes.append(msg)

    prefs["filming_habit_notes"] = notes[-5:]
    prefs["last_shoot_feedback_project"] = project_slug
    with open(user_prefs_file, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)

    print(f"[SHOOTING BRAIN EVOLVED] Đã học xong thói quen bấm máy thực tế từ dự án '{project_slug}'!")
    return prefs


# ==============================================================================
# 3. BỘ CÂU HỎI TƯƠNG TÁC ĐỂ BẠN CHỐT PHONG CÁCH TRƯỚC KHI QUAY
# ==============================================================================

def generate_pre_shoot_questions(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sinh ra 3 câu hỏi ngắn gọn kèm phương án (Khuyên dùng) dựa trên kết quả đọc ảnh sản phẩm
    và dữ liệu Auto-Update mới nhất từ Bộ Nhớ Tự Học!
    """
    rec_vibe = profile.get("recommended_vibe", "V1")
    vibe_options = [
        {
            "code": "V1",
            "label": "KOC Trải Nghiệm Đời Thường & Giải Quyết Nỗi Đau (Chuẩn Mẹ Shin Thúi Nè - Khen 8 Chê 2, Tỷ lệ chốt đơn GPM cao nhất)"
        },
        {
            "code": "V2",
            "label": "Sang Trọng, Tinh Tế & Chữa Lành (Luxury Aesthetic & Pure ASMR - Tôn chất liệu, ánh sáng ấm, ít lời)"
        },
        {
            "code": "V3",
            "label": "Thử Thách Thực Chiến & So Sánh Trực Diện (Torture Test / Before-After One-Take ngay từ giây đầu)"
        },
        {
            "code": "V4",
            "label": "Đập Hộp Nhịp Nhanh Bắt Trend (Fast-Paced Beat-Sync Unboxing - Cắt cảnh dồn dập khớp phách nhạc)"
        }
    ]
    # Đưa phương án khuyên dùng lên đầu
    vibe_options.sort(key=lambda x: 0 if x["code"] == rec_vibe else 1)
    vibe_options[0]["label"] = f"(Khuyên dùng cho sản phẩm này) {vibe_options[0]['label']}"

    questions_payload = {
        "product_summary": f"[{profile['detected_archetype']} - {profile['archetype_name']}] {profile['product_description']}",
        "optical_note": profile["image_optical_analysis"]["lighting_advice"],
        "chr_pre_warning": profile["chr_forbidden_scenes"],
        "questions_for_user": [
            {
                "id": "Q1_VIDEO_VIBE",
                "question": "Câu 1: Bạn muốn quay video sản phẩm này theo Phong Cách (Vibe) chủ đạo nào?",
                "options": [f"{o['code']}: {o['label']}" for o in vibe_options]
            },
            {
                "id": "Q2_TALENT_AND_VOICE",
                "question": "Câu 2: Bạn muốn xuất hiện và thu âm theo hình thức nào trong buổi quay này?",
                "options": [
                    "T1: (Khuyên dùng) Lộ mặt nói trực tiếp ở cảnh đầu/cuối + Quay cận cảnh 2 bàn tay thao tác ở cảnh giữa + Thu tiếng ASMR thật",
                    "T2: Không lộ mặt (Chỉ quay góc nhìn thứ nhất POV 2 bàn tay thao tác sản phẩm) + Thu tiếng động ASMR thật lúc quay, lồng tiếng đọc (Voiceover) sau",
                    "T3: Quay hình hoàn toàn im lặng nhanh gọn, sau đó giao cho Bộ Edit tự ghép Voiceover và hiệu ứng SFX"
                ]
            },
            {
                "id": "Q3_ENVIRONMENT_AND_PROPS",
                "question": "Câu 3: Bạn đang có sẵn bối cảnh và đạo cụ đối chứng nào để mình lên danh sách cảnh quay sát thực tế nhất?",
                "options": [
                    "B1: (Khuyên dùng) Có sẵn vật đối chứng / mẫu cũ / vết bẩn thật để quay cảnh So sánh Trước - Sau (Before/After)",
                    "B2: Chỉ có sản phẩm mới trên bàn làm việc / bàn trang điểm / góc phòng sạch đẹp",
                    "B3: Quay trực tiếp tại khu vực sử dụng thực tế (Nhà bếp / Phòng tắm / Ngoài trời)"
                ]
            }
        ]
    }
    return questions_payload


# ==============================================================================
# 4. XUẤT BẢN THIẾT KẾ 6 CẢNH QUAY KHỚP 100% VỚI BỘ EDIT TỰ ĐỘNG (EDIT-READY BLUEPRINT)
# ==============================================================================

def generate_edit_ready_shooting_blueprint(
    profile: Dict[str, Any],
    vibe_code: str = "V1",
    talent_code: str = "T1",
    props_code: str = "B1",
    project_slug: str = "du_an_moi"
) -> Dict[str, Any]:
    """
    Tạo ra:
    1. Danh sách 6 Clip cần bấm máy (Shot-by-Shot Resource Checklist) được tối ưu hóa riêng cho
       các thuật toán trong `smart_raw_miner.py` và `capcut_master_injector.py`.
    2. Gợi ý lời thoại (Voiceover Script 28s) theo công thức Hook 1.5s -> Demo -> Khen 8 Chê 2 -> Seamless Loop CTA.
    3. File JSON khóa đồng bộ `./workspace/shooting_blueprints/<project_slug>_shooting_plan.json`.
    """
    os.makedirs(BLUEPRINT_DIR, exist_ok=True)
    arch = profile["detected_archetype"]
    trend = profile["viral_trend_hint"]
    honest_con = profile["honest_con_suggestions"][0]

    is_pov_only = (talent_code == "T2")
    angle_talking = "A6 (Góc POV mắt người dùng nhìn xuống 2 bàn tay cầm sản phẩm)" if is_pov_only else "A1 (Góc 45 độ ngang ngực KOC cầm sản phẩm)"

    shots_blueprint: List[Dict[str, Any]] = [
        {
            "clip_slot_id": "RAW_01_HOOK",
            "order": 1,
            "scene_name": "CẢNH 1: MÓC CÂU THỊ GIÁC & KẾT QUẢ TRƯỚC (VISUAL HOOK)",
            "timeline_window_sec": f"0.0s -> {trend['target_hook_dur_sec']}s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 4 - 5 giây (AI sẽ tự cắt lấy 1.5s có chuyển động đắt giá nhất)",
            "camera_angle_code": "A2 (Macro Cận Cảnh 15-20cm)" if vibe_code != "V3" else "A7 (Cận Cảnh Kết Quả Thực Chiến)",
            "action_to_perform": (
                f"Thực hiện ngay hành động đắt giá nhất của sản phẩm: {profile['visual_aha_hook']}. "
                "LƯU Ý QUAN TRỌNG: Bắt đầu bấm máy trước 1 giây rồi mới đưa tay chuyển động dứt khoát vào giữa khung hình!"
            ),
            "why_edit_engine_needs_this": (
                "Giúp thuật toán `trim_clip_on_action_and_motion()` bắt đúng đỉnh vận tốc chuyển động tay (`Cutting on Action`) "
                "và giúp `detect_kinetic_movement_sfx_triggers()` tự động chèn tiếng `Whoosh + Shimmer` ở 0.2s đầu!"
            ),
            "framing_and_text_safe_zone": (
                "Giữ sản phẩm nằm gọn ở vùng Trung Tâm (từ 35% đến 65% chiều dọc màn hình). "
                "Chừa trống 1/3 phía trên để Mắt xích 5 đặt Banner Hook và 1/3 phía dưới để đặt Phụ đề không đè lên sản phẩm!"
            ),
            "suggested_voice_line": "Khoan lướt qua nếu mọi người vẫn đang đau đầu tìm một món vừa chuẩn vừa đáng tiền như thế này nhé..."
        },
        {
            "clip_slot_id": "RAW_02_PAIN_CONTEXT",
            "order": 2,
            "scene_name": "CẢNH 2: NỖI ĐAU THỰC TẾ / LÝ DO MUA HÀNG (EMPATHY & CONTEXT)",
            "timeline_window_sec": f"{trend['target_hook_dur_sec']}s -> 6.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 6 - 8 giây (AI sẽ lọc lấy 4.0s)",
            "camera_angle_code": angle_talking,
            "action_to_perform": (
                "Nếu có mẫu cũ/vết bẩn (B1): Đưa mẫu cũ bất tiện lên trước ống kính, lắc đầu nhẹ rồi đẩy mẫu cũ ra ngoài, "
                "đưa sản phẩm mới từ cạnh phải vào chính giữa. Nếu chỉ có sản phẩm mới (B2): Xoay nhẹ sản phẩm từ mặt bên sang mặt chính diện."
            ),
            "why_edit_engine_needs_this": (
                "Tạo vector dịch chuyển ngang (`Horizontal Motion`) để Bộ Edit tự động áp dụng `Punch-In Jump Cut (1.0x -> 1.15x)` "
                "kèm hiệu ứng âm thanh `Swipe Whoosh` lôi cuốn mắt người xem."
            ),
            "framing_and_text_safe_zone": "Đặt chủ thể cao hơn đáy màn hình ít nhất 30% để né vùng Phụ đề (`y = -0.52`).",
            "suggested_voice_line": "Trước giờ dùng mấy loại cũ cứ bị bất tiện mãi, cho đến khi mình đổi sang em này thì đúng là chân ái."
        },
        {
            "clip_slot_id": "RAW_03_NATIVE_ASMR_UNBOX",
            "order": 3,
            "scene_name": "CẢNH 3: ĐẬP HỘP & THU ÂM THANH ASMR THẬT (TIER-1 NATIVE ASMR)",
            "timeline_window_sec": "6.0s -> 11.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 7 - 10 giây (AI sẽ lọc lấy 5.0s)",
            "camera_angle_code": "A4 (Top-Down 90 độ từ trên xuống bàn) hoặc A2 (Macro nghiêng 30 độ)",
            "action_to_perform": (
                f"Đưa sản phẩm lại gần mic điện thoại khoảng 15cm. Thực hiện: {profile['native_asmr_trigger']}. "
                "⚠️ BẮT BUỘC: Trong 2.5 giây lúc phát ra tiếng động từ sản phẩm, bạn hãy NGỪNG NÓI HOÀN TOÀN và tắt quạt máy trong phòng!"
            ),
            "why_edit_engine_needs_this": (
                "Để hàm `evaluate_and_route_clip_audio()` đo được độ nảy âm thanh `Crest Factor >= 11dB` mà không bị dính giọng nói, "
                "từ đó tự động kích hoạt `CHẾ ĐỘ 1: GIỮ 100% TIẾNG ASMR THẬT CỦA SẢN PHẨM`!"
            ),
            "framing_and_text_safe_zone": profile["image_optical_analysis"]["lighting_advice"],
            "suggested_voice_line": "(Im lặng 2 giây đầu để thu tiếng ASMR thật)... Nghe cái tiếng với nhìn chất hoàn thiện thôi là biết hàng xịn rồi."
        },
        {
            "clip_slot_id": "RAW_04_ONETAKE_PROOF",
            "order": 4,
            "scene_name": "CẢNH 4: TEST CÔNG DỤNG THỰC TẾ LIỀN MẠCH (ONE-TAKE PROOF DEMO)",
            "timeline_window_sec": "11.0s -> 19.0s",
            "recommended_record_duration_sec": "Bấm máy quay LIỀN MẠCH 10 - 15 giây KHÔNG TẮT MÁY GIỮA CHỪNG",
            "camera_angle_code": "A3 (Góc cố định One-Take chứng minh hiệu quả thật)",
            "action_to_perform": (
                "Quay liên tục từ lúc bắt đầu thao tác thử nghiệm sản phẩm cho đến khi hiện rõ kết quả cuối cùng trong cùng 1 cú bấm máy. "
                "Không bấm dừng máy ở giữa!"
            ),
            "why_edit_engine_needs_this": (
                "Bảo vệ kênh tuyệt đối khỏi lỗi `CHR -10đ đến -20đ (Cắt ghép kết quả giả)`. "
                "Đoạn thao tác chờ ở giữa sẽ được Bộ Edit tự động kích hoạt `Speed Ramp (Tua nhanh 2.5x)` kèm hiệu ứng `Fast Whoosh` để video không bị dài dòng!"
            ),
            "framing_and_text_safe_zone": "Giữ nguyên vị trí máy quay cố định để AI có thể tạo thêm cảnh Split-Screen Trước/Sau nếu cần.",
            "suggested_voice_line": "Mình test trực tiếp luôn không cắt ghép cho mọi người kiểm chứng nhé, hiệu quả nhìn thấy rõ ngay trước mắt luôn."
        },
        {
            "clip_slot_id": "RAW_05_HONEST_CON_PIVOT",
            "order": 5,
            "scene_name": "CẢNH 5: ĐIỂM TRỪ NHẸ HỢP LÝ — CÔNG THỨC KHEN 8 CHÊ 2 (TRUST PIVOT)",
            "timeline_window_sec": "19.0s -> 23.5s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 5 - 6 giây (AI lọc lấy 4.5s)",
            "camera_angle_code": "A2 (Chỉ ngón tay vào chi tiết nhỏ trên sản phẩm) hoặc " + angle_talking,
            "action_to_perform": (
                "Dùng ngón trỏ chỉ nhẹ vào chi tiết bạn định nhận xét khách quan. "
                f"Gợi ý điểm chê khéo cho sản phẩm này: \"{honest_con}\"."
            ),
            "why_edit_engine_needs_this": (
                "Giúp Mắt xích 2 & 4 đặt đúng điểm ngoặt tâm lý `Pivot Khen - Chê` tại giây thứ 19, "
                "tự động chèn tiếng `Pop / Bubble` và đổi màu chữ nhấn sang Vàng Champagne (`#FFD166`) tăng 300% độ tin cậy!"
            ),
            "framing_and_text_safe_zone": "Chừa trống vùng dưới màn hình cho phụ đề nhấn màu.",
            "suggested_voice_line": f"À nhưng có 1 điểm trừ nhỏ mình phải nói thật là: {honest_con}."
        },
        {
            "clip_slot_id": "RAW_06_SEAMLESS_LOOP_CTA",
            "order": 6,
            "scene_name": "CẢNH 6: KẾT QUẢ CUỐI & CHỈ TAY GIỎ HÀNG VÒNG LẶP (LOOP CTA)",
            "timeline_window_sec": "23.5s -> 28.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 5 - 6 giây (AI lọc lấy 4.5s)",
            "camera_angle_code": angle_talking,
            "action_to_perform": (
                "Tay phải cầm sản phẩm ngang ngực, TAY TRÁI CHỈ DỨT KHOÁT XUỐNG GÓC DƯỚI BÊN TRÁI MÀN HÌNH "
                "(đúng vị trí gắn Thẻ Giỏ Hàng Vàng TikTok Shop) trong 2 giây cuối cùng."
            ),
            "why_edit_engine_needs_this": (
                "Kích hoạt bộ nhận diện cử chỉ `CTA_POINT` để tự động gắn tiếng `Mouse Click + Bell Ding`, "
                "đặt Sticker Mũi Tên Chỉ Giỏ Hàng và cắt sát đuôi `0.02s` tạo vòng lặp `Seamless Loop` sang Cảnh 1!"
            ),
            "framing_and_text_safe_zone": "TUYỆT ĐỐI KHÔNG để sản phẩm hay bàn tay che mất góc trái dưới màn hình (`y < -0.60, x < -0.35`).",
            "suggested_voice_line": "Đợt này ở giỏ hàng góc trái đang có deal hời lắm, mọi người bấm vào xem thử trước khi hết khuyến mãi, bởi vì..."
        }
    ]

    proj_dirs = setup_and_ingest_project_photos(project_slug, profile.get("image_optical_analysis", {}).get("valid_images", []))

    blueprint_data = {
        "project_slug": project_slug,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "project_isolated_workspace": proj_dirs,
        "product_profile": profile,
        "selected_style": {
            "vibe_code": vibe_code,
            "talent_code": talent_code,
            "props_code": props_code,
            "bgm_mode_locked_for_editor": profile["default_bgm_mode"] if vibe_code != "V4" else "M1_FULL_BEAT_SYNC"
        },
        "chr_forbidden_scenes_checklist": profile["chr_forbidden_scenes"],
        "shots_to_film": shots_blueprint
    }

    json_path = os.path.join(BLUEPRINT_DIR, f"{project_slug}_shooting_plan.json")
    proj_bp_path = os.path.join(proj_dirs["isolated_blueprint_dir"], f"{project_slug}_shooting_plan.json")
    for p_out in (json_path, proj_bp_path):
        with open(p_out, "w", encoding="utf-8") as f:
            json.dump(blueprint_data, f, ensure_ascii=False, indent=2)

    print(f"[SHOOTING BLUEPRINT READY] Đã xuất Bản Thiết Kế 6 Cảnh Quay Chuẩn Bộ Edit tại: {proj_bp_path}")
    print(f"[AUTO-ISOLATED FOLDER] Thư mục lưu video riêng của dự án (Không bao giờ mất file CapCut): {proj_dirs['isolated_videos_dir']}")
    return blueprint_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Node 0: Pre-Production AI Director & Smart Shooting Planner")
    parser.add_argument("--images", type=str, default="", help="Đường dẫn ảnh chụp sản phẩm (cách nhau dấu phẩy, hoặc tự động lấy từ ./raw_photos/)")
    parser.add_argument("--description", type=str, required=True, help="Mô tả sản phẩm, công dụng, giá bán")
    parser.add_argument("--archetype", type=str, default=None, help="Mã ngành hàng P1-P7 (tự động nhận diện nếu bỏ trống)")
    parser.add_argument("--ask-questions", action="store_true", help="Chỉ phân tích ảnh & sinh 3 câu hỏi chọn phong cách trước khi lên kịch bản")
    parser.add_argument("--vibe", type=str, default="V1", help="Phong cách video: V1 (KOC Đời thường), V2 (Sang trọng ASMR), V3 (Test thực chiến), V4 (Beat-Sync)")
    parser.add_argument("--talent", type=str, default="T1", help="Cách lên hình: T1 (Lộ mặt + POV), T2 (Chỉ quay tay POV + ASMR), T3 (Im lặng lồng tiếng sau)")
    parser.add_argument("--props", type=str, default="B1", help="Bối cảnh: B1 (Có mẫu cũ/vết bẩn so sánh), B2 (Bàn sạch), B3 (Tại nơi sử dụng)")
    parser.add_argument("--project-slug", type=str, default="du_an_quay_moi", help="Tên định danh dự án để tự động gom ảnh/video vào ./projects/<project-slug>/")
    args = parser.parse_args()

    raw_img_list = [x.strip() for x in args.images.split(",") if x.strip()]
    workspace_info = setup_and_ingest_project_photos(args.project_slug, raw_img_list)
    prof = analyze_product_photos_and_description(workspace_info["project_photos"], args.description, args.archetype)
    prof["project_isolated_workspace"] = workspace_info

    if args.ask_questions:
        q_out = generate_pre_shoot_questions(prof)
        q_out["project_isolated_workspace"] = workspace_info
        print(json.dumps(q_out, ensure_ascii=False, indent=2))
    else:
        bp = generate_edit_ready_shooting_blueprint(
            prof,
            vibe_code=args.vibe,
            talent_code=args.talent,
            props_code=args.props,
            project_slug=args.project_slug
        )
        print(json.dumps(bp, ensure_ascii=False, indent=2))
