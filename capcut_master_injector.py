#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAPCUT PRO FULL-FEATURE DRAFT INJECTOR (macOS)
Tích hợp đầy đủ Resource IDs từ pyCapCut / VectCutAPI cho phong cách Reviewer meshinthuine.
"""

import os
import re
import json
import uuid
import time
import shutil
import subprocess
from typing import List, Dict, Optional, Tuple

CAPCUT_DRAFTS_ROOT = os.path.expanduser(
    "~/Movies/CapCut/User Data/Projects/com.lveditor.draft"
)

def uid() -> str:
    return str(uuid.uuid4()).upper()

def sec_to_us(sec: float) -> int:
    return int(round(float(sec) * 1_000_000))

# ==============================================================================
# 1. TỪ ĐIỂN RESOURCE ID & EFFECT ID CHÍNH THỨC CỦA CAPCUT QUỐC TẾ
# ==============================================================================

CAPCUT_TRANSITIONS = {
    "PULL_IN":           {"name": "Pull in",           "resource_id": "6724226861666144779", "effect_id": "E27206B3-FFA0-4ea4-B6E7-44350CED4574", "is_overlap": True,  "dur": 250000},
    "PULL_OUT":          {"name": "Pull Out",          "resource_id": "6724226338418332167", "effect_id": "39411271-04D8-40f1-9DF9-1E0A7DA5CF64", "is_overlap": True,  "dur": 250000},
    "HORIZONTAL_BLUR":   {"name": "Horizontal Blur",   "resource_id": "7451535587812594193", "effect_id": "63C1D344-D734-4945-A2D8-867AE7559ABC", "is_overlap": True,  "dur": 250000},
    "RADIAL_BLUR":       {"name": "Radial Blur",       "resource_id": "7215489792597824001", "effect_id": "53E34B82-8CA8-483f-BBE9-EB36EFD0EE1B", "is_overlap": True,  "dur": 250000},
    "DISSOLVE":          {"name": "Dissolve",          "resource_id": "6724846004274729480", "effect_id": "392FD26E-A514-4d0f-8950-EA4A20CB407C", "is_overlap": True,  "dur": 200000},
    "SLIDE":             {"name": "Slide",             "resource_id": "6757982416649851399", "effect_id": "AF0D3666-48D3-4ff0-B836-EB93B174A74A", "is_overlap": True,  "dur": 250000},
    "LEFT":              {"name": "Left",              "resource_id": "6726711499676455435", "effect_id": "9CA0C177-8A1D-410c-9D37-7F6606CD5BB5", "is_overlap": True,  "dur": 250000},
    "RIGHT":             {"name": "Right",             "resource_id": "6724227599616184836", "effect_id": "C3D52822-B616-4e73-9588-AAED851B6CF9", "is_overlap": True,  "dur": 250000},
    "FLASH":             {"name": "Flash",             "resource_id": "6987208055511323137", "effect_id": "15F94905-7A39-4789-8285-92188260756B", "is_overlap": True,  "dur": 150000},
    "BLURRED_HIGHLIGHT": {"name": "Blurred Highlight", "resource_id": "7134999483762348545", "effect_id": "A1C6E234-BAE9-4de6-B659-528933BABFE2", "is_overlap": True,  "dur": 300000},
    "MIX":               {"name": "Mix",               "resource_id": "6724845717472416269", "effect_id": "CE454E9E-9C57-43c5-9E80-B46A6A495D10", "is_overlap": True,  "dur": 200000},
    "GLITCH":            {"name": "Glitch",            "resource_id": "6724844028213596680", "effect_id": "479CE76F-FB0C-435e-AA12-49EE0C5FBCCF", "is_overlap": False, "dur": 150000},
}

CAPCUT_TEXT_ANIMS = {
    "SPRING":      {"title": "Spring",                "resource_id": "6887766363436225025", "type": "in",   "dur": 200000},
    "POP_UP":      {"title": "Pop Up",                "resource_id": "7145435451946439170", "type": "in",   "dur": 200000},
    "BOUNCE_IN":   {"title": "Bounce In",             "resource_id": "6887766069587481090", "type": "in",   "dur": 250000},
    "ELASTIC_II":  {"title": "Elastic Telescopic II", "resource_id": "7161336180561154562", "type": "in",   "dur": 250000},
    "TYPEWRITER":  {"title": "Typewriter",            "resource_id": "7210980292243231233", "type": "in",   "dur": 400000},
    "KARAOKE":     {"title": "Karaoke",               "resource_id": "6771294855785091588", "type": "in",   "dur": 500000},
    "BOUNCE_OUT":  {"title": "Bounce Out",            "resource_id": "6887765964515971585", "type": "out",  "dur": 150000},
    "FADE_OUT":    {"title": "Fade Out",              "resource_id": "6724919382104871427", "type": "out",  "dur": 150000},
    "JUMP":        {"title": "Jump",                  "resource_id": "6724920002958332420", "type": "loop", "dur": 600000},
    "JIGGLE":      {"title": "Jiggle",                "resource_id": "6887766216576864770", "type": "loop", "dur": 600000},
    "FLARE":       {"title": "Flare",                 "resource_id": "7128311749186425346", "type": "loop", "dur": 800000},
}

CAPCUT_VIDEO_ANIMS = {
    "MINI_ZOOM":      {"title": "Mini Zoom",          "resource_id": "6800268825611735559", "type": "in",    "dur": 250000},
    "SLIDE_UP":       {"title": "Slide Up",           "resource_id": "6798333487523828238", "type": "in",    "dur": 250000},
    "SLIDE_LEFT":     {"title": "Slide Left",         "resource_id": "6798332871267324423", "type": "in",    "dur": 250000},
    "SHAKE_1":        {"title": "Shake 1",            "resource_id": "6739418227031413256", "type": "in",    "dur": 250000},
    "WIPER":          {"title": "Wiper",              "resource_id": "6802871256849846791", "type": "in",    "dur": 300000},
    "CARD_3D_2":      {"title": "3D card 2",          "resource_id": "6836319649844433415", "type": "group", "dur": 2000000},
    "ENLARGE_BOUNCE": {"title": "Enlarge and bounce", "resource_id": "7032223659116728833", "type": "group", "dur": 2000000},
    "PENDULUM_1":     {"title": "Pendulum 1",         "resource_id": "6811007755785081357", "type": "group", "dur": 2000000},
}

CAPCUT_SCENE_EFFECTS = {
    "CAMERA_FOCUS": {"name": "Camera Focus",    "resource_id": "6719658716750156291", "effect_id": "15206267"},
    "BLURRY_FOCUS": {"name": "Blurry Focus",    "resource_id": "6758752103092457991", "effect_id": "15206250"},
    "EDGE_GLOW":    {"name": "Edge Glow",       "resource_id": "6769065553207235086", "effect_id": "15206415"},
    "GLOWBURST":    {"name": "Glowburst",       "resource_id": "6753169731617821191", "effect_id": "15206859"},
    "BLURAY_SCAN":  {"name": "Bluray Scanning", "resource_id": "7255269076526699010", "effect_id": "51063477"},
    "CAMERA_SHAKE": {"name": "Camera Shake",    "resource_id": "6863326875649839623", "effect_id": "15206571"},
}

CAPCUT_MASKS = {
    "SPLIT":     {"name": "Split",     "resource_type": "line",      "resource_id": "7374020197990011409"},
    "CIRCLE":    {"name": "Circle",    "resource_type": "circle",    "resource_id": "7374021188315517456"},
    "RECTANGLE": {"name": "Rectangle", "resource_type": "rectangle", "resource_id": "7374021450748924432"},
}

# ==============================================================================
# 2. KHO ÂM THANH 3 NGUỒN LAI (3-TIER HYBRID VIRAL SFX VAULT) & THẨM ĐỊNH ASMR GỐC
# ==============================================================================

def ensure_studio_sfx_pack(sfx_dir: str) -> Dict[str, str]:
    """
    [TẦNG 3 - BỘ TỔNG HỢP 17 SOUND EFFECTS ĐỘNG HỌC, UI & FOLEY VẬT LÝ BẰNG FFMPEG]:
    Đảm bảo thư mục sfx_dir luôn có đủ 17 file Sound Effects chuẩn Studio & Viral Review
    (bao gồm cả âm thanh động học khi Đưa đồ ra/vào, Nhảy biến hình, Đổi vị trí, Chốt đơn).
    """
    os.makedirs(sfx_dir, exist_ok=True)
    sfx_recipes = {
        # Nhóm 1: UI & Text Callout
        "soft_pop":      "sine=frequency=520:duration=0.09,afade=t=in:ss=0:d=0.01,afade=t=out:st=0.03:d=0.06,asetrate=44100*1.3,aresample=44100",
        "bubble_pop":    "sine=frequency=380:duration=0.11,aecho=0.8:0.88:25:0.4,afade=t=out:st=0.04:d=0.07",
        "sparkle_ding":  "sine=frequency=1760:duration=0.45,aecho=0.8:0.85:55:0.5,afade=t=in:ss=0:d=0.01,afade=t=out:st=0.10:d=0.35",
        # Nhóm 2: Âm thanh Động học Không gian (Kinetic Movement SFX: Đưa vào/ra, Nhảy, Đổi vị trí, Chốt giỏ hàng)
        "light_swish":   "anoisesrc=d=0.18:c=pink:r=44100:a=0.4,bandpass=f=1600:width_type=h:w=1200,afade=t=in:ss=0:d=0.06,afade=t=out:st=0.06:d=0.12",
        "whoosh_in":     "anoisesrc=d=0.22:c=pink:r=44100:a=0.52,bandpass=f=950:width_type=h:w=700,afade=t=in:ss=0:d=0.08,afade=t=out:st=0.09:d=0.13",
        "whoosh_out":    "anoisesrc=d=0.16:c=pink:r=44100:a=0.48,bandpass=f=2100:width_type=h:w=1400,afade=t=in:ss=0:d=0.03,afade=t=out:st=0.05:d=0.11",
        "whip_swish":    "anoisesrc=d=0.14:c=white:r=44100:a=0.55,bandpass=f=2600:width_type=h:w=1800,afade=t=in:ss=0:d=0.02,afade=t=out:st=0.04:d=0.10",
        "jump_boing":    "sine=frequency=240:duration=0.26,vibrato=f=14:d=0.8,asetrate=44100*1.45,aresample=44100,afade=t=in:ss=0:d=0.01,afade=t=out:st=0.08:d=0.18",
        "teleport_poof": "anoisesrc=d=0.19:c=brown:r=44100:a=0.60,bandpass=f=750:width_type=h:w=550,aecho=0.8:0.85:35:0.35,afade=t=out:st=0.05:d=0.14",
        "cash_chime":    "sine=frequency=2093:duration=0.38,aecho=0.8:0.9:45:0.55,afade=t=in:ss=0:d=0.008,afade=t=out:st=0.08:d=0.30",
        "subtle_bonk":   "sine=frequency=165:duration=0.14,afade=t=in:ss=0:d=0.005,afade=t=out:st=0.03:d=0.11",
        # Nhóm 3: Foley Vật lý Thay thế (Khi âm gốc video bị ồn)
        "mech_click":    "anoisesrc=d=0.04:c=white:r=44100:a=0.65,highpass=f=1800,afade=t=out:st=0.008:d=0.032",
        "shutter":       "anoisesrc=d=0.08:c=white:r=44100:a=0.5,bandpass=f=2400:width_type=h:w=1600,afade=t=out:st=0.02:d=0.06",
        "box_rip":       "anoisesrc=d=0.28:c=brown:r=44100:a=0.55,bandpass=f=1100:width_type=h:w=900,afade=t=in:ss=0:d=0.04,afade=t=out:st=0.12:d=0.16",
        "spray_mist":    "anoisesrc=d=0.35:c=white:r=44100:a=0.45,highpass=f=3200,afade=t=in:ss=0:d=0.03,afade=t=out:st=0.15:d=0.20",
        "fabric_soft":   "anoisesrc=d=0.25:c=pink:r=44100:a=0.35,bandpass=f=900:width_type=h:w=600,afade=t=in:ss=0:d=0.05,afade=t=out:st=0.10:d=0.15",
        "crisp_crunch":  "anoisesrc=d=0.14:c=white:r=44100:a=0.60,bandpass=f=2100:width_type=h:w=1500,aecho=0.7:0.7:18:0.3,afade=t=out:st=0.04:d=0.10"
    }
    paths = {}
    for name, lavfi_filter in sfx_recipes.items():
        out_path = os.path.join(sfx_dir, f"{name}.wav")
        if not os.path.exists(out_path):
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", lavfi_filter, out_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        paths[name] = os.path.abspath(out_path)
    return paths

def discover_and_index_hybrid_sfx_vault(
    studio_sfx_dir: str = "./workspace/sfx_studio",
    user_viral_sfx_dir: str = "./assets/user_viral_sfx"
) -> Dict[str, str]:
    """
    [KHO ÂM THANH 3 TẦNG LAI (3-TIER HYBRID VIRAL SFX VAULT)]:
    Kết hợp thông minh 3 nguồn âm thanh theo thứ tự ưu tiên từ cao xuống thấp:
    - TẦNG 1 (Ưu tiên số 1): Bộ âm thanh Viral/Trend do chính người dùng sưu tầm trong `./assets/user_viral_sfx/`
      (Hỗ trợ cả file .mp3/.wav/.m4a VÀ tự động tách tiếng nếu người dùng bỏ file video .mp4/.mov vào!).
    - TẦNG 2 (Ưu tiên số 2): Kho âm thanh đã tải/yêu thích trong Cache của CapCut Desktop
      (`~/Movies/CapCut/User Data/Cache/music/`).
    - TẦNG 3 (Bảo hiểm 100%): Bộ 17 âm thanh Động học & Foley chuẩn Studio tự sinh bằng FFmpeg.
    """
    vault = ensure_studio_sfx_pack(studio_sfx_dir)

    # Từ khóa ánh xạ tự động tên file tiếng Việt / tiếng Anh trong bộ sưu tầm của người dùng vào đúng hành động
    keyword_aliases = {
        "whoosh_in":     ["whoosh_in", "dua_vao", "vut_vao", "swoosh_in", "push_in", "vut_am"],
        "whoosh_out":    ["whoosh_out", "dua_ra", "gat_ra", "vut_ra", "pull_out", "swipe"],
        "whip_swish":    ["whip", "doi_vi_tri", "swap", "doi_cho", "lia_nhanh", "swish"],
        "jump_boing":    ["jump", "boing", "nhay", "lo_xo", "spring", "bat_nhay"],
        "teleport_poof": ["teleport", "poof", "bien_hinh", "bung_tay", "snap_change", "magic"],
        "soft_pop":      ["soft_pop", "pop", "bup", " moc_chu", "plop"],
        "bubble_pop":    ["bubble", "bong_bong", "nuoc", "water_drop", "giot_nuoc"],
        "sparkle_ding":  ["sparkle", "bling", "lap_lanh", "twinkle", "shine", "sang_bong", "ting"],
        "cash_chime":    ["cash", "chot_don", "gio_hang", "coin", "ting_ting", "ka_ching", "money"],
        "subtle_bonk":   ["bonk", "fail", "loi", "tut_mood", "quac", "meme_fail", "slide_down"],
        "mech_click":    ["click", "tach", "bam_nut", "switch", "nam_cham", "clack"],
        "shutter":       ["shutter", "chup_anh", "camera"],
        "box_rip":       ["unbox", "rach_hop", "xe_tui", "rip", "mo_hop"],
        "spray_mist":    ["spray", "xit", "suong", "foam"],
        "fabric_soft":   ["fabric", "vai", "so_vai", "rustle"],
        "crisp_crunch":  ["crunch", "gion", "nhai", "bite", "mukbang"]
    }

    # Quét Kho Giải Cứu CapCut (`01_capcut_rescued_assets`) và Sổ Đăng Ký Riêng Ngoài CapCut (`external_custom_sfx_registry.json`)
    capcut_cache_dir = os.path.expanduser("~/Movies/CapCut/User Data/Cache/music")
    capcut_rescued_dir = "./knowledge_vault/01_capcut_rescued_assets"
    external_sfx_dir = "./knowledge_vault/02_external_sfx_not_in_capcut"
    scan_dirs = [
        d for d in (capcut_cache_dir, capcut_rescued_dir, external_sfx_dir, "./raw_inputs/sfx", user_viral_sfx_dir)
        if os.path.exists(d)
    ]

    for root_dir in scan_dirs:
        for dirpath, _, filenames in os.walk(root_dir):
            for fname in filenames:
                low = fname.lower()
                if not low.endswith((".wav", ".mp3", ".m4a", ".aac", ".ogg")):
                    continue
                full_p = os.path.abspath(os.path.join(dirpath, fname))
                rel_str = os.path.relpath(full_p, root_dir).lower()
                for sfx_key, aliases in keyword_aliases.items():
                    if any(alias in rel_str for alias in aliases):
                        vault[sfx_key] = full_p

    # Nạp trực tiếp từ File Chứa Riêng Các Âm Thanh Ngoài CapCut: ./knowledge_vault/external_custom_sfx_registry.json
    ext_reg_path = "./knowledge_vault/external_custom_sfx_registry.json"
    if os.path.exists(ext_reg_path):
        try:
            with open(ext_reg_path, "r", encoding="utf-8") as f:
                ext_reg = json.load(f)
            for sfx_id, item in ext_reg.get("items", {}).items():
                fp = item.get("file_path", "")
                if fp and os.path.exists(fp):
                    vault[sfx_id] = fp
                    low_id = sfx_id.lower()
                    for sfx_key, aliases in keyword_aliases.items():
                        if sfx_key in low_id or any(a in low_id for a in aliases):
                            vault[sfx_key] = fp
        except Exception:
            pass

    return vault

def evaluate_and_route_native_clip_audio(
    video_path: str, start_sec: float, end_sec: float, action_type: str = "GENERIC_HANDLE"
) -> Dict[str, any]:
    """
    [TRÍ TUỆ ÂM THANH GỐC 3 TẦNG - GIỮ TIẾNG THẬT CỦA SẢN PHẨM HOẶC THAY BẰNG FOLEY SFX]:
    Đo trực tiếp chất lượng âm thanh gốc của đoạn video [start_sec, end_sec]:
    1. KEEP_CLEAN_ASMR: Nếu tiếng sản phẩm rõ, giòn (Crest Factor >= 11dB) và nền yên tĩnh (Noise Floor < -36dB)
       -> Giữ nguyên tiếng thật (native_volume = 0.78), bọc Keyframe âm lượng chỉ mở đúng lúc hành động!
    2. SURGICAL_ISOLATE_AND_LAYER: Nếu có tiếng thật của sản phẩm nhưng hơi nhỏ hoặc phòng hơi ồn nhẹ
       -> Mở cửa sổ âm lượng hẹp 0.35s quanh đỉnh tiếng sản phẩm (native_volume = 0.42) + Bồi thêm Foley SFX nhẹ (0.22)!
    3. MUTE_AND_FOLEY_REPLACE: Nếu nền quá ồn (tiếng quạt, tiếng xe, tiếng nói chuyện tạp) hoặc tiếng sản phẩm quá yếu
       -> Tắt hẳn tiếng gốc (native_volume = 0.0) và tự động chọn Foley SFX khớp với hành động trên hình!
    """
    foley_map = {
        "UNBOX_RIP":    "box_rip",
        "BUTTON_CLICK": "mech_click",
        "MAGNET_SNAP":  "mech_click",
        "SPRAY_CLEAN":  "spray_mist",
        "WATER_BUBBLE": "bubble_pop",
        "FABRIC_TOUCH": "fabric_soft",
        "FOOD_BITE":    "crisp_crunch",
        "RESULT_SHINE": "sparkle_ding",
        "GENERIC_HANDLE": "soft_pop"
    }
    recommended_sfx = foley_map.get(action_type, "soft_pop")
    dur = max(0.5, end_sec - start_sec)

    if not os.path.exists(video_path):
        return {"mode": "MUTE_AND_FOLEY_REPLACE", "native_volume": 0.0, "foley_sfx": recommended_sfx, "foley_vol": 0.32}

    cmd = [
        "ffmpeg", "-ss", str(start_sec), "-t", str(dur), "-i", video_path,
        "-vn", "-af", "highpass=f=140,astats=metadata=1:reset=1,ametadata=print",
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    log = proc.stderr + proc.stdout

    peaks = [float(x) for x in re.findall(r"Peak_level=(-?[0-9.]+)", log) if float(x) > -90.0]
    rms_vals = [float(x) for x in re.findall(r"RMS_level=(-?[0-9.]+)", log) if float(x) > -90.0]

    if not peaks or not rms_vals:
        return {"mode": "MUTE_AND_FOLEY_REPLACE", "native_volume": 0.0, "foley_sfx": recommended_sfx, "foley_vol": 0.32}

    max_peak_db = max(peaks)
    sorted_rms = sorted(rms_vals)
    # Noise Floor là mức âm nền ở 25% khung thời gian yên tĩnh nhất của clip
    noise_floor_db = sorted_rms[max(0, len(sorted_rms) // 4)]
    crest_snr_db = max_peak_db - noise_floor_db

    # Kiểm tra xem có bị tiếng nói chuyện tạp liên tục (75% thời gian đều có RMS cao > -26dB) không
    high_rms_ratio = sum(1 for r in rms_vals if r > -26.0) / float(len(rms_vals))
    has_unwanted_chatter = (high_rms_ratio > 0.65 and crest_snr_db < 9.5)

    if not has_unwanted_chatter and crest_snr_db >= 11.5 and noise_floor_db < -36.0 and max_peak_db > -22.0:
        return {
            "mode": "KEEP_CLEAN_ASMR",
            "native_volume": 0.78,
            "foley_sfx": None,
            "foley_vol": 0.0,
            "measured_snr_db": round(crest_snr_db, 1)
        }
    elif not has_unwanted_chatter and crest_snr_db >= 6.5 and noise_floor_db < -29.0 and max_peak_db > -28.0:
        return {
            "mode": "SURGICAL_ISOLATE_AND_LAYER",
            "native_volume": 0.42,
            "foley_sfx": recommended_sfx,
            "foley_vol": 0.22,
            "measured_snr_db": round(crest_snr_db, 1)
        }
    else:
        return {
            "mode": "MUTE_AND_FOLEY_REPLACE",
            "native_volume": 0.0,
            "foley_sfx": recommended_sfx,
            "foley_vol": 0.34,
            "measured_snr_db": round(crest_snr_db, 1)
        }

def create_surgical_volume_keyframes(peak_offset_us: int, clip_duration_us: int, peak_vol: float = 0.75) -> dict:
    """
    Tạo Keyframe Âm lượng (KFTypeVolume) cô lập đúng khoảnh khắc sản phẩm phát ra tiếng thật:
    Đầu clip volume = 0.0 -> Mở lên peak_vol quanh đỉnh hành động (±220ms) -> Đóng về 0.0!
    """
    win_us = 220000  # 0.22 giây mỗi bên
    t_open = max(0, peak_offset_us - win_us)
    t_close = min(clip_duration_us, peak_offset_us + win_us)
    pts = [
        (0, 0.0),
        (max(0, t_open - 40000), 0.05),
        (peak_offset_us, peak_vol),
        (min(clip_duration_us, t_close + 40000), 0.05),
        (clip_duration_us, 0.0)
    ]
    kf_list = []
    for t_us, val in pts:
        kf_list.append({
            "id": uid(), "time_offset": int(t_us), "values": [float(val)],
            "curveType": "Line", "graphID": "",
            "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}
        })
    return {"id": uid(), "property_type": "KFTypeVolume", "keyframe_list": kf_list}

# ==============================================================================
# 3. BỘ MÁY TYPOGRAPHY SANG TRỌNG, CĂN SIZE TỰ ĐỘNG, PHỐI MÀU THEO NỀN VIDEO & STICKER/BLING ENGINE
# ==============================================================================

CAPCUT_FONTS = {
    "LUXURY":   {"name": "Luxury",               "resource_id": "7291876268541219329", "effect_id": "41472051"},
    "MODERN":   {"name": "Modern",               "resource_id": "6740498577912500749", "effect_id": "349479"},
    "POPPINS":  {"name": "Poppins-Bold",         "resource_id": "7312373689708712449", "effect_id": "41472095"},
    "PLAYFAIR": {"name": "PlayfairDisplay-Bold", "resource_id": "7314592810684912130", "effect_id": "41472127"},
    "NUNITO":   {"name": "Nunito",               "resource_id": "6807743644842332685", "effect_id": "643589"},
    "INTER":    {"name": "Inter-Black",          "resource_id": "7314592567717270018", "effect_id": "37039685"},
}

# 5 Bảng Phối Màu Chữ - Viền - Đổ Bóng - Hộp Nền Sang Trọng Theo Ngành Hàng & Khí Chất Video
LUXURY_TYPOGRAPHY_PALETTES = {
    "LUXURY_EDITORIAL": {
        # Mỹ phẩm cao cấp (P3), Nước hoa, Thời trang thiết kế (P4), Decor (P7)
        "base_hex": "#FAF8F5",       # Trắng Ngọc Trai
        "highlight_hex": "#F3D59B",  # Vàng Champagne Ánh Kim
        "alt_hl_hex": "#F4C2C2",     # Hồng Rose Gold
        "stroke_hex": "#2C221E",     # Nâu Espresso Sẫm (sang hơn đen tuyền)
        "stroke_width": 0.038,       # Viền mảnh tinh tế
        "shadow_hex": "#1A1412",
        "shadow_alpha": 0.58,
        "shadow_diffuse": 0.65,
        "pill_bg_hex": "#2C221E",
        "font_key": "LUXURY",
        "default_sub_anim": "SPRING",
        "bling_icons": ["✦", "✧", "✨", "🤍"]
    },
    "COZY_PASTEL_MAMI": {
        # Mẹ & Bé, Gia đình ấm cúng (P2 - chuẩn meshinthuine)
        "base_hex": "#FFFDF9",       # Trắng Kem Ấm
        "highlight_hex": "#FFE885",  # Vàng Bơ Dịu
        "alt_hl_hex": "#FFB7B2",     # Hồng Đào Pastel
        "stroke_hex": "#3E2723",     # Nâu Cacao Ấm
        "stroke_width": 0.055,
        "shadow_hex": "#2D1A12",
        "shadow_alpha": 0.62,
        "shadow_diffuse": 0.50,
        "pill_bg_hex": "#FFF8E7",    # Hộp nền kem sữa
        "font_key": "NUNITO",
        "default_sub_anim": "SPRING",
        "bling_icons": ["✨", "🫧", "🤍", "🌿"]
    },
    "CLEAN_CRISP_MODERN": {
        # Gia dụng tiện ích & Tẩy rửa (P1)
        "base_hex": "#FFFFFF",       # Trắng Tinh Khiết
        "highlight_hex": "#38EF7D",  # Xanh Ngọc Sạch Bóng
        "alt_hl_hex": "#FFD700",     # Vàng Nắng
        "stroke_hex": "#0F2027",     # Xanh Navy Đậm
        "stroke_width": 0.065,
        "shadow_hex": "#09151A",
        "shadow_alpha": 0.72,
        "shadow_diffuse": 0.40,
        "pill_bg_hex": "#0F2027",
        "font_key": "POPPINS",
        "default_sub_anim": "SPRING",
        "bling_icons": ["✨", "🫧", "✓", "✦"]
    },
    "TECH_SLEEK_HUD": {
        # Phụ kiện Công nghệ, Bàn làm việc, Đồ Ô tô (P5)
        "base_hex": "#F5F7FA",       # Trắng Bạc
        "highlight_hex": "#00F2FE",  # Xanh Cyan Công Nghệ
        "alt_hl_hex": "#FF9F43",     # Cam Amber
        "stroke_hex": "#141E30",     # Xám Đen Kim Loại
        "stroke_width": 0.045,
        "shadow_hex": "#0B101B",
        "shadow_alpha": 0.68,
        "shadow_diffuse": 0.45,
        "pill_bg_hex": "#141E30",    # Kính đen mờ Glassmorphism
        "font_key": "INTER",
        "default_sub_anim": "SPRING",
        "bling_icons": ["⚡", "✦", "✓", "✨"]
    },
    "APPETITE_SAVORY": {
        # Đồ ăn vặt, Trà, Thực phẩm (P6)
        "base_hex": "#FFFDF7",       # Trắng Kem
        "highlight_hex": "#FFC837",  # Vàng Giòn Rụm
        "alt_hl_hex": "#FF8008",     # Cam Mật Ong
        "stroke_hex": "#3B1D0A",     # Nâu Caramel Đậm
        "stroke_width": 0.065,
        "shadow_hex": "#241004",
        "shadow_alpha": 0.70,
        "shadow_diffuse": 0.45,
        "pill_bg_hex": "#3B1D0A",
        "font_key": "POPPINS",
        "default_sub_anim": "SPRING",
        "bling_icons": ["✨", "🔥", "💛", "✦"]
    }
}

def hex_to_rgb_float(hex_str: str) -> List[float]:
    h = hex_str.lstrip("#")
    if len(h) != 6:
        return [1.0, 1.0, 1.0]
    return [round(int(h[i:i+2], 16) / 255.0, 4) for i in (0, 2, 4)]

def rgb_float_to_hex(rgb: Tuple[float, float, float]) -> str:
    r, g, b = [max(0, min(255, int(round(c * 255)))) for c in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"

def extract_dynamic_palette_from_actual_video(
    video_path: str, sample_sec: float = 1.0, mode: str = "TONAL_LUXURY"
) -> Dict[str, any]:
    """
    [TRÍ TUỆ 1 - HÚT MÃ MÀU ĐỘC BẢN TRỰC TIẾP TỪ KHUNG HÌNH VIDEO THỰC TẾ]:
    Không ép cứng theo ngành hàng! Trích xuất trực tiếp màu RGB/HSV thực tế của:
    - Vùng trung tâm Sản phẩm (Subject Hue/Sat)
    - Vùng Bối cảnh nền & Vùng đặt chữ (Ambient Temperature & Luminance)
    Sau đó dùng toán học Vòng tròn màu (HSV Color Harmonics) để sinh mã màu Hex
    cho Chữ chính, Từ khóa nhấn, Viền đồng điệu và Hộp nền kính mờ khớp 100% với video!
    """
    import colorsys
    if not os.path.exists(video_path):
        return dict(LUXURY_TYPOGRAPHY_PALETTES["COZY_PASTEL_MAMI"], bottom_luma_y=128.0, bg_busy_score=10.0)

    # 1. Lấy màu RGB trung bình của vùng Sản phẩm ở giữa (crop=iw*0.4:ih*0.4:iw*0.3:ih*0.3)
    cmd_rgb = [
        "ffmpeg", "-ss", str(sample_sec), "-i", video_path, "-vframes", "1",
        "-vf", "crop=iw*0.4:ih*0.4:iw*0.3:ih*0.3,scale=1:1,format=rgb24",
        "-f", "rawvideo", "-"
    ]
    proc_rgb = subprocess.run(cmd_rgb, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc_rgb.stdout
    if len(raw) >= 3:
        sr, sg, sb = raw[0] / 255.0, raw[1] / 255.0, raw[2] / 255.0
    else:
        sr, sg, sb = 0.85, 0.72, 0.55

    # 2. Đo độ sáng (YAVG) và độ rối chi tiết (YDIF/VREP) của vùng đáy nơi đặt chữ (crop=iw:ih*0.32:0:ih*0.62)
    cmd_bot = [
        "ffmpeg", "-ss", str(sample_sec), "-t", "0.5", "-i", video_path,
        "-vf", "crop=iw:ih*0.32:0:ih*0.62,fps=2,scale=120:-1,signalstats,metadata=print",
        "-an", "-f", "null", "-"
    ]
    proc_bot = subprocess.run(cmd_bot, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    log_b = proc_bot.stderr + proc_bot.stdout
    y_vals = [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", log_b)]
    sat_vals = [float(x) for x in re.findall(r"lavfi\.signalstats\.SATAVG=([0-9.]+)", log_b)]
    bottom_luma_y = (sum(y_vals) / len(y_vals)) if y_vals else 128.0
    bg_busy_score = (sum(sat_vals) / len(sat_vals)) if sat_vals else 25.0

    # 3. Chuyển màu thực tế của sản phẩm/bối cảnh sang hệ HSV để tính bảng màu Hòa âm (Color Harmony)
    h, s, v = colorsys.rgb_to_hsv(sr, sg, sb)
    is_warm_scene = (sr >= sb + 0.04)

    # Màu chữ chính: Trắng Ngọc Trai Ấm (#FFFDF8) nếu video ấm, Trắng Tinh Khiết (#F8FAFC) nếu video lạnh
    base_hex = "#FFFDF8" if is_warm_scene else "#F8FAFC"

    # Màu Từ khóa nhấn (Highlight Hex):
    # - Chế độ TONAL_LUXURY: Giữ đúng góc màu Hue của sản phẩm nhưng nâng độ sáng V=0.96, khóa độ bão hòa S=0.48 (Pastel Champagne sang trọng)
    # - Chế độ POP_CONTRAST (dùng cho câu Hook/Giá tiền): Xoay góc màu 150 độ (Split-Complementary) với S=0.62, V=0.97
    if mode == "POP_CONTRAST":
        hl_h = (h + 0.42) % 1.0
        hl_s = 0.62
    else:
        hl_h = h if s > 0.12 else (0.11 if is_warm_scene else 0.52)
        hl_s = max(0.42, min(0.58, s * 1.15))
    hl_rgb = colorsys.hsv_to_rgb(hl_h, hl_s, 0.96)
    highlight_hex = rgb_float_to_hex(hl_rgb)

    # Màu Viền & Hộp Nền (Stroke & Pill Box):
    # Không dùng màu đen #000000 vô hồn! Lấy chính góc màu Hue của video hạ xuống độ tối sâu V=0.14, S=0.38
    dark_rgb = colorsys.hsv_to_rgb(h, min(0.40, max(0.20, s)), 0.14)
    stroke_hex = rgb_float_to_hex(dark_rgb)
    shadow_rgb = colorsys.hsv_to_rgb(h, min(0.45, max(0.20, s)), 0.08)
    shadow_hex = rgb_float_to_hex(shadow_rgb)

    return {
        "base_hex": base_hex,
        "highlight_hex": highlight_hex,
        "stroke_hex": stroke_hex,
        "stroke_width": 0.042 if bottom_luma_y < 145 else 0.062,
        "shadow_hex": shadow_hex,
        "shadow_alpha": 0.60 if bottom_luma_y < 145 else 0.82,
        "shadow_diffuse": 0.60,
        "pill_bg_hex": stroke_hex,
        "font_key": "LUXURY" if (s < 0.35 and bottom_luma_y > 105) else ("NUNITO" if is_warm_scene else "POPPINS"),
        "bottom_luma_y": round(bottom_luma_y, 1),
        "bg_busy_score": round(bg_busy_score, 1)
    }

def compute_obstacle_free_text_position(
    video_path: str, start_sec: float, dur_sec: float = 1.5, role: str = "SUBTITLE"
) -> Tuple[float, float]:
    """
    [TRÍ TUỆ 2 - ĐỊNH VỊ VỊ TRÍ TEXT ĐỘNG KHÔNG ĐÈ LÊN SẢN PHẨM (OBSTACLE-AWARE POSITIONING)]:
    Phân tích mật độ chuyển động và chi tiết của các vùng trên khung hình dọc 9:16:
    1. Với SUBTITLE: Mặc định ở vùng đáy chuẩn (y = -0.38). Nhưng nếu phát hiện bàn tay và sản phẩm
       đang thao tác sát đáy bàn (vùng đáy có chuyển động mạnh gấp >1.35 lần vùng giữa),
       hệ thống tự động dời Phụ đề lên vùng trống phía trên (y = +0.42 hoặc -0.18) để nhường chỗ cho sản phẩm!
    2. Với CALLOUT & BLING_ACCENT: So sánh mật độ chi tiết giữa nửa Trái và nửa Phải của sản phẩm,
       tự động đặt nhãn vào "Khoảng trống thở" (Negative Space) bên cạnh sản phẩm, tuyệt đối không đè lên giữa sản phẩm!
    """
    if role == "HOOK_BANNER":
        return (0.0, 0.58)
    if role == "CTA":
        return (0.0, -0.42)
    if not os.path.exists(video_path):
        return (0.0, -0.38) if role == "SUBTITLE" else (0.34, 0.16)

    def zone_activity(crop_expr: str) -> float:
        cmd = [
            "ffmpeg", "-ss", str(start_sec), "-t", str(min(1.5, dur_sec)), "-i", video_path,
            "-vf", f"{crop_expr},fps=3,scale=80:-1,signalstats,metadata=print:key=lavfi.signalstats.YDIF",
            "-an", "-f", "null", "-"
        ]
        p = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        vals = [float(x) for x in re.findall(r"lavfi\.signalstats\.YDIF=([0-9.]+)", p.stderr + p.stdout)]
        return (sum(vals) / len(vals)) if vals else 2.0

    if role == "SUBTITLE":
        mid_act = zone_activity("crop=iw*0.8:ih*0.35:iw*0.1:ih*0.30")
        bot_act = zone_activity("crop=iw*0.8:ih*0.28:iw*0.1:ih*0.62")
        # Nếu sản phẩm/tay đang thao tác tập trung ở vùng đáy bàn -> Nâng phụ đề lên để không che sản phẩm!
        if bot_act > max(3.5, mid_act * 1.35):
            return (0.0, 0.42)
        return (0.0, -0.38)

    # Với CALLOUT hoặc BLING_ACCENT: Tìm khoảng trống thở (Negative Space) bên Trái hoặc bên Phải sản phẩm
    left_act = zone_activity("crop=iw*0.42:ih*0.40:iw*0.05:ih*0.25")
    right_act = zone_activity("crop=iw*0.42:ih*0.40:iw*0.53:ih*0.25")
    if left_act <= right_act:
        # Nửa bên trái thoáng hơn (sản phẩm đang nằm lệch sang phải) -> Đặt Callout ở khoảng trống bên Trái
        return (-0.34, 0.18 if role == "CALLOUT" else 0.28)
    else:
        # Nửa bên phải thoáng hơn -> Đặt Callout ở khoảng trống bên Phải
        return (0.32, 0.18 if role == "CALLOUT" else 0.28)

def select_smart_text_animation_and_style(
    text_str: str,
    role: str = "SUBTITLE",
    clip_dur_sec: float = 1.8,
    clip_speed: float = 1.0,
    bg_busy_score: float = 25.0,
    bottom_luma_y: float = 128.0,
    pill_bg_hex: str = "#241A14"
) -> Dict[str, any]:
    """
    [TRÍ TUỆ 3 - QUYẾT ĐỊNH THÔNG MINH "LÚC NÀO DÙNG CÁI NÀO"]:
    Tự động chọn hiệu ứng chữ (In/Out/Loop) và quyết định bật/tắt Hộp nền kính mờ (Frosted Pill Box)
    dựa trên ngữ nghĩa câu nói, tốc độ cảnh quay và độ rối thực tế của nền video!
    """
    txt_lower = text_str.lower()
    anim_in = "SPRING"
    anim_out = None
    anim_loop = None
    bg_color = ""

    if role == "HOOK_BANNER":
        anim_in, anim_out = "BOUNCE_IN", "BOUNCE_OUT"
        bg_color = pill_bg_hex
    elif role == "CTA":
        anim_in, anim_loop = "SPRING", "JUMP"
        bg_color = pill_bg_hex if bottom_luma_y > 160 else ""
    elif role == "BLING_ACCENT":
        anim_in, anim_out, anim_loop = "POP_UP", "FADE_OUT", "FLARE"
    elif role == "CALLOUT":
        # Nếu câu chứa con số đo lường, kích thước, cân nặng, nhiệt độ -> Dùng Máy đánh chữ (TYPEWRITER)
        if re.search(r"\b(\d+\s*(cm|mm|kg|ml|w|mah|độ|%)|1m\d+)\b", txt_lower):
            anim_in = "TYPEWRITER"
        else:
            anim_in = "POP_UP"
        anim_out = "BOUNCE_OUT"
        bg_color = pill_bg_hex
    else:
        # SUBTITLE: Linh hoạt theo nhịp cảnh và ý nghĩa câu nói
        if clip_speed < 0.95 or clip_dur_sec >= 2.6:
            # Cảnh quay chậm sang trọng (Micro Slow-Mo / Pan) -> Chữ hiện êm ái bằng FADE_IN
            anim_in = "FADE_OUT" if False else "SPRING"  # Hoặc FADE_IN nhẹ
        if any(w in txt_lower for w in ("co giãn", "đàn hồi", "giảm sâu", "rẻ", "cành", "k ")):
            anim_in = "ELASTIC_II"
        # Tự động bật hộp nền kính mờ nếu vùng nền dưới chữ quá rối hoặc chói lóa
        if bg_busy_score > 48.0 or bottom_luma_y > 188.0:
            bg_color = pill_bg_hex

    return {
        "anim_in": anim_in,
        "anim_out": anim_out,
        "anim_loop": anim_loop,
        "bg_color": bg_color
    }

def compute_adaptive_font_size(text_str: str, role: str = "SUBTITLE") -> float:
    """
    Tự động căn chỉnh Size Text linh hoạt theo độ dài câu và vai trò:
    - Câu ngắn đắt giá (<=12 ký tự): Phóng to 9.4 để đập vào mắt.
    - Câu vừa (13-22 ký tự): 8.2 chuẩn tầm mắt.
    - Câu dài (>22 ký tự): Thu nhẹ về 7.2 + tự động ngắt dòng trong vùng Safe Zone 76%.
    """
    n = len(text_str.strip())
    if role == "BLING_ACCENT":
        return 10.5
    if role == "HOOK_BANNER":
        return 9.6 if n <= 18 else (8.4 if n <= 28 else 7.5)
    if role == "CALLOUT":
        return 7.6 if n <= 18 else 6.8
    # SUBTITLE hoặc CTA
    if n <= 12:
        return 9.4
    elif n <= 22:
        return 8.2
    elif n <= 32:
        return 7.3
    return 6.6

def create_multistyle_text_material(
    text_str: str,
    highlight_keywords: Optional[List[str]] = None,
    palette_key: str = "COZY_PASTEL_MAMI",
    bottom_luma_y: float = 128.0,
    role: str = "SUBTITLE",
    custom_font_size: Optional[float] = None,
    bg_color: str = ""
) -> dict:
    """
    Tạo đối tượng Text Native CapCut chuẩn Sang Trọng (Luxury Typography):
    1. Tự động chọn bảng màu Chữ - Viền - Bóng theo Palette của ngành hàng.
    2. Tự động bù trừ độ dày Viền & Bóng theo độ sáng thực tế của vùng nền video (bottom_luma_y):
       - Nền quá sáng (>170): Tự tăng viền +25% & bóng đậm 0.85 để chữ không bị chìm vào nền trắng.
       - Nền tối (<95): Tự mảnh hóa viền 0.035 để chữ thanh thoát, sang trọng.
    3. Tô màu riêng Từ Khóa (Multi-style ranges) và khóa biên Safe Zone (line_max_width = 0.76).
    """
    mat_id = uid()
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["COZY_PASTEL_MAMI"])
    font_info = CAPCUT_FONTS.get(pal["font_key"], CAPCUT_FONTS["NUNITO"])

    base_hex = pal["base_hex"]
    highlight_hex = pal["highlight_hex"]
    stroke_hex = pal["stroke_hex"]
    stroke_w = pal["stroke_width"]
    shadow_alpha = pal["shadow_alpha"]
    shadow_diffuse = pal["shadow_diffuse"]

    # Dynamic Contrast Guard: Tự thích ứng với độ sáng vùng đặt chữ của video
    if bottom_luma_y > 170.0:
        stroke_w = min(0.09, round(stroke_w * 1.28, 4))
        shadow_alpha = min(0.90, round(shadow_alpha + 0.22, 2))
    elif bottom_luma_y < 95.0:
        stroke_w = max(0.030, round(stroke_w * 0.80, 4))

    font_size = custom_font_size or compute_adaptive_font_size(text_str, role=role)
    base_rgb = hex_to_rgb_float(base_hex)
    hl_rgb = hex_to_rgb_float(highlight_hex)
    stroke_rgb = hex_to_rgb_float(stroke_hex)
    shadow_rgb = hex_to_rgb_float(pal["shadow_hex"])

    hl_mask = [False] * len(text_str)
    for kw in (highlight_keywords or []):
        if not kw:
            continue
        for m in re.finditer(re.escape(kw), text_str, flags=re.IGNORECASE):
            for idx in range(m.start(), m.end()):
                hl_mask[idx] = True

    shadow_entry = [{
        "diffuse": round(shadow_diffuse / 6.0, 4),
        "angle": -45.0,
        "distance": 4.5,
        "alpha": shadow_alpha,
        "content": {"solid": {"color": shadow_rgb}}
    }]
    font_entry = {"id": font_info["resource_id"], "path": f"C:/{font_info['name']}.ttf"}

    styles = []
    if len(text_str) > 0:
        cur_state = hl_mask[0]
        start_idx = 0
        for i in range(1, len(text_str) + 1):
            if i == len(text_str) or hl_mask[i] != cur_state:
                color_rgb = hl_rgb if cur_state else base_rgb
                sz = round(font_size * 1.14, 1) if cur_state else font_size
                styles.append({
                    "fill": {"alpha": 1.0, "content": {"render_type": "solid", "solid": {"alpha": 1.0, "color": color_rgb}}},
                    "range": [start_idx, i],
                    "size": sz,
                    "bold": True,
                    "font": font_entry,
                    "strokes": [{"content": {"solid": {"alpha": 1.0, "color": stroke_rgb}}, "width": stroke_w}],
                    "shadows": shadow_entry
                })
                if i < len(text_str):
                    cur_state = hl_mask[i]
                    start_idx = i

    # Cờ bitmask chuẩn của pyJianYingDraft: 7 (base) | 8 (border) | 16 (background) | 32 (shadow)
    check_flag = 7 | 8 | 32 | (16 if bg_color else 0)
    content_obj = {"text": text_str, "styles": styles}

    return {
        "id": mat_id,
        "type": "text",
        "content": json.dumps(content_obj, ensure_ascii=False),
        "check_flag": check_flag,
        "alignment": 1,
        "line_feed": 1,
        "line_max_width": 0.76,  # Khóa biên Safe Zone 76% không bao giờ đè vào cột nút TikTok bên phải
        "force_apply_line_max_width": True,
        "letter_spacing": 0.02,
        "line_spacing": 0.05,
        "font_size": font_size,
        "font_name": font_info["name"],
        "font_resource_id": font_info["resource_id"],
        "text_color": base_hex,
        "background_color": bg_color,
        "background_alpha": 0.88 if bg_color else 0.0,
        "background_style": 1 if bg_color else 0,
        "background_round_radius": 0.42 if bg_color else 0.0,
        "background_height": 0.14,
        "background_width": 0.14,
        "border_color": stroke_hex,
        "border_width": stroke_w,
        "has_shadow": True,
        "shadow_color": pal["shadow_hex"],
        "shadow_alpha": shadow_alpha,
        "shadow_smoothing": shadow_diffuse,
        "shadow_distance": 4.5,
        "shadow_angle": -45.0,
        "layer_weight": 1
    }

def create_native_sticker_material_and_segment(
    sticker_resource_id: str,
    start_sec: float,
    end_sec: float,
    pos_x: float = -0.55,
    pos_y: float = -0.52,
    scale: float = 0.35,
    rotation: float = 0.0
) -> Tuple[dict, dict]:
    """
    Tạo Sticker gốc của CapCut (materials.stickers + Sticker_segment trên Track Sticker),
    ví dụ: Mũi tên chỉ Giỏ hàng góc trái, Tia lấp lánh Bling, Khung lấy nét.
    """
    mat_id = uid()
    dur_us = sec_to_us(end_sec - start_sec)
    s_mat = {
        "id": mat_id,
        "resource_id": sticker_resource_id,
        "sticker_id": sticker_resource_id,
        "source_platform": 1,
        "type": "sticker"
    }
    s_seg = {
        "id": uid(),
        "material_id": mat_id,
        "extra_material_refs": [],
        "source_timerange": {"start": 0, "duration": dur_us},
        "target_timerange": {"start": sec_to_us(start_sec), "duration": dur_us},
        "clip": {
            "scale": {"x": scale, "y": scale},
            "rotation": rotation,
            "transform": {"x": pos_x, "y": pos_y},
            "flip": {"vertical": False, "horizontal": False},
            "alpha": 1.0
        },
        "render_index": 13000,
        "visible": True
    }
    return s_mat, s_seg

def create_animation_group(
    in_key: Optional[str] = None,
    out_key: Optional[str] = None,
    loop_key: Optional[str] = None,
    is_text: bool = True,
    clip_duration_us: int = 2000000
) -> dict:
    """Tạo đối tượng trong materials.material_animations cho Text hoặc Video."""
    catalog = CAPCUT_TEXT_ANIMS if is_text else CAPCUT_VIDEO_ANIMS
    panel = "" if is_text else "video"
    mat_type = "text" if is_text else "video"
    anims = []

    if in_key and in_key in catalog:
        info = catalog[in_key]
        dur = min(info["dur"], clip_duration_us // 2)
        anims.append({
            "anim_adjust_params": None,
            "platform": "all",
            "panel": panel,
            "material_type": mat_type,
            "name": info["title"],
            "id": info["resource_id"],
            "resource_id": info["resource_id"],
            "type": info["type"],
            "start": 0,
            "duration": dur
        })
    if out_key and out_key in catalog:
        info = catalog[out_key]
        dur = min(info["dur"], clip_duration_us // 3)
        anims.append({
            "anim_adjust_params": None,
            "platform": "all",
            "panel": panel,
            "material_type": mat_type,
            "name": info["title"],
            "id": info["resource_id"],
            "resource_id": info["resource_id"],
            "type": "out",
            "start": max(0, clip_duration_us - dur),
            "duration": dur
        })
    if loop_key and loop_key in catalog:
        info = catalog[loop_key]
        anims.append({
            "anim_adjust_params": None,
            "platform": "all",
            "panel": panel,
            "material_type": mat_type,
            "name": info["title"],
            "id": info["resource_id"],
            "resource_id": info["resource_id"],
            "type": "loop",
            "start": 0,
            "duration": clip_duration_us
        })

    return {
        "id": uid(),
        "type": "sticker_animation",
        "multi_language_current": "none",
        "animations": anims
    }

def create_transition_material(trans_key: str, duration_us: Optional[int] = None) -> dict:
    """Tạo đối tượng chuyển cảnh trong materials.transitions."""
    info = CAPCUT_TRANSITIONS.get(trans_key, CAPCUT_TRANSITIONS["PULL_IN"])
    return {
        "id": uid(),
        "name": info["name"],
        "effect_id": info["effect_id"],
        "resource_id": info["resource_id"],
        "duration": duration_us or info["dur"],
        "is_overlap": info["is_overlap"],
        "platform": "all",
        "type": "transition",
        "category_id": "",
        "category_name": ""
    }

def create_mask_material(
    mask_key: str = "RECTANGLE",
    center_x: float = 0.0,
    center_y: float = 0.0,
    width: float = 0.5,
    height: float = 0.5,
    feather: float = 0.05,
    rotation: float = 0.0,
    round_corner: float = 0.25
) -> dict:
    """Tạo mặt nạ (Split, Circle, Rectangle bo góc) trong materials.common_mask."""
    info = CAPCUT_MASKS.get(mask_key, CAPCUT_MASKS["RECTANGLE"])
    return {
        "id": uid(),
        "name": info["name"],
        "platform": "all",
        "position_info": "",
        "resource_type": info["resource_type"],
        "resource_id": info["resource_id"],
        "type": "mask",
        "config": {
            "aspectRatio": 1.0,
            "centerX": center_x,
            "centerY": center_y,
            "expansion": 0.0,
            "feather": feather,
            "height": height,
            "invert": False,
            "rotation": rotation,
            "roundCorner": round_corner,
            "width": width
        }
    }

def create_scale_keyframes(start_scale: float, end_scale: float, duration_us: int) -> List[dict]:
    """Tạo cặp Keyframe phóng to mượt (Slow Creep-Zoom) cho KFTypeScaleX và KFTypeScaleY."""
    kfs = []
    for prop in ("KFTypeScaleX", "KFTypeScaleY"):
        kfs.append({
            "id": uid(),
            "property_type": prop,
            "keyframe_list": [
                {
                    "id": uid(), "time_offset": 0, "values": [start_scale],
                    "curveType": "Line", "graphID": "",
                    "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}
                },
                {
                    "id": uid(), "time_offset": duration_us, "values": [end_scale],
                    "curveType": "Line", "graphID": "",
                    "left_control": {"x": 0.0, "y": 0.0}, "right_control": {"x": 0.0, "y": 0.0}
                }
            ]
        })
    return kfs

CAPCUT_VOICE_FILTERS = {
    "SWEET":     {"name": "Sweet",     "resource_id": "7320193577613529602", "effect_id": "2787429"},
    "ENERGETIC": {"name": "Energetic", "resource_id": "7320193885114733057", "effect_id": "2787437"},
    "DEEP":      {"name": "Deep",      "resource_id": "7021052537344102913", "effect_id": "1376190"},
}

def create_scene_effect_material(fx_key: str) -> dict:
    """Tạo đối tượng kỹ xảo cảnh quay trong materials.video_effects (chuẩn pyJianYingDraft)."""
    info = CAPCUT_SCENE_EFFECTS.get(fx_key, CAPCUT_SCENE_EFFECTS["CAMERA_FOCUS"])
    return {
        "id": uid(),
        "name": info["name"],
        "effect_id": info["effect_id"],
        "resource_id": info["resource_id"],
        "type": "video_effect",
        "apply_target_type": 2,
        "adjust_params": [],
        "category_id": "",
        "category_name": "",
        "platform": "all",
        "render_index": 10000,
        "source_platform": 0,
        "time_range": None,
        "value": 1.0,
        "version": ""
    }

def create_voice_filter_material(voice_key: str) -> dict:
    """Tạo bộ lọc giọng nói trong materials.audio_effects (Sweet / Energetic / Deep)."""
    info = CAPCUT_VOICE_FILTERS.get(voice_key, CAPCUT_VOICE_FILTERS["SWEET"])
    return {
        "id": uid(),
        "name": info["name"],
        "resource_id": info["resource_id"],
        "category_id": "sound_effect",
        "category_name": "Voice filters",
        "audio_adjust_params": [],
        "is_ugc": False,
        "production_path": "",
        "speaker_id": "",
        "sub_type": 1,
        "time_range": {"duration": 0, "start": 0},
        "type": "audio_effect"
    }

# ==============================================================================
# 4. HÀM KIỂM ĐỊNH CHÉO CHỐNG LỖI CORRUPTED PROJECT (SELF-VERIFICATION ENGINE)
# ==============================================================================

def verify_capcut_draft(draft: dict) -> Tuple[bool, List[str]]:
    """
    Kiểm tra toàn vẹn tham chiếu (Referential Integrity) và chuẩn CHR trước khi ghi đĩa:
    1. Mọi material_id và extra_material_refs trong tracks phải tồn tại trong materials.
    2. Mọi file media cục bộ phải tồn tại thật trên ổ cứng.
    3. Thời lượng ảnh tĩnh không vượt quá 30% tổng thời lượng video (Bảo vệ điểm CHR).
    """
    errors = []
    all_mat_ids = set()
    photo_mat_ids = set()
    for mat_list in draft.get("materials", {}).values():
        if isinstance(mat_list, list):
            for item in mat_list:
                if isinstance(item, dict) and "id" in item:
                    all_mat_ids.add(item["id"])
                    if item.get("type") == "photo":
                        photo_mat_ids.add(item["id"])
                    if "path" in item and item["path"] and not os.path.exists(item["path"]):
                        errors.append(f"Missing media file on disk: {item['path']}")

    total_v1_us = 0
    photo_v1_us = 0
    for trk in draft.get("tracks", []):
        for seg in trk.get("segments", []):
            mid = seg.get("material_id")
            if mid not in all_mat_ids:
                errors.append(f"Orphan material_id {mid} in track {trk.get('type')}")
            for ref in seg.get("extra_material_refs", []):
                if ref not in all_mat_ids:
                    errors.append(f"Orphan extra_material_ref {ref} in track {trk.get('type')}")
            if trk.get("type") == "video" and seg.get("render_index", 0) == 0:
                dur = seg.get("target_timerange", {}).get("duration", 0)
                total_v1_us += dur
                if mid in photo_mat_ids:
                    photo_v1_us += dur

    if total_v1_us > 0 and (photo_v1_us / total_v1_us) > 0.30:
        errors.append(
            f"CHR Violation Risk: Static photos occupy {photo_v1_us/total_v1_us:.1%} of Track V1 (>30%). "
            "Must move static photos to Track V2 PiP (`is_pip: True`)!"
        )
    return (len(errors) == 0, errors)

# ==============================================================================
# 5. HÀM CHÍNH: BƠM TOÀN BỘ PROJECT ĐA LỚP VÀO CAPCUT DESKTOP
# ==============================================================================

def inject_full_capcut_project(project_name: str, edit_plan: dict):
    """
    Đóng CapCut tạm thời, bơm toàn bộ Video, PiP, Masks, Transitions (tự động khâu khít 0µs),
    Multi-Style Text + Animations, Scene Effects Track, Voiceover + Voice Filters, SFX, BGM
    vào thư mục Draft của CapCut, kiểm định toàn vẹn và mở lại ứng dụng.
    """
    subprocess.run(["killall", "CapCut"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    template_dir = os.path.join(CAPCUT_DRAFTS_ROOT, "0711")
    target_dir = os.path.join(CAPCUT_DRAFTS_ROOT, project_name)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(template_dir, target_dir)

    draft_info_path = os.path.join(target_dir, "draft_info.json")
    with open(draft_info_path, "r", encoding="utf-8") as f:
        draft = json.load(f)

    draft_id = uid()
    now_ts = int(time.time())
    draft["id"] = draft_id
    draft["name"] = project_name
    draft["fps"] = 30.0
    draft["canvas_config"] = {"ratio": "9:16", "width": 1080, "height": 1920, "background": None}

    videos_mat, audios_mat, texts_mat, speeds_mat, canvases_mat = [], [], [], [], []
    transitions_mat, anims_mat, masks_mat, vfx_mat, fades_mat, audio_fx_mat = [], [], [], [], [], []

    v1_segments, v2_pip_segments, effect_segments = [], [], []
    text_sub_segments, text_hook_segments = [], []
    audio_vo_segments, audio_sfx_segments, audio_bgm_segments = [], [], []

    total_duration_us = 0
    v1_cursor_us = 0  # Con trỏ tự động khâu khít 0µs giữa các clip trên Track V1 để Transition luôn hoạt động

    # 1. Nạp Main Video Track (V1) & Overlay PiP Track (V2)
    for seg in edit_plan.get("video_timeline", []):
        v_mat_id, sp_mat_id, cv_mat_id = uid(), uid(), uid()
        src_start_us = sec_to_us(seg["source_in_sec"])
        src_dur_us = sec_to_us(seg["source_out_sec"] - seg["source_in_sec"])
        speed_val = float(seg.get("speed", 1.0))
        t_dur_us = sec_to_us(seg["timeline_end_sec"] - seg["timeline_start_sec"])

        if seg.get("is_pip"):
            t_start_us = sec_to_us(seg["timeline_start_sec"])
        else:
            # Khâu khít liền mạch tuyệt đối trên Track V1 để Transition Overlap không bị hở
            t_start_us = v1_cursor_us
            v1_cursor_us += t_dur_us

        total_duration_us = max(total_duration_us, t_start_us + t_dur_us)

        videos_mat.append({
            "id": v_mat_id,
            "type": "photo" if seg["source_file"].lower().endswith((".jpg", ".jpeg", ".png", ".webp")) else "video",
            "path": os.path.abspath(seg["source_file"]),
            "material_name": os.path.basename(seg["source_file"]),
            "width": seg.get("width", 1080), "height": seg.get("height", 1920),
            "duration": sec_to_us(seg.get("file_total_duration_sec", 30.0)),
            "has_audio": True, "category_name": "local", "crop_ratio": "free", "crop_scale": 1.0,
            "crop": {"upper_left_x": 0.0, "upper_left_y": 0.0, "upper_right_x": 1.0, "upper_right_y": 0.0,
                     "lower_left_x": 0.0, "lower_left_y": 1.0, "lower_right_x": 1.0, "lower_right_y": 1.0}
        })
        speeds_mat.append({"id": sp_mat_id, "type": "speed", "mode": 0, "speed": speed_val, "curve_speed": None})
        blur_lvl = float(seg.get("canvas_blur", 0.0))
        canvases_mat.append({
            "id": cv_mat_id,
            "type": "canvas_blur" if blur_lvl > 0 else "canvas_color",
            "color": "", "blur": blur_lvl
        })

        extra_refs = [sp_mat_id, cv_mat_id]

        if seg.get("video_anim"):
            anim_grp = create_animation_group(in_key=seg["video_anim"], is_text=False, clip_duration_us=t_dur_us)
            anims_mat.append(anim_grp)
            extra_refs.append(anim_grp["id"])

        if seg.get("mask"):
            m_mat = create_mask_material(mask_key=seg["mask"])
            masks_mat.append(m_mat)
            extra_refs.append(m_mat["id"])

        if seg.get("transition") and not seg.get("is_pip"):
            tr_mat = create_transition_material(seg["transition"])
            transitions_mat.append(tr_mat)
            extra_refs.append(tr_mat["id"])

        scale_start = float(seg.get("scale", 1.0))
        scale_end = float(seg.get("scale_end", scale_start * 1.05))
        kfs = create_scale_keyframes(scale_start, scale_end, t_dur_us) if scale_end != scale_start else []

        v_seg_obj = {
            "id": uid(), "material_id": v_mat_id, "extra_material_refs": extra_refs,
            "source_timerange": {"start": src_start_us, "duration": src_dur_us},
            "target_timerange": {"start": t_start_us, "duration": t_dur_us},
            "speed": speed_val, "volume": float(seg.get("native_volume", 0.0)),
            "clip": {
                "scale": {"x": scale_start, "y": scale_start}, "rotation": 0.0,
                "transform": {"x": float(seg.get("pos_x", 0.0)), "y": float(seg.get("pos_y", 0.0))},
                "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0
            },
            "uniform_scale": {"on": True, "value": scale_start},
            "common_keyframes": kfs,
            "enable_adjust": True, "enable_lut": True,
            "render_index": 1 if seg.get("is_pip") else 0
        }
        if seg.get("is_pip"):
            v2_pip_segments.append(v_seg_obj)
        else:
            v1_segments.append(v_seg_obj)

    # 2. Nạp Kỹ xảo Cảnh quay (Video Scene Effects Track: CAMERA_FOCUS, BLURRY_FOCUS, EDGE_GLOW, BLURAY_SCAN...)
    for fx in edit_plan.get("scene_effects", []):
        fx_mat = create_scene_effect_material(fx["effect_key"])
        vfx_mat.append(fx_mat)
        fx_dur_us = sec_to_us(fx["end_sec"] - fx["start_sec"])
        effect_segments.append({
            "id": uid(),
            "material_id": fx_mat["id"],
            "extra_material_refs": [],
            "target_timerange": {"start": sec_to_us(fx["start_sec"]), "duration": fx_dur_us},
            "render_index": 11000,
            "visible": True,
            "volume": 1.0
        })

    # 3. Nạp Phụ đề Động Đa Màu Từ Khóa, Nhãn Callout & Icon Bling Sang Trọng
    default_palette = edit_plan.get("typography_palette", "COZY_PASTEL_MAMI")
    default_luma_y = float(edit_plan.get("bottom_luma_y", 128.0))

    for txt in edit_plan.get("text_overlays", []):
        dur_us = sec_to_us(txt["end_sec"] - txt["start_sec"])
        role = txt.get("role", "SUBTITLE")
        t_mat = create_multistyle_text_material(
            text_str=txt["text"],
            highlight_keywords=txt.get("highlight_keywords", []),
            palette_key=txt.get("palette_key", default_palette),
            bottom_luma_y=float(txt.get("bottom_luma_y", default_luma_y)),
            role=role,
            custom_font_size=txt.get("font_size"),
            bg_color=txt.get("bg_color", "")
        )
        texts_mat.append(t_mat)

        anim_in = txt.get("anim_in", "BOUNCE_IN" if role == "HOOK_BANNER" else ("POP_UP" if role in ("CALLOUT", "BLING_ACCENT") else "SPRING"))
        anim_out = txt.get("anim_out", "BOUNCE_OUT" if role in ("HOOK_BANNER", "CALLOUT", "BLING_ACCENT") else None)
        anim_loop = txt.get("anim_loop", "FLARE" if role == "BLING_ACCENT" else ("JUMP" if role == "CTA" else None))

        anim_grp = create_animation_group(in_key=anim_in, out_key=anim_out, loop_key=anim_loop, is_text=True, clip_duration_us=dur_us)
        anims_mat.append(anim_grp)

        scale_xy = float(txt.get("scale", 0.72 if role == "BLING_ACCENT" else 1.0))
        t_seg = {
            "id": uid(), "material_id": t_mat["id"], "extra_material_refs": [anim_grp["id"]],
            "source_timerange": {"start": 0, "duration": dur_us},
            "target_timerange": {"start": sec_to_us(txt["start_sec"]), "duration": dur_us},
            "clip": {
                "scale": {"x": scale_xy, "y": scale_xy}, "rotation": float(txt.get("rotation", 0.0)),
                "transform": {"x": float(txt.get("pos_x", 0.0)), "y": float(txt.get("pos_y", -0.38))},
                "flip": {"vertical": False, "horizontal": False}, "alpha": 1.0
            },
            "render_index": 14000
        }
        if role in ("HOOK_BANNER", "CALLOUT", "CTA", "BLING_ACCENT"):
            text_hook_segments.append(t_seg)
        else:
            text_sub_segments.append(t_seg)

    # 4. Nạp các Track Âm thanh (Voiceover + Voice Filters + Studio SFX + Commercial BGM + Fade In/Out)
    for aud in edit_plan.get("audio_tracks", []):
        a_mat_id, sp_mat_id = uid(), uid()
        dur_us = sec_to_us(aud["end_sec"] - aud["start_sec"])
        has_voice_fx = bool(aud.get("voice_filter"))
        audios_mat.append({
            "id": a_mat_id, "type": "extract_music",
            "path": os.path.abspath(aud["source_file"]),
            "name": os.path.basename(aud["source_file"]),
            "duration": sec_to_us(aud.get("file_total_duration_sec", 60.0)),
            "has_audio_effect": has_voice_fx,
            "category_name": "local"
        })
        speeds_mat.append({"id": sp_mat_id, "type": "speed", "mode": 0, "speed": 1.0, "curve_speed": None})
        extra_refs = [sp_mat_id]

        if aud.get("fade_in_sec") or aud.get("fade_out_sec"):
            fade_id = uid()
            fades_mat.append({
                "id": fade_id, "type": "audio_fade",
                "fade_in_duration": sec_to_us(aud.get("fade_in_sec", 0.0)),
                "fade_out_duration": sec_to_us(aud.get("fade_out_sec", 0.0)),
                "fade_type": 0
            })
            extra_refs.append(fade_id)

        if has_voice_fx:
            vfx_obj = create_voice_filter_material(aud["voice_filter"])
            audio_fx_mat.append(vfx_obj)
            extra_refs.append(vfx_obj["id"])

        a_seg = {
            "id": uid(), "material_id": a_mat_id, "extra_material_refs": extra_refs,
            "source_timerange": {"start": sec_to_us(aud.get("source_in_sec", 0.0)), "duration": dur_us},
            "target_timerange": {"start": sec_to_us(aud["start_sec"]), "duration": dur_us},
            "speed": 1.0, "volume": float(aud.get("volume", 1.0)), "render_index": 0
        }
        track_role = aud.get("role", "VOICEOVER")
        if track_role == "SFX":
            audio_sfx_segments.append(a_seg)
        elif track_role == "BGM":
            audio_bgm_segments.append(a_seg)
        else:
            audio_vo_segments.append(a_seg)

    draft["duration"] = total_duration_us
    draft["materials"]["videos"] = videos_mat
    draft["materials"]["audios"] = audios_mat
    draft["materials"]["texts"] = texts_mat
    draft["materials"]["speeds"] = speeds_mat
    draft["materials"]["canvases"] = canvases_mat
    draft["materials"]["transitions"] = transitions_mat
    draft["materials"]["material_animations"] = anims_mat
    draft["materials"]["common_mask"] = masks_mat
    draft["materials"]["video_effects"] = vfx_mat
    draft["materials"]["audio_fades"] = fades_mat
    draft["materials"]["audio_effects"] = audio_fx_mat

    tracks = [{"id": uid(), "type": "video", "segments": v1_segments, "flag": 0, "attribute": 0}]
    if v2_pip_segments:
        tracks.append({"id": uid(), "type": "video", "segments": v2_pip_segments, "flag": 0, "attribute": 0})
    if effect_segments:
        tracks.append({"id": uid(), "type": "effect", "segments": effect_segments, "flag": 0, "attribute": 0})
    tracks.extend([
        {"id": uid(), "type": "text", "segments": text_sub_segments, "flag": 0, "attribute": 0},
        {"id": uid(), "type": "text", "segments": text_hook_segments, "flag": 0, "attribute": 0},
        {"id": uid(), "type": "audio", "segments": audio_vo_segments, "flag": 0, "attribute": 0},
        {"id": uid(), "type": "audio", "segments": audio_sfx_segments, "flag": 0, "attribute": 0},
        {"id": uid(), "type": "audio", "segments": audio_bgm_segments, "flag": 0, "attribute": 0},
    ])
    draft["tracks"] = tracks

    # Kiểm định toàn vẹn trước khi lưu
    is_valid, errs = verify_capcut_draft(draft)
    if not is_valid:
        raise ValueError(f"❌ Phát hiện lỗi cấu trúc Draft CapCut: {errs}")

    # Ghi đồng thời vào draft_info.json, draft_content.json và Timelines/ (nếu có) để tương thích 100%
    for fname in ("draft_info.json", "draft_content.json"):
        with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
            json.dump(draft, f, ensure_ascii=False)

    timelines_dir = os.path.join(target_dir, "Timelines")
    if os.path.isdir(timelines_dir):
        for sub in os.listdir(timelines_dir):
            tl_content = os.path.join(timelines_dir, sub, "draft_content.json")
            if os.path.exists(tl_content):
                with open(tl_content, "w", encoding="utf-8") as f:
                    json.dump(draft, f, ensure_ascii=False)

    # Cập nhật draft_meta_info.json và root_meta_info.json
    meta_path = os.path.join(target_dir, "draft_meta_info.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta.update({
            "draft_id": draft_id, "draft_name": project_name,
            "draft_fold_path": target_dir, "tm_duration": total_duration_us,
            "tm_draft_Modified": now_ts * 1_000_000
        })
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)

    root_meta_path = os.path.join(CAPCUT_DRAFTS_ROOT, "root_meta_info.json")
    if os.path.exists(root_meta_path):
        with open(root_meta_path, "r", encoding="utf-8") as f:
            root_meta = json.load(f)
        store = root_meta.get("all_draft_store", [])
        new_entry = dict(store[0]) if store else {}
        new_entry.update({
            "draft_id": draft_id, "draft_name": project_name,
            "draft_fold_path": target_dir, "draft_json_file": draft_info_path,
            "draft_root_path": CAPCUT_DRAFTS_ROOT, "tm_duration": total_duration_us,
            "tm_draft_create": now_ts * 1_000_000, "tm_draft_modified": now_ts * 1_000_000
        })
        store = [e for e in store if e.get("draft_name") != project_name]
        store.insert(0, new_entry)
        root_meta["all_draft_store"] = store
        with open(root_meta_path, "w", encoding="utf-8") as f:
            json.dump(root_meta, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã kiểm định (0 lỗi) & bơm thành công Project '{project_name}' vào CapCut Desktop!")
