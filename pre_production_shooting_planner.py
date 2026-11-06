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
        "keywords": ["kem", "serum", "sữa rửa mặt", "toner", "chống nắng", "son", "phấn", "cushion", "dầu gội", "tẩy trang", "mặt nạ", "skincare", "dưỡng ẩm", "mụn", "trắng da", "lược", "tóc", "nước hoa", "body mist", "xịt thơm", "sữa tắm", "gương", "máy uốn tóc"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cận cảnh Macro 15cm giọt serum chảy trên da / bóp tràn tinh chất mặt nạ (@3thag8_) hoặc đầu ngón tay tán chất kem tan mướt dưới ánh sáng tạt 45 độ",
        "native_asmr_trigger": "Tiếng bóp vòi pump 'xịt/tạch', tiếng xoáy nắp lọ thủy tinh, tiếng vỗ nhẹ chất kem lên mu bàn tay, tiếng răng lược chải tóc",
        "invisible_to_visible_physics_props": [
            "Đạo cụ vật lý chứng minh chất kem/dưỡng chất (@3thag8_): Bóp mạnh túi mặt nạ cho tinh chất tràn ngập lòng bàn tay hoặc nhỏ giọt serum trượt dọc cổ tay dưới đèn tạt 45 độ.",
            "Nếu là Bàn chải / Chăm sóc răng miệng (@grayunbox 2.8M views): Dùng 'Đạo cụ Thế thân Sạch' — chải trực tiếp vào rãnh xoắn bên trong nắp tuýp kem đánh răng & kẽ khớp ngón tay để chứng minh sợi lông siêu mảnh luồn sâu mà không cần quay trong miệng!",
            "Nếu là Mặt nạ mắt / Miếng chườm mắt (@grayunbox): Dùng Gấu Bông / Thú bông làm mẫu thử (Plushie Proxy) khi quay POV không lộ mặt.",
            "Nếu là Nước hoa / Body Mist (@grayunbox): Xịt sương trực tiếp lên cổ tay áo khoác Denim đen để tia sương trắng nổi bật + Phẩy tay quạt hương để AI thả hạt lá 🍃 bay.",
            "Nếu là Xà phòng / Kem dưỡng da (@grayunbox): Quay thêm 3 giây giơ cánh tay dưới ánh nắng ngoài trời thật (Cam thường không filter) để AI ghép cửa sổ PIP chứng minh chất da thật."
        ],
        "wardrobe_and_lighting_setup": (
            "Gợi ý phục trang & ánh sáng tôn sản phẩm: Mặc áo len dệt kim tay dài màu Nâu Espresso / Đen (@byraanni) hoặc đặt đèn bàn ánh vàng ấm "
            "rọi từ đỉnh đầu xuống mặt bàn tối (@honghanhxinhgai_01) để làm nổi bật chất kem trắng/trong suốt gấp 3 lần!"
        ),
        "honest_con_suggestions": [
            "Mùi thảo mộc tự nhiên lúc mới mở nắp hơi rõ trong 3 giây đầu (do không dùng hương liệu nhân tạo), nhưng thoa lên 10 giây là bay hết",
            "Vỏ lọ làm dày dặn cầm hơi đầm tay khi mang đi du lịch, bù lại rơi không sợ vỡ",
            "Chất kem đặc nên chỉ cần lấy bằng hạt đậu là đủ, lấy nhiều quá sẽ lâu thấm hơn"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG quay cảnh so sánh làn da đã qua chỉnh sửa filter làm mịn với làn da mộc.",
            "❌ KHÔNG nói các từ y khoa tuyệt đối khi thu âm: 'trị dứt điểm mụn/nám 100%', 'thần dược', 'trắng bật 5 tông tức thì'.",
            "✅ Hệ thống sẽ tự động gắn nhãn bảo vệ CHR '*hiệu quả sản phẩm tuỳ vào cơ địa mỗi người*' và chấm tách OCR ('m.ụn', 'tr.ắng da') theo chuẩn @3thag8_."
        ],
        "default_bgm_mode": "M3_AESTHETIC_CHILL_SYNTH"
    },
    "P2": {
        "name": "Đồ Gia Dụng Thông Minh, Nhà Bếp, Bình Ly & Vệ Sinh",
        "keywords": ["máy xay", "nồi", "chảo", "cây lau", "bình giữ nhiệt", "ly giữ nhiệt", "cốc", "máy hút bụi", "kệ", "tẩy", "rửa", "gia dụng", "bếp", "hộp đựng", "dao", "kéo", "khăn giấy"],
        "recommended_vibe": "V2",
        "visual_aha_hook": "Tổ hợp 3 Cảnh Collage 3.3s (@byraanni: Cầm ly uống thực tế 1.1s -> Flatlay 90 độ trên khay 1.1s -> Mở giấy nến 1.1s) hoặc Test thực chiến One-Take",
        "native_asmr_trigger": "Tiếng đá viên 'lách cách' rơi vào bình inox, tiếng bật nắp bật 'tạch' 1 chạm, tiếng gõ móng tay lên thân inox 304 dày dặn",
        "invisible_to_visible_physics_props": [
            "Nếu là Bình/Ly giữ nhiệt (@byraanni): Pha Matcha Latte xanh mướt hoặc Cà phê đá có màu tương phản mạnh với thành cốc + Dốc ngược 180 độ lắc mạnh 3 cái trước ống kính để chứng minh ron cao su kín nước 100%!",
            "Nếu là Sáp thơm / Nhang trầm / Tinh dầu (@grayunbox 2.8M views): Bóc lớp màng seal bạc sát mic thu ASMR + Dùng đầu tăm gỗ chọc nhẹ vào bề mặt thạch sáp (Toothpick Jelly-Poke) chứng minh độ núng nính đàn hồi!",
            "Nếu là Kệ / Tủ / Hộp đựng nhiều ngăn cần lắp ráp (@grayunbox): Quay cảnh Kệ Đã Lắp Hoàn Chỉnh xếp đầy đồ đẹp mắt ở 2 giây đầu tiên (Finished-First Hook), sau đó mới quay cảnh tháo lắp và ấn trượt bánh xe 360 độ!",
            "Nếu là Khăn giấy/Khăn lau (@3thag8_): Nhúng đẫm tờ khăn giấy vào cốc nước trong suốt rồi dùng 2 tay kéo căng hết cỡ để chứng minh độ dai không mủn rách!"
        ],
        "wardrobe_and_lighting_setup": (
            "Bối cảnh chuẩn Tạp chí Kinfolk (@byraanni): Mặt bàn tròn trắng mờ (YAVG ~155) cạnh rèm voan cửa sổ + "
            "Mặc áo cardigan len gân màu Nâu Espresso kéo trễ ngang lòng bàn tay để tạo tương phản thị giác sang trọng."
        ),
        "honest_con_suggestions": [
            "Dây điện đi kèm hơi ngắn (khoảng 80cm) nên phải đặt gần ổ cắm, bù lại công suất máy rất khỏe",
            "Ron cao su chống tràn làm cực khít nên lúc mới mua mở nắp cần hơi dùng lực nhẹ, bù lại bỏ cốp xe lắc cỡ nào cũng không rỉ 1 giọt nước",
            "Lưỡi dao/bề mặt rất sắc bén nên lúc tháo ra vệ sinh mọi người nhớ cẩn thận tay"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG cắt ghép ngắt cảnh giữa lúc 'Đang bẩn' và 'Đã sạch' (Dễ bị AI TikTok phạt -10đ lỗi Phóng đại hiệu quả). Bắt buộc quay liền mạch One-Take!",
            "❌ KHÔNG để vật sắc nhọn (dao/kéo) chĩa thẳng vào ống kính ở 3 giây đầu mà không có ngữ cảnh nấu ăn."
        ],
        "default_bgm_mode": "M2_SELECTIVE_HOOK_AND_CTA_SYNC"
    },
    "P3": {
        "name": "Thời Trang, Phụ Kiện, Giày Dép, Túi Xách & Trang Sức",
        "keywords": ["áo", "quần", "váy", "đầm", "túi", "giày", "dép", "kính", "mũ", "thắt lưng", "vớ", "tất", "khoác", "form", "cardigan", "búp bê", "hoodie", "sweater", "dây chuyền", "nhẫn", "vòng tay", "khuyên tai", "bạc", "kẹp tóc"],
        "recommended_vibe": "V2",
        "visual_aha_hook": "Cảnh xỏ giày/khoác túi bước đi thực tế 1.1s nối mượt sang cảnh mở hộp giấy gói chỉn chu (@byraanni) hoặc kéo giãn chất vải hết cỡ",
        "native_asmr_trigger": "Tiếng mở giấy gói sột soạt êm tai, tiếng khóa kéo kim loại mượt mà, tiếng gõ nhẹ đế giày/móc khóa kim loại",
        "invisible_to_visible_physics_props": [
            "Nếu là Túi xách / Ví (@byraanni): Xếp sẵn Điện thoại + Son + Phấn nước + Ví nhỏ trên mặt bàn rồi bỏ từng món vào túi để chứng minh sức chứa thực tế (Capacity Test).",
            "Nếu là Giày dép (@byraanni): Quay cảnh 2 bàn tay bẻ cong đế giày 90 độ chứng minh đế êm mềm + Cảnh mang tất trắng xỏ giày bước đi dưới nắng tự nhiên.",
            "Nếu là Quần áo: Luồn đèn Flash điện thoại vào mặt trong vải để chứng minh vải dệt dày dặn không bị lộ."
        ],
        "wardrobe_and_lighting_setup": (
            "Phối sẵn 1 bộ trang phục đồng tông Pastel/Kem/Nâu Espresso (Color-coordinated outfit) khớp với màu phụ kiện để lên hình chuẩn Lookbook Pinterest."
        ),
        "honest_con_suggestions": [
            "Lúc mới mở túi vẫn còn 1-2 sợi chỉ thừa nhỏ ở mặt trong đường vắt sổ, cắt nhẹ là đẹp",
            "Form may chuẩn nên ai thích mặc rộng thoải mái hoặc bàn chân dày thì nên nhích lên 1 size nhé",
            "Màu ngoài đời trầm hơn ảnh hãng chụp studio khoảng 5% nhưng nhìn thực tế lại sang và tây hơn"
        ],
        "chr_forbidden_scenes": [
            "❌ TUYỆT ĐỐI KHÔNG để lộ logo các thương hiệu xa xỉ lớn (Gucci, Chanel, LV, Nike...) trên nền hoặc trên sản phẩm nếu không có giấy ủy quyền (-40đ CHR).",
            "❌ KHÔNG quay góc máy quá nhạy cảm khi thử đồ (tránh lỗi Hở hang -20đ CHR)."
        ],
        "default_bgm_mode": "M1_FULL_BEAT_SYNC"
    },
    "P4": {
        "name": "Mẹ & Bé, Đồ Chơi, Văn Phòng Phẩm & Góc Học Tập",
        "keywords": ["bé", "bỉm", "tã", "sữa", "bình sữa", "đồ chơi", "khăn ướt", "ăn dặm", "mẹ bầu", "trẻ em", "gặm nướu", "xe đẩy", "sổ", "sổ tay", "bút", "hộp bút", "bóp viết", "sticker", "giấy note", "văn phòng phẩm", "planner"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cảnh test độ an toàn/mềm mại trực tiếp trên tay mẹ (đổ nước màu xanh thử độ thấm hút của bỉm hoặc bóp thử độ mềm không góc cạnh của đồ chơi)",
        "native_asmr_trigger": "Tiếng bóp đồ chơi/nhựa silicone đàn hồi, tiếng xé miếng dán êm ái, tiếng lắc nhẹ",
        "invisible_to_visible_physics_props": [
            "Chuẩn bị cốc nước ấm / giấy khô để áp lên bề mặt bỉm sau 15 giây chứng minh khô thoáng 100%.",
            "Quay cận cảnh ngón tay miết mạnh quanh viền nhựa chứng minh hoàn thiện bo tròn không có nhựa thừa (ba-via) làm xước tay bé."
        ],
        "wardrobe_and_lighting_setup": "Ánh sáng phòng ấm áp tự nhiên (Chuẩn @meshinthuine), góc máy sạch gọn tạo cảm giác tin cậy của người mẹ.",
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
        "keywords": ["bánh", "kẹo", "trà", "cà phê", "khô gà", "khô bò", "hạt", "sốt", "mì", "ăn vặt", "ngũ cốc", "socola", "mật ong", "matcha"],
        "recommended_vibe": "V1",
        "visual_aha_hook": "Cận cảnh bẻ đôi chiếc bánh/miếng thịt thấy rõ nhân chảy hoặc thớ sợi bên trong kèm biểu cảm cắn miếng đầu tiên",
        "native_asmr_trigger": "Tiếng nhai giòn rụm 'rộp rộp' sát mic 15cm, tiếng bật nắp lon 'xì', tiếng rót đá lạnh lách cách",
        "invisible_to_visible_physics_props": [
            "Đặt sản phẩm trên đĩa gốm trắng hoặc khay gỗ cùng ly đá trong suốt để màu sắc món ăn bật lên rõ nhất.",
            "Quay cận cảnh 15cm lúc xé vỏ hoặc bẻ đôi để thu trọn âm thanh giòn/dẻo tự nhiên."
        ],
        "wardrobe_and_lighting_setup": "Ánh sáng ấm 4500K tôn màu vàng/đỏ của thực phẩm, tuyệt đối tránh đèn huỳnh quang xanh lạnh làm đồ ăn nhìn kém ngon.",
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
        "name": "Phụ Kiện Công Nghệ, Điện Tử, Quạt Mini, Máy Ảnh & Thiết Bị Số",
        "keywords": ["tai nghe", "loa", "sạc", "cáp", "ốp lưng", "đèn", "chuột", "bàn phím", "giá đỡ", "gimbal", "mic", "pin dự phòng", "quạt", "máy ảnh", "digicam"],
        "recommended_vibe": "V2",
        "visual_aha_hook": "Cảnh biến lực vô hình thành hữu hình (@byraanni & @3thag8_): Thổi bay dải giấy ăn/khói nến bằng quạt mini, thả tai nghe vào cốc nước test chống nước, hoặc tự chụp qua gương cổ điển",
        "native_asmr_trigger": "Tiếng nút bấm cơ học 4 cấp độ 'tạch tạch', tiếng nắp hộp tai nghe đóng 'tách' nam châm, tiếng màn trập máy ảnh",
        "invisible_to_visible_physics_props": [
            "Nếu là Quạt cầm tay / Máy sấy (@byraanni): Chuẩn bị 1 tờ giấy ăn mỏng / bông gòn hoặc 1 cây nến vừa thổi tắt có khói trắng để quay cảnh gió quạt thổi bay tung khói/giấy (Biến gió vô hình thành hình ảnh mãn nhãn!).",
            "Nếu là Tai nghe / Đồng hồ chống nước (@3thag8_): Chuẩn bị 1 cốc thủy tinh nước trong suốt, thả trực tiếp tai nghe vào nước 3 giây rồi vớt lên lau khô kết nối Bluetooth ngay trong 1 cú máy One-Take!",
            "Nếu là Máy ảnh / Đèn / Điện thoại (@byraanni): Đặt 1 chiếc gương để bàn viền cổ điển đối diện để quay cảnh tự chụp qua gương + Giữ máy đứng yên 2.5s ở cảnh soi nút bấm/cổng sạc để AI tạo Kính Lúp Tròn Nét Đứt phóng đại 162%!"
        ],
        "wardrobe_and_lighting_setup": (
            "Setup Studio Pegboard 2 nhiệt độ màu (@3thag8_: đèn vàng ấm hắt bảng lỗ phía sau + đèn trắng rọi bàn) hoặc Bàn trắng mờ + Áo len Nâu Espresso (@byraanni)."
        ),
        "honest_con_suggestions": [
            "Chất liệu vỏ nhám mờ nhìn rất sang nhưng nếu tay ra mồ hôi dầu sẽ hơi lưu dấu nhẹ, lau qua là sạch",
            "Ở mức công suất mạnh nhất (mức 4) tiếng gió sẽ hơi nghe rõ một xíu nếu ngồi trong phòng kín yên tĩnh, nhưng ra ngoài trời thì mát cực kỳ"
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
        "visual_aha_hook": "Cận cảnh viên uống/gói bột hòa tan trong cốc nước trong suốt kết hợp quay rõ tem nhãn chính hãng (Giữ yên 2.5s để AI tạo Keyframe Zoom-Hold 1.5s đọc chữ @kieneditcuong)",
        "native_asmr_trigger": "Tiếng mở nắp lọ bảo hiểm, tiếng khuấy thìa vào ly thủy tinh",
        "invisible_to_visible_physics_props": [
            "Chuẩn bị 1 ly thủy tinh trong suốt và thìa inox dài để quay cảnh hòa tan hoặc soi rõ màu sắc viên uống dưới ánh nắng."
        ],
        "wardrobe_and_lighting_setup": "Ánh sáng tự nhiên trong trẻo, giữ lọ sản phẩm đứng yên 2 giây trước ống kính để bộ Edit kích hoạt 4-Keyframe Zoom-Hold đọc bảng thành phần.",
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
    smart_context_strategy = select_smart_contextual_shooting_strategy(description, detected_arch, img_metrics)

    return {
        "product_description": description,
        "detected_archetype": detected_arch,
        "archetype_name": arch_rules["name"],
        "image_optical_analysis": img_metrics,
        "smart_contextual_strategy": smart_context_strategy,
        "visual_aha_hook": smart_context_strategy.get("bespoke_visual_hook") or viral_trend_hint.get("evolved_visual_hook", arch_rules["visual_aha_hook"]),
        "native_asmr_trigger": smart_context_strategy.get("bespoke_asmr_trigger") or arch_rules["native_asmr_trigger"],
        "invisible_to_visible_physics_props": smart_context_strategy.get("tailored_physics_props") or arch_rules.get("invisible_to_visible_physics_props", []),
        "wardrobe_and_lighting_setup": smart_context_strategy.get("tailored_lighting_and_wardrobe") or arch_rules.get("wardrobe_and_lighting_setup", ""),
        "honest_con_suggestions": arch_rules["honest_con_suggestions"],
        "chr_forbidden_scenes": arch_rules["chr_forbidden_scenes"],
        "recommended_vibe": smart_context_strategy.get("recommended_vibe_code", "V0"),
        "recommended_talent_mode": viral_trend_hint.get("evolved_talent_mode", "T1"),
        "default_bgm_mode": viral_trend_hint.get("evolved_bgm_mode", arch_rules["default_bgm_mode"]),
        "viral_trend_hint": viral_trend_hint
    }


def select_smart_contextual_shooting_strategy(
    description: str,
    archetype: str,
    img_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    [BỘ NÃO TIỀN KỲ ĐA NGUỒN — BIẾT THÔNG MINH SẢN PHẨM NÀO NÊN QUAY CẢNH GÌ, DÙNG ĐẠO CỤ GÌ & HIỆU ỨNG GÌ]:
    Phân tích ngữ nghĩa cụ thể của từng sản phẩm để chọn chính xác kỹ thuật đắt giá nhất từ 8 KOC:
    (@meshinthuine, @honghanhxinhgai_01, @kieneditcuong, @3thag8_, @byraanni, @grayunbox, @minhtienoiii06, @yuhtt09)
    thay vì gợi ý chung chung cứng nhắc!
    """
    desc_low = (description or "").lower()
    yavg = float(img_metrics.get("avg_luminance_yavg", 132.0))

    # Mặc định thông minh (Hệ hợp nhất 8 KOC)
    strategy: Dict[str, Any] = {
        "recommended_vibe_code": "V0",
        "primary_koc_fusion": "@meshinthuine + @byraanni + @grayunbox + @minhtienoiii06 + @yuhtt09",
        "semantic_icon_family": "✨ ✦ ✓ 🤍",
        "bespoke_visual_hook": "",
        "bespoke_asmr_trigger": "",
        "creative_hook_options": [],
        "tailored_physics_props": [],
        "tailored_lighting_and_wardrobe": "",
        "audio_and_bgm_blueprint": {
            "recommended_bgm_key": "bgm_v1_meshinthuine_warm_indie_acoustic_108bpm",
            "bgm_style_note": "Warm Indie Acoustic / Cafe Guitar 108 BPM (Ducking 18% -> 5% khi có giọng đọc)",
            "recommended_sfx_keys": ["crystal_aha_shimmer", "clean_velvet_whoosh", "luxury_soft_pop", "cart_gold_chime"]
        },
        "auto_edit_effects_to_trigger": []
    }

    # Case 0A: Văn phòng phẩm / Sổ tay / Bút bi gel / Hộp bút / Góc học tập (@yuhtt09 #01 8.1M views, #04 4.1M views + @honghanhxinhgai_01 #05-#06 Casio Proof)
    if any(k in desc_low for k in ("sổ", "sổ tay", "planner", "bút", "hộp bút", "túi bút", "bóp viết", "giấy note", "văn phòng phẩm", "sticker", "kẹp tài liệu", "máy tính")) and not any(x in desc_low for x in ("quạt", "máy sấy", "máy hút bụi")):
        strategy.update({
            "primary_koc_fusion": "@yuhtt09 (8.1M Views Flashback Unbox & Pen-Swatch ASMR) + @honghanhxinhgai_01 (180° Lay-Flat Casio Calculator Proof & Chibi Stickers) + @byraanni (Macro Loupe)",
            "semantic_icon_family": "🌷 🎀 ✏️ 🌱",
            "bespoke_visual_hook": (
                "Cấu trúc Flashback Unbox (@yuhtt09 8.1M views): Cảnh 1 (0.0s-1.1s) mở sẵn nắp hộp đầy ắp bút/sổ tay hoặc mở phẳng túi bút 180 độ nhét vừa cả máy tính Casio (@honghanhxinhgai_01) kèm tiêu đề uốn cong ⌒ + Kaomoji *ੈ✩‧₊˚🌷🎀*ੈ✩‧₊˚ "
                "-> Cảnh 2 (1.1s-3.0s) quay ngược lại cảnh dùng dao rọc giấy mini (hình chân mèo hồng) rạch băng keo thùng hàng!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng dao rọc giấy rạch băng keo giòn rụm + Tiếng bấm ngòi bút bi gel 'tách tách' + "
                "Tiếng ngòi bút viết sột soạt trên giấy định lượng dày & tiếng kéo khóa túi bút mở phẳng 180 độ (@yuhtt09 & @honghanhxinhgai_01)!"
            ),
            "creative_hook_options": [
                "Hook 1 (Flashback Unbox 8.1M views - @yuhtt09): Mở sẵn hộp khoe trọn bộ màu pastel 1.1s -> Cắt về cảnh rạch thùng hàng + Bóc xốp nổ",
                "Hook 2 (Test ngòi ngang / khô nhanh & Báo giá hạt dẻ 4.1M views): 'Bút gel bấm êm viết siêu mượt mà chỉ 9 🌱/chiếc' (Viết thử từng màu + miết ngón tay kiểm chứng không lem)",
                "Hook 3 (Mở phẳng 180° nhét vừa máy tính Casio - @honghanhxinhgai_01 #05): Mở khóa túi bút trải phẳng như khay, xếp 30 cây bút + đặt vừa vặn cả chiếc máy tính khoa học Casio ('để được cả máy tính +-=')"
            ],
            "tailored_physics_props": [
                "Dao Rọc Giấy Mini Hình Chân Mèo Hồng (@yuhtt09): Đạo cụ nhận diện thương hiệu khi mở thùng carton ở giây 1.1s.",
                "Bài Test Viết Thử & Quệt Ngón Tay Không Lem (@yuhtt09 4.1M views): Viết trực tiếp tên từng mã màu lên giấy trắng rồi dùng ngón trỏ miết ngang ngay lập tức để chứng minh mực khô siêu tốc!",
                "Bài Test Mở Phẳng 180 Độ + Nhét Máy Tính Casio (@honghanhxinhgai_01 #05): Nếu là hộp bút/túi đựng, mở banh 180 độ rồi thả 20-30 cây bút kèm 1 chiếc máy tính Casio bỏ túi vào rồi kéo khóa zip êm ru."
            ],
            "tailored_lighting_and_wardrobe": (
                "Studio High-Key Airy Douyin White (@yuhtt09 YAVG ~166) hoặc Thảm bàn chần bông ấm áp (@honghanhxinhgai_01): "
                "Bảng lỗ trắng gắn nơ ruy-băng hồng Coquette 🎀 + Đèn ngủ bánh mì TOAST + Bộ lọc CapCut 'Trong như pha lê 44%' (@kieneditcuong #12) giúp da tay POV trắng hồng."
            ),
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm",
                "bgm_style_note": "Nhạc Sped-up K-Pop / Pop Coquette Pluck 130 BPM (@yuhtt09 8.1M views - Không cần đọc Voiceover, trộn 34% dưới tiếng ASMR thật)",
                "recommended_sfx_keys": [
                    "box_cutter_tape_slice",
                    "bubble_wrap_unroll_pop",
                    "pen_click_and_paper_write",
                    "zipper_slide_bag_smooth",
                    "sfx_kien_pac_low_telop_subtitle_pop",
                    "sfx_kien_poyo_kawaii_skin_touch_bounce",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "YUHTT09_ARCH_CURVED_TITLE_KAOMOJI",
                "YUHTT09_FLASHBACK_UNBOX_PACING",
                "YUHTT09_SPROUT_PRICE_REBUS",
                "HONGHANH_CHIBI_SUBTITLE_STICKER",
                "KIEN_POV_SKIN_CRYSTAL_FILTER_44",
                "BYRAANNI_DASHED_LOUPE_162"
            ]
        })

    # Case 0E (MỚI): Nệm hút chân không / Chăn ga gối / Gối / Sofa / Nội thất phòng ngủ (@minhtienoiii06 #03 731K views + @meshinthuine #05 Pantone Swatch)
    elif any(k in desc_low for k in ("nệm", "đệm", "chăn", "ga gối", "drap", "gối", "sofa", "ghế lười", "thảm", "giường")) and not any(x in desc_low for x in ("cho bé", "sơ sinh", "em bé")):
        strategy.update({
            "primary_koc_fusion": "@minhtienoiii06 (731K Views Water-Glass Jump Test & Vacuum Slice Inflation) + @meshinthuine (15.04% Like Rate Pantone Color Swatch Card & Dual-Pill Title) + @grayunbox (Studio Makeover)",
            "semantic_icon_family": "🛏️ 💤 🎨 ✨",
            "bespoke_visual_hook": (
                "Cảnh 1 (0.0s-1.5s): Đặt 1 ly nước đầy lên mặt nệm rồi nhảy mạnh cạnh ly mà nước KHÔNG sánh 1 giọt (@minhtienoiii06 #03 731K views) "
                "hoặc Hiện Thẻ Bảng Màu Pantone 4 Ô (COCOA / TRUFFLE) góc phải trên kèm Tiêu đề 2 Viên Thuốc Đôi '[set ga gối] [màu hottrend]' (@meshinthuine #05)!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng kéo dao rạch lớp nilon hút chân không cho chiếc nệm dày 25cm tự động phồng căng kèm tiếng xì hơi 'xììì' cực đã tai (`sfx_minhtien_vacuum_mattress_air_inflate_hiss.wav`) "
                "+ Tiếng bàn tay miết lên bề mặt vải lụa Ice Silk mát lạnh!"
            ),
            "creative_hook_options": [
                "Hook 1 (Test Ly Nước Không Đổ + Rạch Túi Hút Chân Không - @minhtienoiii06 731K views): Nhảy cạnh ly nước trên nệm lò xo độc lập -> Cắt sang cảnh rạch bịch nilon nệm tự phồng gấp 5 lần",
                "Hook 2 (Bảng Màu Pantone + Tiêu Đề Viên Thuốc Đôi - @meshinthuine #05): Hiện thẻ Pantone 4 tông màu + Sticker cắt rời họa tiết vải + Dấu ngày tháng máy ảnh film OCT 24 2026"
            ],
            "tailored_physics_props": [
                "Bài Test Ly Nước Chống Rung Lắc (@minhtienoiii06 #03): Đặt 1 cốc thủy tinh chứa 80% nước lên giữa nệm, dùng tay ấn mạnh hoặc nhảy bên cạnh để chứng minh lò xo độc lập không truyền động!",
                "Cảnh Rạch Nilon Tự Phồng (Vacuum Inflation One-Take): Quay liên tục không cắt cảnh rạch lớp bọc hút chân không để nệm/gối tự bung phồng lên trước mắt người xem.",
                "Đo Độ Dày Bằng Gang Tay (@minhtienoiii06): Đặt bàn tay căng ngang thành nệm kèm nhãn chữ 'độ dày 25cm'."
            ],
            "tailored_lighting_and_wardrobe": "Ánh sáng phòng ngủ ấm áp (YAVG ~148) + Mặc đồ ngủ ở nhà thoải mái đồng điệu với tông màu chăn ga (@meshinthuine & @minhtienoiii06).",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v1_meshinthuine_warm_indie_acoustic_108bpm",
                "bgm_style_note": "Nhạc Indie Ấm Áp Chữa Lành 108 BPM (@meshinthuine) kết hợp tiếng rạch túi hút chân không tự phồng",
                "recommended_sfx_keys": [
                    "sfx_minhtien_vacuum_mattress_air_inflate_hiss",
                    "box_cutter_tape_slice",
                    "sfx_kien_pac_low_telop_subtitle_pop",
                    "clean_velvet_whoosh",
                    "cart_gold_chime"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "MESHIN_PANTONE_SWATCH_CARD_AND_DUAL_PILL",
                "MINHTIENOIII_DASHED_HEIGHT_RULER_1M7",
                "KIEN_3POINT_ORGANIC_HANDHELD_ROTATION_ZOOM"
            ]
        })

    # Case 0F (MỚI): Micro thu âm / Tai nghe Bluetooth / Loa / Thiết bị âm thanh (@byraanni #01 1.2M views TNW A41 & #05 Redmi Buds 8 Lite)
    elif any(k in desc_low for k in ("micro", "mic thu âm", "mic không dây", "tai nghe", "airpods", "buds", "loa", "bluetooth")):
        strategy.update({
            "primary_koc_fusion": "@byraanni (1.2M Views 4-Stage Extreme ASMR Mic Proof & Floating Part-Pointer Specs) + @3thag8_ (Ngâm Nước One-Take) + @kieneditcuong (Zoom Nét Đứt)",
            "semantic_icon_family": "🎙️ 🎧 🧊 ✨",
            "bespoke_visual_hook": (
                "Liên hoàn 4 Bài Test Âm Thanh Thực Tế trong 3.5s đầu TRƯỚC KHI KHUI HỘP (@byraanni #01 1.2M views): "
                "(1) Kẹp mic sát túi nilon bóp sột soạt -> (2) Kẹp mic lên thành ly thủy tinh khi rót nước -> (3) Kẹp lên bát khoai tây chiên bẻ giòn rụm -> (4) Thả đá viên & gõ bàn phím cơ!"
            ),
            "bespoke_asmr_trigger": (
                "100% Native ASMR sắc nét từ chính micro/thiết bị: tiếng rót nước lọc, tiếng bẻ snack giòn tan, tiếng đá viên lanh canh, tiếng gõ phím cơ 'clack clack' và tiếng bật nắp hộp sạc 'tách'!"
            ),
            "creative_hook_options": [
                "Hook 1 (4-Stage Extreme ASMR Proof - @byraanni 1.2M views): Kẹp mic thu trực tiếp 4 âm thanh đời thực trong 3.5s đầu rồi mới mở hộp",
                "Hook 2 (Floating Part-Pointer Specs - @byraanni #05): Cầm hộp sạc tai nghe Pastel mở nắp kèm các dòng thông số nhỏ ('Hybrid ANC 42dB', 'Driver 12.4mm', 'Dual Mic AI') bám sát từng bộ phận"
            ],
            "tailored_physics_props": [
                "Đạo Cụ 4 Tầng Thử Mic (@byraanni #01 1.2M views): Chuẩn bị sẵn 1 ly thủy tinh + chai nước, 1 bát snack khoai tây, 1 muỗng đá viên và 1 bàn phím cơ để kẹp mic trực tiếp lên thành ly/bát quay cận cảnh!",
                "Test Lực Hút Nam Châm & Dây Đeo (@byraanni): Quay cảnh đặt viên nam châm sau áo hút chặt mic không rơi + Kéo dây đeo cổ nam châm tiện lợi."
            ],
            "tailored_lighting_and_wardrobe": "Bàn tròn trắng Bắc Âu + Đèn bàn chao xếp ly vàng ấm + Áo len tay loe đen/nâu tạo độ tương phản sang trọng cho thiết bị màu Pastel (@byraanni).",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v5_byraanni_pinterest_editorial_rnb_102bpm",
                "bgm_style_note": "Tắt nhạc nền ở 3.5s đầu để phô diễn 100% Native ASMR của mic, sau đó đệm nhẹ Pinterest Chill R&B 102 BPM (@byraanni)",
                "recommended_sfx_keys": [
                    "water_pour_splash_test",
                    "crispy_bite_crunch",
                    "sfx_kien_pac_low_telop_subtitle_pop",
                    "magnifier_loupe_zoom",
                    "cart_gold_chime"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "BYRAANNI_FLOATING_PART_POINTER_SPECS",
                "BYRAANNI_DASHED_LOUPE_162",
                "KIEN_3POINT_ORGANIC_HANDHELD_ROTATION_ZOOM"
            ]
        })

    # Case 0G (MỚI): Sách cho bé / Đồ chơi giáo dục / Đồ Mẹ & Bé (@meshinthuine #01 2.9M views & #02 2.3M views)
    elif any(k in desc_low for k in ("cho bé", "sơ sinh", "em bé", "sách âm thanh", "sách vải", "đồ chơi", "mẹ và bé", "bỉm", "bình sữa", "ăn dặm")):
        strategy.update({
            "primary_koc_fusion": "@meshinthuine (2.9M Views Intimate Mother-Baby POV & 2.3M Views White-Stroke Cutout PIP Storyteller)",
            "semantic_icon_family": "👶🏻 📖 🍼 🤍",
            "bespoke_visual_hook": (
                "Cấu trúc White-Stroke Cutout PIP (@meshinthuine #02 2.3M views): Nền chính V1 quay cận cảnh tay mẹ dùng que chỉ bấm vào từng trang sách phát ra tiếng nói ('Yêu mẹ', 'Mẹ đi làm'), "
                "đồng thời góc trái dưới hiện Cửa Sổ Tách Nền Viền Trắng Dày (Sticker Cutout PIP) cảnh hai mẹ con đang tương tác thật!"
            ),
            "bespoke_asmr_trigger": "Tiếng loa sách điện tử phát âm thanh trong trẻo + Tiếng em bé cười/ê a thật + Tiếng lật trang sách bìa cứng",
            "creative_hook_options": [
                "Hook 1 (1.000 Ngày Đầu Đời Storytelling - @meshinthuine 2.9M views): Cảnh POV mẹ nằm đọc sách tương phản Đỏ-Đen-Trắng cho bé sơ sinh kèm khối chữ tâm sự 3 đoạn ở trung tâm",
                "Hook 2 (White-Stroke Cutout PIP - @meshinthuine 2.3M views): Toàn màn hình quay cận cảnh que chỉ bấm nút âm thanh trên sách + Hình tách nền viền trắng của mẹ và bé ở góc trái dưới"
            ],
            "tailored_physics_props": [
                "Tương Tác Thật Cùng Bé (@meshinthuine): Quay 1 đúp toàn cảnh mẹ và bé cùng chơi sản phẩm (để AI tách nền làm Sticker PIP viền trắng) + 1 đúp POV cận cảnh bàn tay thao tác từng nút bấm/trang sách."
            ],
            "tailored_lighting_and_wardrobe": "Ánh sáng phòng ngủ ấm cúng dịu mắt cho bé (YAVG ~142) + Chăn ga trắng kem sạch sẽ.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v1_meshinthuine_warm_indie_acoustic_108bpm",
                "bgm_style_note": "Nhạc Indie Acoustic Ấm Áp 108 BPM (@meshinthuine) hạ nhỏ 5% nhường chỗ cho giọng kể của mẹ và tiếng sách nói",
                "recommended_sfx_keys": [
                    "luxury_soft_pop",
                    "sfx_kien_pac_low_telop_subtitle_pop",
                    "clean_velvet_whoosh",
                    "cart_gold_chime"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "MESHIN_WHITE_STROKE_CUTOUT_PIP",
                "MESHIN_PANTONE_SWATCH_CARD_AND_DUAL_PILL",
                "KIEN_3POINT_ORGANIC_HANDHELD_ROTATION_ZOOM"
            ]
        })

    # Case 0B: Thời trang / Quần áo / Áo len / Tất vớ / Túi xách / Giày dép (@yuhtt09 #02 5.5M views + @meshinthuine #03 15.04% Like Rate Rattan Basket)
    elif archetype == "P3" and not any(k in desc_low for k in ("dây chuyền", "nhẫn", "vòng tay", "khuyên tai", "bạc", "kính", "kẹp tóc")):
        strategy.update({
            "primary_koc_fusion": "@yuhtt09 (5.5M Views 6-Step Faceless Garment & Shop Rating Pill) + @meshinthuine (15.04% Like Rate Rattan Vali Pop-Out & Pantone Swatch) + @byraanni (Lookbook Collage)",
            "semantic_icon_family": "🧦 👗 👜 🎀",
            "bespoke_visual_hook": (
                "Gắn Huy Hiệu Uy Tín '⭐ 4.9/5 (2.1k) | Đã bán 23.6K' (@yuhtt09 #23) hoặc Mở chiếc Vali Mây Đan Vintage cho 5 chiếc áo len/đồ gấp gọn bật nảy ra liên hoàn kèm Dấu ngày tháng máy film 'OCT 24 2026' (@meshinthuine #03 - 15.04% Like/View)!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng bật khóa vali mây đan, tiếng kéo khóa túi zip nhựa mờ 'xoẹt', tiếng búng ngón tay vào tag giấy 🏷️, "
                "tiếng kéo giãn cổ áo/cổ tất đàn hồi 4 chiều & tiếng kéo khóa túi xách mượt mà (@yuhtt09 & @meshinthuine)!"
            ),
            "creative_hook_options": [
                "Hook 1 (Vali Mây Đan Pop-Out + Film Date Stamp - @meshinthuine #03 15.04% Like Rate): Mở nắp giỏ mây đan lấy lần lượt 5 mẫu áo len Hàn Quốc phối sẵn theo bảng màu Pantone",
                "Hook 2 (Social Proof Rating Pill - @yuhtt09 #23): Hiện thanh đánh giá '⭐ 4.8/5 | Đã bán 23.6K' ngay trên ngực áo để chốt uy tín trong 1.2s đầu",
                "Hook 3 (Nhét Cả Thế Giới Vào Túi - @yuhtt09 #27-#29): Bỏ lần lượt phấn nước, bảng mắt, son, nước hoa, điện thoại vào túi xách để chứng minh sức chứa"
            ],
            "tailored_physics_props": [
                "Quy Trình 6 Bước Kiểm Định Quần Áo Không Cần Lộ Mặt (@yuhtt09 #23-#26): (1) Giơ áo trước cửa gỗ -> (2) Rút khỏi túi zip mờ -> (3) Khoe tag mác chính hãng 🏷️ -> (4) Vạch lót nỉ/cotton bên trong nhéo thử độ dày -> (5) Macro đường chỉ thêu/túi áo -> (6) Mặc thử cắt ngang cổ xoay trước gương.",
                "Nếu là Tất / Vớ (@yuhtt09 #02 5.5M views): Luồn hẳn bàn tay vào bên trong từng đôi tất rồi xòe rộng 5 ngón tay kéo căng 4 chiều để chứng minh dệt kim dày dặn không xù lông!",
                "Nếu là Túi xách (@yuhtt09 #27-#29): Thực hiện bài test 'What's In My Bag' thả 5-6 món mỹ phẩm vào túi + Cảnh xách túi đứng trên nền sàn bê tông xám nối vòng lặp Seamless Loop."
            ],
            "tailored_lighting_and_wardrobe": "Ánh sáng trắng trong trẻo (YAVG ~166 chuẩn @yuhtt09) hoặc Nắng ấm phòng ngủ (@meshinthuine) kết hợp gương soi toàn thân góc cắt ngang cổ.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm",
                "bgm_style_note": "Nhạc Sped-up K-Pop Pluck 130 BPM (@yuhtt09) đẩy nhịp cắt nhanh 1.02s-1.15s/cảnh qua từng mẫu áo/tất",
                "recommended_sfx_keys": [
                    "box_cutter_tape_slice",
                    "zipper_slide_bag_smooth",
                    "ui_double_pop",
                    "clean_velvet_whoosh",
                    "camera_shutter_clean",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "YUHTT09_SHOP_RATING_SOCIAL_PROOF_PILL",
                "MESHIN_PANTONE_SWATCH_CARD_AND_DUAL_PILL",
                "YUHTT09_ARCH_CURVED_TITLE_KAOMOJI",
                "YUHTT09_SPROUT_PRICE_REBUS",
                "RADIAL_BLUR_LOOP"
            ]
        })

    # Case 0C: Trang sức bạc / Dây chuyền / Nhẫn / Kính mắt / Gương LED / Kẹp tóc (@honghanhxinhgai_01 #01 21.3M views Sashimi Hair Clip + @yuhtt09 #05 3.7M views)
    elif any(k in desc_low for k in ("dây chuyền", "nhẫn", "vòng tay", "khuyên tai", "bạc", "trang sức", "kính", "gọng kính", "gương", "kẹp tóc")):
        strategy.update({
            "primary_koc_fusion": "@honghanhxinhgai_01 (21.3M Views Supermarket Sashimi Basket Hook & Backpack Toss Durability Proof) + @yuhtt09 (3.7M Views Seal-Peel & 3 Silver Jewelry Trust-Builders) + @byraanni (Stop-Motion Knolling)",
            "semantic_icon_family": "💍 🐟 ✨ 🎀",
            "bespoke_visual_hook": (
                "Đặt sản phẩm vào Giỏ Siêu Thị Hồng Mini kèm 2 Bình Luận Trái Chiều (@honghanhxinhgai_01 #01 - 21.3 TRIỆU VIEWS!) "
                "hoặc Cận cảnh Macro nghiêng mặt đá/mặt gương dưới đèn bắt tia lấp lánh (@yuhtt09 3.7M views) / Stop-Motion xếp kẹp tóc lên khay sứ lượn sóng (@byraanni #03)!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng lột tấm seal nilon khỏi mặt gương LED 'xẹt' êm ái (@yuhtt09 3.7M views), "
                "tiếng mở hộp nhung trang sức 'tách', hoặc tiếng bóp lò xo kẹp tóc acrylic chắc nịch!"
            ),
            "creative_hook_options": [
                "Hook 1 (Giỏ Siêu Thị Mini + Ném Vào Balo Test Độ Bền - @honghanhxinhgai_01 21.3M views): Đặt kẹp tóc trong giỏ siêu thị mini -> Ném thẳng vào balo đựng đầy sách vở mang đi học về vẫn lành lặn ('chỉ 49 🐟')",
                "Hook 2 (Bộ 3 Bảo Chứng Bạc Thật - @yuhtt09 #44-#46): Khoe ngay Thẻ bảo hành + Chai nước rửa bạc + Khăn lau bạc đi kèm trong hộp quà có nơ",
                "Hook 3 (Lột Seal Gương LED Đổi 3 Màu Đèn - @yuhtt09 3.7M views): Lột tấm màng bảo vệ gương sát mic rồi chạm ngón tay đổi 3 chế độ đèn Trắng - Vàng - Trung tính"
            ],
            "tailored_physics_props": [
                "Nếu là Kẹp tóc / Phụ kiện (@honghanhxinhgai_01 21.3M views & @yuhtt09 1.7M views): Quay bài test 'Nhét Balo Mang Đi Tùm Lum' (bỏ kẹp tóc vào balo xóc mạnh rồi lấy ra chứng minh nhựa acrylic dày không gãy răng) + Kẹp thử lên mái tóc dày thật!",
                "Nếu là Trang sức bạc (@yuhtt09 #44-#46): Bắt buộc quay đủ Bộ 3 Bảo Chứng Uy Tín (Thẻ bảo hành + Nước rửa bạc + Khăn lau bạc) + Xoay nghiêng viên đá Moonstone dưới đèn để thấy ánh xanh dương đổi màu!",
                "Nếu là Gương LED (@yuhtt09 3.7M views): Giữ nguyên tấm seal nilon trên mặt gương để quay cảnh lột seal One-Take + Chạm nút cảm ứng đổi 3 màu ánh sáng."
            ],
            "tailored_lighting_and_wardrobe": "Bàn trắng Pegboard Coquette (@yuhtt09) hoặc Thảm chần bông đèn vàng ấm (@honghanhxinhgai_01) + Bộ lọc 'Trong như pha lê 44%' (@kieneditcuong).",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm",
                "bgm_style_note": "Nhạc Sped-up K-Pop Coquette Pluck 130 BPM (@yuhtt09) hoặc Kawaii Lo-Fi 116 BPM (@honghanhxinhgai_01)",
                "recommended_sfx_keys": [
                    "screen_seal_peel_smooth",
                    "crystal_aha_shimmer",
                    "ui_double_pop",
                    "magnifier_loupe_zoom",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "YUHTT09_ARCH_CURVED_TITLE_KAOMOJI",
                "HONGHANH_CHIBI_SUBTITLE_STICKER",
                "YUHTT09_NUMBERED_FEATURE_BADGES",
                "KIEN_POV_SKIN_CRYSTAL_FILTER_44",
                "BYRAANNI_DASHED_LOUPE_162"
            ]
        })

    # Case 0D: Đồ ăn vặt / Bánh trung thu / Mật táo đỏ / Bánh phồng sữa / Bánh tráng / Kẹo dẻo (@minhtienoiii06 19.3M + @grayunbox 597K Cross-Section)
    elif archetype == "P5" or any(k in desc_low for k in ("bánh", "kẹo", "ăn vặt", "bánh tráng", "phồng sữa", "trung thu", "mật táo", "táo đỏ", "chip chip", "khoai môn", "socola", "mứt", "khô gà", "hạt", "sữa bột")):
        strategy.update({
            "primary_koc_fusion": "@minhtienoiii06 (19.3M Views Sensory & 4-Bag Glass Bowl Montage) + @grayunbox (597K Views Sunlit Cross-Section Split & Viscous Syrup Drip) + @3thag8_ (Cross-Section Dip) + @kieneditcuong (11 Food SFX)",
            "semantic_icon_family": "🗣️ 🍅 🍠 ✨ 🤤",
            "bespoke_visual_hook": (
                "Nhịp cắt siêu tốc 1.1s (@minhtienoiii06 19.3M views): Cầm đôi 2 màu tương phản / Bẻ đôi bánh lộ nhân phô mai 2 màu dưới nắng xiên (@grayunbox 597K views) "
                "hoặc Xé 4 gói bim bim đổ vào 4 góc bát thủy tinh lớn (@minhtienoiii06 1.59M views) / Múc mật táo đỏ đặc sánh kéo sợi từ thìa sứ trắng (@grayunbox 302K views)!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng xé bánh dẻo/giòn sát mic 15cm + Tiếng kéo nhân phô mai/mật sánh (`sfx_kien_cheese_pull_mucus_necha_mlem.wav`) + "
                "Tiếng khuấy đá lanh canh dưới nắng + Đặt 1 NẮP HỘP THIẾC RỖNG ở dưới để thả viên kẹo vào tạo tiếng vang 'tách - keng' ASMR gấp 3 lần (@minhtienoiii06)!"
            ),
            "creative_hook_options": [
                "Hook 1 (Bẻ Đôi Lộ Nhân 2 Màu Dưới Nắng Xiên - @grayunbox 597K views): Hai tay cầm 2 nửa bánh vừa cắt (tím việt quất + xanh matcha nhân phô mai) đưa sát ống kính dưới ánh nắng rèm sáo",
                "Hook 2 (Tranh luận từ vựng vùng miền - @minhtienoiii06 12.9M views): 'Bịch Bánh Tráng ❌ / Bao Bánh Tráng ✅ — Cho hỏi chỗ mọi người gọi là Bịch hay Bao ?'",
                "Hook 3 (Kết hợp biến tấu 'Ăn kiểu này ngon' - @minhtienoiii06 13.8M views): '🗣️ ai thử món này chưa ?' (Trải bánh phồng sữa múc kem lạnh cuộn tròn như bánh Crepe rồi cắn ngập răng!)"
            ],
            "tailored_physics_props": [
                "Bẻ Đôi Lộ Nhân & Dao Nhựa Xúc Lõi Phô Mai (@grayunbox 597K views): Cắt đôi chiếc bánh trước để mở màn ở 0.0s, sau đó dùng dao/thìa xúc thẳng vào phần nhân mềm mịn ở giữa.",
                "Múc Sốt / Mật Đặc Kéo Sợi Dưới Nắng (@grayunbox 302K views): Dùng thìa sứ trắng múc mật táo đỏ/sữa đặc giơ cao cho dòng mật sánh chảy kéo sợi xuống ly thủy tinh trong nắng.",
                "Vũ đạo Cầm Đôi & Bóp Nhún Đàn Hồi (@minhtienoiii06): Bóp xẹp chiếc bánh bông lan mini cho tự phồng lại như squishy rồi xé đôi lộ thớ bánh vàng ươm.",
                "Bia Cộng Hưởng Âm Thanh Nắp Thiếc (@minhtienoiii06): Nếu là kẹo viên/vật nhỏ, bắn/thả vào nắp hộp thiếc rỗng để thu tiếng 'tách - keng' vang giòn."
            ],
            "tailored_lighting_and_wardrobe": (
                "Bàn học Chill @minhtienoiii06 (Đèn ngủ bánh mì TOAST + iPad mở hoạt hình Shin/Doraemon chạy ngầm) "
                "hoặc Bàn gỗ tối màu đón nắng xiên qua rèm sáo ngang (@grayunbox)."
            ),
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v7_minhtienoiii_healing_farm_orchestra_124bpm",
                "bgm_style_note": "Nhạc Nông Trại Chữa Lành (Akito orchestra 124 BPM) trộn dưới tiếng ASMR xé/cắn thật & SFX đồ ăn @kieneditcuong",
                "recommended_sfx_keys": [
                    "ping_pong_question",
                    "ui_double_pop",
                    "snack_bag_crinkle_open",
                    "sfx_kien_cheese_pull_mucus_necha_mlem",
                    "sfx_kien_sizzling_pan_fry_crackle",
                    "tin_lid_metallic_clink",
                    "crispy_bite_crunch",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "MINHTIENOIII_DIALECT_DEBATE_OR_SPEAKING_HOOK",
                "MINHTIENOIII_AGRICULTURAL_PRICE_AND_SENSORY_SHIELD",
                "MINHTIENOIII_HYPER_TACTILE_125S_CUTS",
                "RADIAL_BLUR_LOOP"
            ]
        })

    # Case 0B: Tripod / Gậy chụp ảnh / Đèn trợ sáng / Giá đỡ điện thoại (@minhtienoiii06 #02 15.5M views & #22 1.65M views)
    elif any(k in desc_low for k in ("tripod", "gậy chụp ảnh", "gậy selfie", "giá đỡ điện thoại", "gimbal", "đèn trợ sáng", "livestream", "1m7")):
        strategy.update({
            "primary_koc_fusion": "@minhtienoiii06 (15.5M Views Live Viewfinder + Thước Đo 1m7) + @byraanni (Kính Lúp 162%) + @kieneditcuong (Zoom-Hold)",
            "semantic_icon_family": "📸 💡 🗣️ ✨ 📏",
            "bespoke_visual_hook": (
                "Cầm Tripod đã gắn sẵn 1 chiếc điện thoại thứ 2 ĐANG MỞ MÀN HÌNH CAMERA QUAY TRỰC TIẾP (Live Viewfinder in Frame - @minhtienoiii06 15.5M views) "
                "kèm câu Hook: 'đi chơi hay đi du lịch 1 mình có cái này vẫn tự 📸 ảnh xinh'!"
            ),
            "bespoke_asmr_trigger": "Tiếng kéo khớp inox 'xoẹt', tiếng bung 3 chân tripod 'tạch', tiếng bấm remote Bluetooth 'tách' & tiếng màn trập chụp ảnh",
            "creative_hook_options": [
                "Hook 1 (Nỗi đau đi chơi 1 mình - 15.5M views): 'đi chơi hay đi du lịch 1 mình có cái này vẫn tự 📸 ảnh xinh'",
                "Hook 2 (Biến hình 3-in-1): Gập gọn vừa lòng bàn tay -> Kéo dài 1m7 đứng vững kèm thước đo nét đứt < - - - 1m7 - - - >"
            ],
            "tailored_physics_props": [
                "Bằng Chứng Màn Hình Camera Sống (@minhtienoiii06 15.5M views): Gắn 1 điện thoại phụ mở sẵn app Camera góc rộng 0.5x lên Tripod để người xem thấy đồng thời cả chiếc Tripod bên ngoài LẪN góc nhìn siêu rộng bên trong màn hình điện thoại!",
                "Quay cảnh kéo dài tối đa đặt trên sàn nhà để Bộ Edit tự động vẽ Đường Kẻ Nét Đứt Đo Chiều Cao (< - - - 1m7 - - - >) dọc thân cây!",
                "Tháo rời đèn LED đôi bật đủ 3 chế độ màu (Trắng - Vàng - Trung tính) chiếu thẳng vào ống kính + Tháo rời nút bấm Bluetooth chụp từ xa."
            ],
            "tailored_lighting_and_wardrobe": "Bàn học sáng có kệ gỗ + cây xanh rủ (@minhtienoiii06) kết hợp quay góc rộng toàn thân trong phòng ngủ/phòng khách khi kéo dài 1m7.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v7_minhtienoiii_healing_farm_orchestra_124bpm",
                "bgm_style_note": "Nhạc Giao Hưởng Nhịp Nhanh (Mozart - Eine Kleine Nachtmusik 124 BPM) đẩy tốc độ cắt 1.36s/cảnh cực kỳ lôi cuốn",
                "recommended_sfx_keys": [
                    "ping_pong_question",
                    "mech_click_v1",
                    "magnifier_loupe_zoom",
                    "camera_shutter_clean",
                    "clean_velvet_whoosh",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "MINHTIENOIII_DASHED_HEIGHT_RULER_1M7",
                "MINHTIENOIII_AGRICULTURAL_PRICE_AND_SENSORY_SHIELD",
                "BYRAANNI_DASHED_LOUPE_162",
                "KIEN_4KF_ZOOM_HOLD"
            ]
        })

    # Case 1: Sản phẩm Răng miệng / Bàn chải (@grayunbox #06 - 216K views)
    elif any(k in desc_low for k in ("bàn chải", "kem đánh răng", "tăm nước", "niềng răng", "răng")):
        strategy.update({
            "primary_koc_fusion": "@grayunbox (Proxy Proof) + @byraanni (Kính Lúp 162%) + @kieneditcuong (Glow Hook)",
            "semantic_icon_family": "🪥 🫧 ✨ 🦷",
            "bespoke_visual_hook": "Cận cảnh Macro 15cm đầu bàn chải bật viền phát quang EDGE_GLOW (@kieneditcuong) + Ngón tay miết thử độ đàn hồi sợi lông",
            "bespoke_asmr_trigger": "Tiếng miết đầu lông bàn chải 'sột soạt' sát mic 15cm + Tiếng xoáy nắp tuýp kem đánh răng",
            "tailored_physics_props": [
                "Đạo cụ Thế thân Sạch (@grayunbox): Chuẩn bị 1 nắp tuýp kem đánh răng có rãnh xoắn sâu bên trong — quay cảnh chải trực tiếp vào rãnh nắp & nếp gấp khớp ngón tay để chứng minh sợi lông siêu mảnh luồn sạch mọi ngóc ngách mà KHÔNG cần quay cảnh đánh răng trong miệng!",
                "Giữ yên đầu bàn chải 2.5 giây trước ống kính để AI tự động bật Kính Lúp Tròn Nét Đứt phóng đại 162% (@byraanni) soi mật độ sợi lông."
            ],
            "tailored_lighting_and_wardrobe": "Bàn trắng mờ cạnh cửa sổ rèm sáo ngang (@grayunbox) + Mặc áo khoác Denim đen chỉ nổi để lông bàn chải trắng/pastel bật lên sắc nét.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v6_grayunbox_holiday_breakfast_jazz_112bpm",
                "bgm_style_note": "Nhạc Jazz Bữa Sáng Tinh Tế (sano mika - Elegant holiday breakfast 112 BPM) cắt khớp 50% phách nhạc",
                "recommended_sfx_keys": ["glowing_stroke_freeze", "magnifier_loupe_zoom", "paper_tear_manga_sketch", "asmr_tactile_click", "cart_gold_chime"]
            },
            "auto_edit_effects_to_trigger": ["KIEN_GLOW_STROKE_FREEZE", "BYRAANNI_DASHED_LOUPE_162", "GRAYUNBOX_EMOJI_REBUS"]
        })

    # Case 2: Hương thơm / Sáp thơm / Trầm hương / Nước hoa / Body Mist / Trà (@yuhtt09 #03 4.8M views, #35-#38 + @grayunbox #01 2.8M views)
    elif any(k in desc_low for k in ("trầm", "nhang", "sáp thơm", "nến thơm", "tinh dầu", "nước hoa", "body mist", "xịt thơm", "trà xanh", "bột matcha")) and not any(x in desc_low for x in ("quạt", "máy sấy", "máy hút bụi", "áo", "quần", "kẹp tóc")):
        strategy.update({
            "primary_koc_fusion": "@yuhtt09 (4.8M Views Sweater-Sleeve Mist Spritz & Shimmer Swirl) + @grayunbox (Nắng Rèm Sáo + Hạt Lá Bay 🍃) + @byraanni (Collage 3 Cảnh)",
            "semantic_icon_family": "🍃 🍵 🌿 ✨",
            "bespoke_visual_hook": "Cận cảnh xịt chùm tia sương mịn ngược sáng lên cổ tay áo len trắng (@yuhtt09 4.8M views) hoặc bóc lớp màng seal bạc / đốt khói trầm bay lên dưới vệt nắng xiên qua rèm sáo ngang (@grayunbox 2.8M views)",
            "bespoke_asmr_trigger": "Tiếng vòi xịt sương 'xịt' mịn sát mic (`fine_mist_spray_shimmer`), tiếng bóc seal bạc 'xoẹt' giòn tan, hoặc tiếng bật lửa 'tách'",
            "tailored_physics_props": [
                "Nếu là Sáp thơm / Gel (@grayunbox): Dùng 1 que tăm gỗ nhỏ chọc nhẹ vào bề mặt thạch sáp (Toothpick Jelly-Poke) để chứng minh chất thạch trong veo núng nính!",
                "Nếu là Nước hoa / Xịt thơm quần áo (@yuhtt09 4.8M views & @grayunbox): Xịt trực tiếp lên cổ tay áo len dệt kim trắng dày dặn (để hạt sương bám lên sợi len) hoặc áo khoác bò đen + Lắc nhẹ thân chai nếu có nhũ kim tuyến xoáy tròn dưới đèn (#38)!",
                "Nếu có Quà tặng kèm (như hộp diêm, lư đồng, túi thơm, chai chiết mini): Giơ món quà tặng ra ở giây thứ 3.5 để Bộ Edit kích hoạt hiệu ứng Chụp ảnh đứng hình Manga Freeze-Frame 0.45s!"
            ],
            "tailored_lighting_and_wardrobe": "Bối cảnh Nắng xiên qua rèm sáo ngang (@grayunbox) hoặc Bàn trắng Pegboard Coquette (@yuhtt09) làm bật tia sương.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v6_grayunbox_holiday_breakfast_jazz_112bpm",
                "bgm_style_note": "Nhạc Cafe Bossanova / Holiday Breakfast Jazz 112 BPM (@grayunbox) hoặc Sped-up Pop Pluck 130 BPM (@yuhtt09) kết hợp tiếng xịt sương mịn",
                "recommended_sfx_keys": ["fine_mist_spray_shimmer", "snack_bag_crinkle_open", "paper_tear_manga_sketch", "shutter_v1", "clean_velvet_whoosh", "cart_gold_chime"]
            },
            "auto_edit_effects_to_trigger": ["GRAYUNBOX_SCENT_LEAF_PARTICLES", "GRAYUNBOX_BONUS_GIFT_FREEZE_FRAME", "GRAYUNBOX_EMOJI_REBUS"]
        })

    # Case 3: Kệ / Tủ / Hộp đựng đồ / Đồ lắp ráp nhiều chi tiết (@grayunbox #08 - 170K views)
    elif any(k in desc_low for k in ("kệ", "tủ", "hộp đựng", "lắp ráp", "nhiều ngăn", "giá để đồ")):
        strategy.update({
            "primary_koc_fusion": "@grayunbox (Finished-First Assembly Hook) + @3thag8_ (Test Chịu Lực) + @minhtienoiii06 (Thước Đo Kích Thước)",
            "semantic_icon_family": "🧸 📦 ✨ 💛",
            "bespoke_visual_hook": "Đảo ngược cấu trúc (@grayunbox): Mở đầu 2.0s bằng cảnh Kệ Đã Lắp Hoàn Chỉnh 100% xếp đầy gấu bông/đồ đạc gọn đẹp, rồi mới cắt về cảnh đập hộp lắp ráp!",
            "bespoke_asmr_trigger": "Tiếng ấn khớp nhựa 'tạch tạch' chắc nịch, tiếng lăn bánh xe 360 độ mượt trên sàn",
            "tailored_physics_props": [
                "Chuẩn bị sẵn gấu bông / sách vở / chai lọ nặng đặt lên kệ rồi dùng tay ấn thử độ chịu lực không võng + đẩy nhẹ cho kệ xoay 360 độ.",
                "Giữ máy cố định ở cảnh khớp khóa hoặc bánh xe 2.5s để AI bật Kính Lúp Tròn Nét Đứt 162% + Vẽ thước đo chiều cao nét đứt."
            ],
            "tailored_lighting_and_wardrobe": "Ánh sáng phòng tự nhiên rộng rãi, đặt máy góc 45 độ thấy trọn chiều cao của kệ.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v4_3thag8_classical_minuet_bounce_118bpm",
                "bgm_style_note": "Nhạc Cổ Điển Dây Búng Thanh Lịch (Boccherini's Menuet 118 BPM - @3thag8_) kết hợp tiếng khớp nhựa cơ học",
                "recommended_sfx_keys": ["mech_click_v1", "magnifier_loupe_zoom", "whoosh_in_v1", "radial_zoom_loop_whoosh", "bell_ding_cta"]
            },
            "auto_edit_effects_to_trigger": ["GRAYUNBOX_FINISHED_FIRST_HOOK", "BYRAANNI_DASHED_LOUPE_162", "MINHTIENOIII_DASHED_HEIGHT_RULER_1M7", "RADIAL_BLUR_LOOP"]
        })

    # Case 4: Sản phẩm phát sáng / Đèn LED / Thiệp 3D phát nhạc (@grayunbox #04 - 504K views)
    elif any(k in desc_low for k in ("đèn led", "phát sáng", "đèn ngủ", "thiệp", "sinh nhật", "dạ quang")) or yavg < 96.0:
        strategy.update({
            "primary_koc_fusion": "@grayunbox (Low-Key Ambient LED Mode YAVG ~85) + @kieneditcuong (Zoom-Hold)",
            "semantic_icon_family": "🎁 🎂 ✨ 💡",
            "bespoke_visual_hook": "Bật công tắc phát sáng ngay giây 0.5s trong phòng hạ tối nhẹ (Low-Key Ambient) để quầng sáng LED phản chiếu lung linh lên mặt bàn",
            "bespoke_asmr_trigger": "Tiếng gạt công tắc 'tách' + Giai điệu nhạc/ánh sáng thật của sản phẩm",
            "tailored_physics_props": [
                "Tắt bớt đèn trần chính, chỉ giữ 1 nguồn sáng phụ nhẹ để độ sáng nền giảm về YAVG ~85 — giúp ánh đèn LED của sản phẩm rực rỡ gấp 3 lần trên camera!"
            ],
            "tailored_lighting_and_wardrobe": "Chế độ Low-Key Ambient (@grayunbox): Nền tối dịu làm bật quầng sáng ấm của sản phẩm.",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v1_meshinthuine_warm_indie_acoustic_108bpm",
                "bgm_style_note": "Nhạc Indie Ấm Áp Dịu Nhẹ (Feels Like Magic 108 BPM) nhường không gian cho tiếng công tắc và hiệu ứng lấp lánh",
                "recommended_sfx_keys": ["crystal_aha_shimmer", "mech_click_v1", "glowing_stroke_freeze", "cart_gold_chime"]
            },
            "auto_edit_effects_to_trigger": ["GRAYUNBOX_LOWKEY_LED_GLOW", "KIEN_4KF_ZOOM_HOLD"]
        })

    # Case 5: Quạt mini / Máy sấy / Thiết bị có nút bấm nhiều cấp độ (@byraanni #02 918K views Confetti & Water Ripple)
    elif any(k in desc_low for k in ("quạt", "máy sấy", "máy hút bụi", "sạc", "pin", "máy ảnh")):
        strategy.update({
            "primary_koc_fusion": "@byraanni (918K Views Confetti Blast, Water Bowl Ripple & Floating Part-Pointer Specs) + @3thag8_ (Ngâm Nước One-Take)",
            "semantic_icon_family": "⚡ 🔋 💨 ✦",
            "bespoke_visual_hook": "Bật quạt thổi tung hộp kim tuyến bạc bay lên ống kính & thổi gợn sóng bát nước (@byraanni #02 - 918K views) hoặc thả thiết bị chống nước vào cốc thủy tinh (@3thag8_)",
            "bespoke_asmr_trigger": "Tiếng bấm nút chuyển cấp độ gió 'tạch tạch' (lên tới 100/199 cấp) + Tiếng gió vút mạnh dần + Tiếng nhíp dán sticker chữ cái DIY lên thân quạt",
            "tailored_physics_props": [
                "Bộ 3 Thị Giác Hóa Sức Gió 17.000 RPM (@byraanni #02 918K views): (1) Chuẩn bị 1 hộp nhỏ đựng kim tuyến bạc/giấy vụn để bật quạt thổi bay tung tóe lên camera; (2) Bật quạt thổi trực tiếp vào 1 bát nước thủy tinh cho mặt nước gợn sóng mạnh; (3) Dùng nhíp gắp sticker chữ cái dán tên riêng lên thân quạt!",
                "Giữ ngón tay chỉ vào nút bấm / màn hình LED trong 2.5 giây để Bộ Edit tự động gắn Kính Lúp Nét Đứt (@kieneditcuong #06 & @byraanni) kèm Floating Part-Pointer Specs."
            ],
            "tailored_lighting_and_wardrobe": "Mặt bàn trắng mờ + Áo len dệt kim màu Nâu Espresso/Đen kéo trễ ngang lòng bàn tay (@byraanni).",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v5_byraanni_pinterest_editorial_rnb_102bpm",
                "bgm_style_note": "Nhạc R&B / Chill Pop Thẩm Mỹ Pinterest (303 Music Vibes 102 BPM - @byraanni) kết hợp tiếng bấm nút tốc độ & tiếng thông số",
                "recommended_sfx_keys": ["snack_bag_crinkle_open", "mech_click_v1", "sfx_kien_pac_low_telop_subtitle_pop", "magnifier_loupe_zoom", "water_splash_submerge", "camera_shutter_clean"]
            },
            "auto_edit_effects_to_trigger": ["BYRAANNI_3SHOT_COLLAGE", "BYRAANNI_FLOATING_PART_POINTER_SPECS", "BYRAANNI_DASHED_LOUPE_162", "KIEN_3POINT_ORGANIC_HANDHELD_ROTATION_ZOOM"]
        })

    # Case 6: Bình giữ nhiệt / Ly giữ nhiệt (@3thag8_ #04 815K views 3-Way Drinking Hook + @byraanni #06 Pink Leopard Tumbler)
    elif any(k in desc_low for k in ("bình giữ nhiệt", "ly giữ nhiệt", "cốc giữ nhiệt", "bình nước")):
        strategy.update({
            "primary_koc_fusion": "@3thag8_ (815K Views 3-Way Drinking Action-First Hook) + @byraanni (Collage 3x1.1s, Test Dốc Ngược 180° & Floating Specs) + @yuhtt09 (1.6M Views Sunhouse)",
            "semantic_icon_family": "🧊 🥤 💧 ✨",
            "bespoke_visual_hook": (
                "Biểu diễn ngay 3 Cách Uống trong 3.5s đầu TRƯỚC KHI KHUI HỘP (@3thag8_ #04 - 815K views): "
                "(1) Bấm nút bật nắp ống hút -> (2) Mở khóa uống trực tiếp -> (3) Rót nước ra chiếc cốc nắp bình!"
            ),
            "bespoke_asmr_trigger": "Tiếng đá viên 'lách cách' rơi vào lòng inox 304 + Tiếng bấm lẫy bật nắp 'tạch' + Tiếng rót nước vào cốc nắp bình",
            "tailored_physics_props": [
                "Biểu Diễn 3 Cách Uống Đầu Video (@3thag8_ 815K views): Quay liên hoàn 3 thao tác bật ống hút, mở miệng uống trực tiếp và rót ra nắp cốc trong 3.5 giây đầu tiên rồi mới cắt về cảnh khui hộp và túi vải tặng kèm.",
                "Bài Test Dốc Ngược 180 Độ Không Rò Nước (@byraanni #06 & @yuhtt09 #39): Đổ đầy nước đá vào bình, đóng chặt nắp rồi DỐC NGƯỢC 180 ĐỘ LẮC MẠNH trước ống kính kèm nhãn 'Leakproof 💦'!"
            ],
            "tailored_lighting_and_wardrobe": "Bàn Pegboard hoa len đèn vàng ấm (@3thag8_) hoặc Bàn tròn trắng Bắc Âu + Áo len tay dài (@byraanni).",
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v5_byraanni_pinterest_editorial_rnb_102bpm",
                "bgm_style_note": "Nhạc Pinterest Chill R&B 102 BPM (@byraanni) trộn cùng tiếng rót nước đá 'lách cách' (`liquid_pour_ice_clink.wav`)",
                "recommended_sfx_keys": ["liquid_pour_ice_clink", "mech_click_v1", "sfx_kien_pac_low_telop_subtitle_pop", "magnifier_loupe_zoom", "radial_zoom_loop_whoosh", "cart_gold_chime"]
            },
            "auto_edit_effects_to_trigger": ["BYRAANNI_3SHOT_COLLAGE", "BYRAANNI_FLOATING_PART_POINTER_SPECS", "BYRAANNI_DUAL_FONT_HEADER", "RADIAL_BLUR_LOOP"]
        })

    # Case 7: Kem chống nắng / Cushion / Son / Mặt nạ / Xà phòng / Sữa rửa mặt / Duỗi tóc / Skincare (@3thag8_ #01 2.44M views + @yuhtt09 2026 + @kieneditcuong #05 Skincare SFX)
    elif any(k in desc_low for k in ("xà phòng", "sữa rửa mặt", "sữa tắm", "kem", "chống nắng", "cushion", "phấn", "serum", "mặt nạ", "toner", "tẩy tế bào", "son", "duỗi tóc", "ủ tóc", "dầu gội")):
        strategy.update({
            "primary_koc_fusion": "@3thag8_ (2.44M Views 3-Comment Social Proof Stack & Silk Foam Heart Drawing) + @yuhtt09 (2026 Makeup Proofs: Lẻ ❌ vs Combo ✅, Test Nước + Khăn Giấy Khô & 5 Ô Giấy Thấm Dầu) + @kieneditcuong (#05 Skincare SFX & #12 Crystal Clear 44% Skin Filter) + @meshinthuine (#04 Pajama-to-Glam Transition)",
            "semantic_icon_family": "🫧 ✨ 💦 🐣",
            "bespoke_visual_hook": (
                "Xếp chồng 3 Bình Luận Khen Thật trong 3s đầu trong khi kéo sợi bọt xà phòng tơ tằm trắng xóa & vẽ hình trái tim lên lớp bọt trên cánh tay (@3thag8_ #01 - 2.44M views) "
                "hoặc Bơm chất kem đường lượn sóng chữ S / vòi kem hình ngôi sao (@yuhtt09 #52, #54) "
                "hoặc Biến hình từ đồ ngủ Pijama che ống kính sang váy công chúa khui hộp quà mỹ phẩm (@meshinthuine #04 - 13.5% Like Rate)!"
            ),
            "bespoke_asmr_trigger": (
                "Tiếng vặn mở nắp (`sfx_kien_remove_bottle_cap_unscrew.wav`), tiếng kéo sợi bọt tơ tằm (`sfx_kien_cheese_pull_mucus_necha_mlem.wav`), "
                "tiếng chạm da đàn hồi (`sfx_kien_poyo_kawaii_skin_touch_bounce.wav`) & tiếng lấp lánh sau khi skincare xong (`sfx_kien_kirarin_glitter_skincare_done.wav`)!"
            ),
            "creative_hook_options": [
                "Hook 1 (Xếp Chồng 3 Bình Luận + Kéo Bọt Tơ Tằm Vẽ Trái Tim - @3thag8_ 2.44M views): Ghim 3 comment thật liên tiếp trong khi kéo bọt xà phòng dày đặc phủ kín cẳng tay rồi dùng ngón tay vẽ hình trái tim lên bọt",
                "Hook 2 (So Sánh Giá Lẻ ❌ vs Combo 6 Món ✅ - @yuhtt09 #51): '❌ Lẻ cushion gần 300 🐣 | ✅ Combo 6 món hơn 300 🐣' thả từng món quà xuống bàn",
                "Hook 3 (Che Ống Kính Biến Hình Pijama -> Glam - @meshinthuine #04): Mặc đồ ngủ ôm hộp quà -> Đưa tay áo che camera ở 1.4s -> Hiện ra diện mạo lung linh mở hộp lâu đài"
            ],
            "tailored_physics_props": [
                "Nếu là Xà phòng / Sữa rửa mặt / Sữa tắm (@3thag8_ 2.44M views): Bỏ bánh xà phòng vào lưới tạo bọt, vò cho bọt đặc quánh rồi kéo sợi tơ tằm giữa 2 bàn tay + Phủ bọt trắng kín cánh tay và dùng ngón trỏ VẼ HÌNH TRÁI TIM LÊN BỌT!",
                "Bài Test Xịt Nước + Áp Khăn Giấy Khô Không Lem (@yuhtt09 #03, #06, #14): Sau khi tán kem chống nắng/cushion/son lên mu bàn tay, xịt/đổ nước trực tiếp lên cho đọng giọt rồi dùng tờ KHĂN GIẤY TRẮNG KHÔ ấn mạnh xuống và giơ tờ giấy trắng tinh lên chứng minh không trôi!",
                "Bài Test 5 Ô Giấy Thấm Dầu Xanh (@yuhtt09 #54): Cắt 5 mảnh giấy thấm dầu xanh dương nhỏ đặt lên vùng da vừa thoa kem rồi lật lại chứng minh ráo mịn không bóng dầu!",
                "Nếu là Kem duỗi tóc / Ủ tóc (@3thag8_ #06): Bóp cò cho kem trắng trào qua răng lược xanh ở 0.0s rồi chải trực tiếp lên lọn tóc thật!"
            ],
            "tailored_lighting_and_wardrobe": (
                "Studio High-Key Airy Douyin White (@yuhtt09 YAVG ~166) hoặc Bàn Pegboard đèn kép (@3thag8_) + "
                "Bật Bộ lọc CapCut 'Trong như pha lê (Crystal Clear)' ở mức 44% (@kieneditcuong #12) giúp da tay POV trắng hồng không lộ khuyết điểm."
            ),
            "audio_and_bgm_blueprint": {
                "recommended_bgm_key": "bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm",
                "bgm_style_note": "Nhạc Sped-up K-Pop Pluck 130 BPM (@yuhtt09) hoặc Kawaii Lo-Fi R&B 116 BPM kết hợp trọn bộ 6 SFX Skincare của @kieneditcuong (#05)",
                "recommended_sfx_keys": [
                    "sfx_kien_remove_bottle_cap_unscrew",
                    "sfx_kien_poyo_kawaii_skin_touch_bounce",
                    "sfx_kien_kirarin_glitter_skincare_done",
                    "sfx_kien_cheese_pull_mucus_necha_mlem",
                    "screen_seal_peel_smooth",
                    "water_pour_splash_test",
                    "bell_ding_cta"
                ]
            },
            "auto_edit_effects_to_trigger": [
                "YUHTT09_COMBO_PRICE_STACK_OR_3IN1_BADGE",
                "YUHTT09_WATER_TISSUE_BLOT_PROOF_CALLOUT",
                "KIEN_POV_SKIN_CRYSTAL_FILTER_44",
                "GRAYUNBOX_OUTDOOR_SKIN_PIP",
                "3THAG8_CHR_SKINCARE_SHIELD"
            ]
        })

    return strategy


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
    và dữ liệu Auto-Update mới nhất từ Bộ Nhớ Tự Học (Hội tụ tinh hoa 6 KOC Master)!
    """
    rec_vibe = profile.get("recommended_vibe", "V0")
    smart_strat = profile.get("smart_contextual_strategy", {})
    fusion_summary = smart_strat.get("primary_koc_fusion", "@meshinthuine + @byraanni + @grayunbox")
    vibe_options = [
        {
            "code": "V0",
            "label": f"AI Tự Động Phối Trộn Thông Minh Tinh Hoa 8 KOC Theo Đúng Đặc Tính Sản Phẩm ({fusion_summary} - Chọn đúng Icon {smart_strat.get('semantic_icon_family', '✨')}, Nhạc nền & Hiệu ứng chuẩn ngữ cảnh)"
        },
        {
            "code": "V1",
            "label": "KOC Trải Nghiệm Đời Thường & Giải Quyết Nỗi Đau (Chuẩn @meshinthuine - Khen 8 Chê 2, Tỷ lệ chốt đơn GPM cao nhất)"
        },
        {
            "code": "V2",
            "label": "Tạp Chí Kinfolk / Pinterest Editorial & Kính Lúp Nét Đứt 162% (Chuẩn @byraanni - Mở đầu Collage 3x1.1s, Chữ Kép + Áo Len Nâu Espresso trên Bàn Trắng)"
        },
        {
            "code": "V3",
            "label": "Thử Thách Vật Lý Thực Chiến + Lá Chắn CHR/OCR (Chuẩn @3thag8_ - Test ngâm nước/xé giấy ướt/bóp tràn dưỡng chất + Vòng lặp Radial Blur)"
        },
        {
            "code": "V4",
            "label": "Kỹ Xảo Thị Giác 3s Đầu & 6 Keyframe Zoom Đọc Nhãn (Chuẩn @kieneditcuong - Tô viền phát quang, Bóng mờ 51%, Zoom-Hold 1.5s soi thành phần)"
        },
        {
            "code": "V5",
            "label": "Đèn Bàn Ấm Tối Giản & Phản Biện Công Dụng Ngược (Chuẩn @honghanhxinhgai_01 - Màu da HSL hồng mịn, Phụ đề treo y=+0.46 không che tay)"
        },
        {
            "code": "V6",
            "label": "Nắng Rèm Sáo Chiaroscuro, Đạo Cụ Thế Thân POV & Emoji-Rebus (Chuẩn @grayunbox 2.8M views - Rèm sáo + Lò xo Chrome, Manga Freeze-Frame quà tặng, Hạt lá bay 🍃)"
        },
        {
            "code": "V7",
            "label": "Bàn Học Chill Đèn Toast Xanh, Biến Tấu Vị Giác & Camera Sống Trong Khung Hình (Chuẩn @minhtienoiii06 19.3M views - Cắt siêu tốc 1.25s, Hook tranh luận Bịch/Bao ❌✅, Bia nắp thiếc ASMR, Thước đo 1m7 & Emoji giá 🍅/🍠)"
        },
        {
            "code": "V8",
            "label": "Studio Bàn Trắng Pegboard Coquette, Flashback Unbox Không Cần Lời Thoại & Bằng Chứng Đa Ngành (Chuẩn @yuhtt09 8.1M views - 0% Voiceover, 100% ASMR Rạch Hộp/Lột Seal/Xịt Sương + Nhạc Sped-up K-Pop + Chữ Vòm ⌒ Kaomoji 🌷🎀 + So sánh Lẻ ❌/Combo ✅ 🐣 + Test Khăn Giấy Khô/Giấy Thấm Dầu)"
        }
    ]
    # Đưa phương án khuyên dùng lên đầu
    vibe_options.sort(key=lambda x: 0 if x["code"] == rec_vibe else 1)
    vibe_options[0]["label"] = f"(Khuyên dùng cho sản phẩm này) {vibe_options[0]['label']}"

    questions_payload = {
        "product_summary": f"[{profile['detected_archetype']} - {profile['archetype_name']}] {profile['product_description']}",
        "smart_contextual_routing_preview": smart_strat,
        "optical_note": profile["image_optical_analysis"]["lighting_advice"],
        "wardrobe_and_lighting_setup": profile.get("wardrobe_and_lighting_setup", ""),
        "physics_props_to_prepare": profile.get("invisible_to_visible_physics_props", []),
        "chr_pre_warning": profile["chr_forbidden_scenes"],
        "questions_for_user": [
            {
                "id": "Q1_VIDEO_VIBE",
                "question": "Câu 1: Bạn muốn quay video sản phẩm này theo Phong Cách (Vibe) chủ đạo nào (Mặc định V0: AI tự phối trộn thông minh từ 6 KOC)?",
                "options": [f"{o['code']}: {o['label']}" for o in vibe_options]
            },
            {
                "id": "Q2_TALENT_AND_VOICE",
                "question": "Câu 2: Bạn muốn xuất hiện và thu âm theo hình thức nào trong buổi quay này?",
                "options": [
                    "T1: (Khuyên dùng) Lộ mặt nói trực tiếp ở cảnh đầu/cuối + Quay cận cảnh 2 bàn tay thao tác ở cảnh giữa + Thu tiếng ASMR thật",
                    "T2: Không lộ mặt (Chỉ quay góc nhìn thứ nhất POV 2 bàn tay mặc áo len Nâu Espresso thao tác chuẩn @byraanni / @3thag8_) + Thu tiếng ASMR thật",
                    "T3: Quay hình hoàn toàn im lặng nhanh gọn, sau đó giao cho Bộ Edit tự ghép Voiceover và hiệu ứng SFX"
                ]
            },
            {
                "id": "Q3_ENVIRONMENT_AND_PROPS",
                "question": "Câu 3: Bạn đang có sẵn bối cảnh và đạo cụ vật lý nào để mình lên danh sách cảnh quay sát thực tế nhất?",
                "options": [
                    "B1: (Khuyên dùng) Có sẵn đạo cụ vật lý chứng minh công dụng (Cốc nước test chống nước / Giấy ăn + Khói nến test gió / Pha Matcha dốc ngược 180 độ / Mẫu cũ so sánh)",
                    "B2: Mặt bàn tròn trắng mờ + Rèm cửa sổ sáng tự nhiên (Chuẩn Kinfolk @byraanni) hoặc Bảng lỗ Pegboard (@3thag8_)",
                    "B3: Bàn làm việc tối bật 1 đèn bàn vàng ấm rọi từ đỉnh đầu xuống (Chuẩn @honghanhxinhgai_01) hoặc tại nơi sử dụng thực tế"
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
    physics_props = profile.get("invisible_to_visible_physics_props", [])
    physics_prop_hint = physics_props[0] if physics_props else "Thực hiện bài test vật lý chứng minh công dụng thật trước ống kính."

    is_pov_only = (talent_code == "T2") or (vibe_code in ("V2", "V5", "V6", "V8"))
    angle_talking = "A6 (Góc POV mắt người dùng nhìn xuống 2 bàn tay cầm sản phẩm)" if is_pov_only else "A1 (Góc 45 độ ngang ngực KOC cầm sản phẩm)"
    smart_strat = profile.get("smart_contextual_strategy", {})

    # Ánh xạ Phong cách (V0-V8) sang cấu hình tự động cho CapCut Master Injector
    vibe_editor_map = {
        "V0": {
            "koc_persona": f"SMART_AUTO_FUSION ({smart_strat.get('primary_koc_fusion', '8 KOC Master')})",
            "color_grade_preset": "AUTO_CONTEXTUAL",
            "typography_palette": "AUTO_CONTEXTUAL",
            "hook_visual_preset": "AUTO_CONTEXTUAL",
            "subtitle_zone_preference": "AUTO",
            "enable_dashed_loupe_pip": "BYRAANNI_DASHED_LOUPE_162" in smart_strat.get("auto_edit_effects_to_trigger", []),
            "semantic_icon_family": smart_strat.get("semantic_icon_family", "✨ ✦ ✓ 🤍"),
            "auto_edit_effects_to_trigger": smart_strat.get("auto_edit_effects_to_trigger", [])
        },
        "V1": {
            "koc_persona": "@meshinthuine",
            "color_grade_preset": "MESHIN_NATURAL_DAYLIGHT",
            "typography_palette": "COZY_PASTEL_MAMI",
            "hook_visual_preset": "CLEAN_ACTION_ZOOM",
            "subtitle_zone_preference": "AUTO",
            "enable_dashed_loupe_pip": False
        },
        "V2": {
            "koc_persona": "@byraanni",
            "color_grade_preset": "BYRAANNI_KINFOLK_ESPRESSO",
            "typography_palette": "KINFOLK_ESPRESSO_CREAM",
            "hook_visual_preset": "BYRAANNI_3SHOT_COLLAGE",
            "subtitle_zone_preference": "AUTO",
            "enable_dashed_loupe_pip": True
        },
        "V3": {
            "koc_persona": "@3thag8_",
            "color_grade_preset": "3THAG8_PEGBOARD_CLEAN_PINK",
            "typography_palette": "PEGBOARD_ROSE_GOLD",
            "hook_visual_preset": "CLEAN_ACTION_ZOOM",
            "subtitle_zone_preference": "AUTO",
            "enable_dashed_loupe_pip": True
        },
        "V4": {
            "koc_persona": "@kieneditcuong",
            "color_grade_preset": "3THAG8_PEGBOARD_CLEAN_PINK",
            "typography_palette": "TECH_SLEEK_HUD",
            "hook_visual_preset": "KIEN_GLOW_STROKE_FREEZE",
            "subtitle_zone_preference": "AUTO",
            "enable_dashed_loupe_pip": True
        },
        "V5": {
            "koc_persona": "@honghanhxinhgai_01",
            "color_grade_preset": "HONGHANH_WARM_DESK_LAMP",
            "typography_palette": "LUXURY_EDITORIAL",
            "hook_visual_preset": "KIEN_GHOST_OPACITY_51",
            "subtitle_zone_preference": "UPPER_MIDDLE_HONGHANH",
            "enable_dashed_loupe_pip": False
        },
        "V6": {
            "koc_persona": "@grayunbox",
            "color_grade_preset": "GRAYUNBOX_VENETIAN_BLINDS_CHIAROSCURO",
            "typography_palette": "GRAYUNBOX_CLEAN_MINIMAL",
            "hook_visual_preset": "BYRAANNI_3SHOT_COLLAGE",
            "subtitle_zone_preference": "UPPER_THIRD_GRAYUNBOX",
            "enable_dashed_loupe_pip": True
        },
        "V7": {
            "koc_persona": "@minhtienoiii06",
            "color_grade_preset": "MINHTIENOIII_COZY_TOAST_LAMP_SENSORY",
            "typography_palette": "MINHTIENOIII_GENZ_SENSORY_POP",
            "hook_visual_preset": "CLEAN_ACTION_ZOOM",
            "subtitle_zone_preference": "UPPER_THIRD_GRAYUNBOX",
            "enable_dashed_loupe_pip": True
        },
        "V8": {
            "koc_persona": "@yuhtt09",
            "color_grade_preset": "YUHTT09_HIGHKEY_AIRY_DOUYIN_WHITE",
            "typography_palette": "YUHTT09_COQUETTE_CLEAN_WHITE_PILL",
            "hook_visual_preset": "CLEAN_ACTION_ZOOM",
            "subtitle_zone_preference": "LOWER_MIDDLE_YUHTT09",
            "enable_dashed_loupe_pip": True
        }
    }
    editor_cfg = vibe_editor_map.get(vibe_code, vibe_editor_map["V0"])

    hook_action_desc = (
        f"Quay Tổ Hợp 3 Cảnh Collage liên tiếp (mỗi cảnh 2 giây để AI cắt lấy đúng 1.1s x 3 = 3.3s chuẩn @byraanni): "
        f"(1) Cầm/dùng sản phẩm thực tế -> (2) Đặt sản phẩm lên khay nhìn từ đỉnh 90 độ (A4 Flatlay) -> (3) Tay mở lớp giấy nến/hộp gói. "
        f"Hoặc thực hiện ngay: {profile['visual_aha_hook']}."
        if vibe_code == "V2"
        else (
            f"Thực hiện ngay hành động đắt giá nhất của sản phẩm: {profile['visual_aha_hook']}. "
            "LƯU Ý QUAN TRỌNG: Bắt đầu bấm máy trước 1 giây rồi mới đưa tay chuyển động dứt khoát vào giữa khung hình!"
        )
    )

    shots_blueprint: List[Dict[str, Any]] = [
        {
            "clip_slot_id": "RAW_01_HOOK",
            "order": 1,
            "scene_name": "CẢNH 1: MÓC CÂU THỊ GIÁC & COLLAGE TẠP CHÍ 3.3s (VISUAL HOOK)",
            "timeline_window_sec": "0.0s -> 3.3s" if vibe_code == "V2" else f"0.0s -> {trend['target_hook_dur_sec']}s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 5 - 6 giây (AI sẽ tự cắt lấy 1.5s hoặc 3 cảnh 1.1s đắt giá nhất)",
            "camera_angle_code": "A1 -> A4 -> A2 (Tổ hợp 3 góc Collage @byraanni)" if vibe_code == "V2" else ("A2 (Macro Cận Cảnh 15-20cm)" if vibe_code != "V3" else "A7 (Cận Cảnh Kết Quả Thực Chiến)"),
            "action_to_perform": hook_action_desc,
            "why_edit_engine_needs_this": (
                "Giúp thuật toán `trim_cutting_on_action()` bắt đúng đỉnh vận tốc chuyển động tay, "
                "đồng thời kích hoạt `build_editorial_dual_font_title_cluster()` (Chữ Kép Tạp Chí + Vòng Cung Sao `✧ ⁀➴ ✦` + Nhãn Thông Số Đối Xứng)!"
            ),
            "framing_and_text_safe_zone": (
                "Giữ sản phẩm nằm gọn ở vùng Trung Tâm (từ 35% đến 65% chiều dọc màn hình). "
                "Chừa trống 1/3 phía trên để Mắt xích 5 đặt Cụm Tiêu Đề Kép và hai bên Trái/Phải (`x = ±0.42`) cho nhãn thông số bay!"
            ),
            "suggested_voice_line": "Khoan lướt qua nếu mọi người vẫn đang đau đầu tìm một món vừa chuẩn vừa đáng tiền như thế này nhé..."
        },
        {
            "clip_slot_id": "RAW_02_PAIN_CONTEXT",
            "order": 2,
            "scene_name": "CẢNH 2: NỖI ĐAU THỰC TẾ / SOI TEM NHÃN ZOOM-HOLD 4 KEYFRAMES (CONTEXT & SPEC)",
            "timeline_window_sec": f"{trend['target_hook_dur_sec']}s -> 6.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 6 - 8 giây (AI sẽ lọc lấy 4.0s)",
            "camera_angle_code": angle_talking,
            "action_to_perform": (
                "Đưa sản phẩm ra giữa khung hình, giữ yên mặt tem nhãn/thành phần trước ống kính đúng 2 giây "
                "(để AI tự động áp dụng công thức `ZOOM_HOLD_READ_LABEL_4KF` của @kieneditcuong: Phóng to 148% -> Giữ yên 1.5s cho khách đọc chữ -> Thu về 100%), "
                "sau đó xoay nhẹ sản phẩm từ mặt bên sang mặt chính diện."
            ),
            "why_edit_engine_needs_this": (
                "Kích hoạt Keyframe 4 điểm `create_6_archetype_zoom_keyframes('ZOOM_HOLD_READ_LABEL_4KF')` "
                "kèm hiệu ứng âm thanh `whoosh_in + soft_pop` lôi cuốn mắt người xem."
            ),
            "framing_and_text_safe_zone": "Đặt chủ thể cao hơn đáy màn hình ít nhất 30% để né vùng Phụ đề.",
            "suggested_voice_line": "Trước giờ dùng mấy loại cũ cứ bị bất tiện mãi, cho đến khi mình đổi sang em này thì đúng là chân ái."
        },
        {
            "clip_slot_id": "RAW_03_NATIVE_ASMR_AND_LOUPE",
            "order": 3,
            "scene_name": "CẢNH 3: THU TIẾNG ASMR THẬT + SOI KÍNH LÚP TRÒN NÉT ĐỨT 162% (@byraanni LOUPE)",
            "timeline_window_sec": "6.0s -> 11.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 7 - 10 giây (AI sẽ lọc lấy 5.0s)",
            "camera_angle_code": "A4 (Top-Down 90 độ từ trên xuống bàn trắng) hoặc A2 (Macro nghiêng 30 độ)",
            "action_to_perform": (
                f"Đưa sản phẩm lại gần mic điện thoại khoảng 15cm. Thực hiện: {profile['native_asmr_trigger']}. "
                "ĐẶC BIỆT: Giữ ngón tay chỉ vào nút bấm / cổng sạc / chi tiết nhỏ trong 2.5 giây để Bộ Edit tự động bật "
                "`Kính Lúp Hình Tròn Viền Nét Đứt 162% (inject_dashed_circle_magnifier_pip)` chuẩn @byraanni! "
                "⚠️ BẮT BUỘC: Ngừng nói hoàn toàn trong 2.5 giây phát ra tiếng động ASMR!"
            ),
            "why_edit_engine_needs_this": (
                "Để `evaluate_and_route_native_clip_audio()` giữ 100% tiếng ASMR thật (`Crest Factor >= 11.5dB`) "
                "và để `inject_dashed_circle_magnifier_pip()` tạo mặt nạ tròn `1.62x` trên Track V2 kèm nhãn `● chi tiết`!"
            ),
            "framing_and_text_safe_zone": profile["image_optical_analysis"]["lighting_advice"],
            "suggested_voice_line": "(Im lặng 2 giây đầu để thu tiếng ASMR thật)... Nghe cái tiếng với nhìn từng chi tiết nhỏ thôi là biết hàng xịn rồi."
        },
        {
            "clip_slot_id": "RAW_04_ONETAKE_PHYSICS_PROOF",
            "order": 4,
            "scene_name": "CẢNH 4: TEST ĐẠO CỤ VẬT LÝ LIỀN MẠCH (INVISIBLE-TO-VISIBLE ONE-TAKE PROOF)",
            "timeline_window_sec": "11.0s -> 19.0s",
            "recommended_record_duration_sec": "Bấm máy quay LIỀN MẠCH 10 - 15 giây KHÔNG TẮT MÁY GIỮA CHỪNG",
            "camera_angle_code": "A3 (Góc cố định One-Take chứng minh hiệu quả vật lý thật)",
            "action_to_perform": (
                f"Thực hiện bài test vật lý đắt giá nhất trong 1 cú bấm máy liên tục: {physics_prop_hint} "
                "Tuyệt đối không bấm dừng máy ở giữa!"
            ),
            "why_edit_engine_needs_this": (
                "Biến công dụng vô hình thành bằng chứng thị giác không thể chối cãi (học từ @byraanni & @3thag8_), "
                "đồng thời bảo vệ kênh tuyệt đối khỏi lỗi `CHR -10đ đến -20đ (Cắt ghép kết quả giả)`."
            ),
            "framing_and_text_safe_zone": "Giữ nguyên vị trí máy quay cố định để AI tự động tua nhanh Speed Ramp 2.5x đoạn chờ ở giữa.",
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
            "scene_name": "CẢNH 6: KẾT QUẢ CUỐI & VÒNG LẶP VÔ TẬN RADIAL BLUR (SEAMLESS LOOP CTA)",
            "timeline_window_sec": "23.5s -> 28.0s",
            "recommended_record_duration_sec": "Bấm máy quay khoảng 5 - 6 giây (AI lọc lấy 4.5s)",
            "camera_angle_code": angle_talking,
            "action_to_perform": (
                "Tay phải cầm sản phẩm ngang ngực, TAY TRÁI CHỈ DỨT KHOÁT XUỐNG GÓC DƯỚI BÊN TRÁI MÀN HÌNH "
                "(đúng vị trí gắn Thẻ Giỏ Hàng Vàng TikTok Shop) trong 2 giây cuối cùng."
            ),
            "why_edit_engine_needs_this": (
                "Kích hoạt `inject_3s_visual_hook_and_radial_loop_outro()` tự động gắn chuyển cảnh `RADIAL_BLUR` + "
                "`MATCH_SCALE_TRANSITION (1.0x -> 1.36x)` ở 0.3s cuối cùng (chuẩn @3thag8_ & @byraanni) để cuốn người xem lặp lại Cảnh 1!"
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
        "setup_guide_before_filming": {
            "wardrobe_and_lighting": profile.get("wardrobe_and_lighting_setup", ""),
            "physics_props_checklist": physics_props,
            "creative_hook_options": smart_strat.get("creative_hook_options", []),
            "audio_and_bgm_blueprint": smart_strat.get("audio_and_bgm_blueprint", {}),
            "camera_settings_mandate": "Quay ở 1080p hoặc 4K 60fps, khóa lấy nét & phơi sáng (AE/AF Lock) vào đúng sản phẩm trước khi bấm máy."
        },
        "selected_style": {
            "vibe_code": vibe_code,
            "talent_code": talent_code,
            "props_code": props_code,
            "koc_persona_reference": editor_cfg["koc_persona"],
            "color_grade_preset_locked": editor_cfg["color_grade_preset"],
            "typography_palette_locked": editor_cfg["typography_palette"],
            "hook_visual_preset_locked": editor_cfg["hook_visual_preset"],
            "subtitle_zone_preference": editor_cfg["subtitle_zone_preference"],
            "enable_dashed_loupe_pip": editor_cfg["enable_dashed_loupe_pip"],
            "enable_chr_shield_and_ocr_evasion": True,
            "enable_radial_blur_loop_outro": True,
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
