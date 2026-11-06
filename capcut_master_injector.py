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

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CAPCUT_DRAFTS_ROOT = os.path.expanduser(
    "~/Movies/CapCut/User Data/Projects/com.lveditor.draft"
)
if not os.path.exists(CAPCUT_DRAFTS_ROOT) and os.name == "nt":
    CAPCUT_DRAFTS_ROOT = os.path.expandvars(
        r"%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft"
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
    ext_reg_path = os.path.join(REPO_ROOT, "knowledge_vault", "external_custom_sfx_registry.json")
    if os.path.exists(ext_reg_path):
        try:
            with open(ext_reg_path, "r", encoding="utf-8") as f:
                ext_reg = json.load(f)
            for sfx_id, item in ext_reg.get("items", {}).items():
                raw_fp = item.get("relative_path") or item.get("file_path", "")
                fp = raw_fp
                if raw_fp and not os.path.exists(raw_fp):
                    # Tự động ánh xạ lại đường dẫn khi clone repo sang máy tính mới
                    cand = os.path.abspath(os.path.join(REPO_ROOT, raw_fp.lstrip("./")))
                    if os.path.exists(cand):
                        fp = cand
                    else:
                        for marker in ("knowledge_vault/", "workspace/"):
                            if marker in raw_fp:
                                rel_tail = raw_fp.split(marker, 1)[1]
                                cand2 = os.path.abspath(os.path.join(REPO_ROOT, marker, rel_tail))
                                if os.path.exists(cand2):
                                    fp = cand2
                                    break
                elif raw_fp:
                    fp = os.path.abspath(raw_fp)

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
    },
    "KINFOLK_ESPRESSO_CREAM": {
        # Phong cách Tạp chí Kinfolk / Pinterest Aesthetic (@byraanni): Kem Ngà + Nâu Espresso + Vàng Caramel
        "base_hex": "#FDFBF7",       # Kem Ngà Tinh Khiết (Warm Ivory)
        "highlight_hex": "#E6B980",  # Vàng Latte / Caramel Sáng
        "alt_hl_hex": "#D4A373",     # Nâu Cam Đất Nhẹ
        "stroke_hex": "#2C1A12",     # Nâu Espresso Đậm
        "stroke_width": 0.042,
        "shadow_hex": "#1A0F0A",
        "shadow_alpha": 0.62,
        "shadow_diffuse": 0.58,
        "pill_bg_hex": "#3B261E",    # Hộp nền Espresso Mờ Sang Trọng
        "font_key": "PLAYFAIR",
        "default_sub_anim": "SPRING",
        "bling_icons": ["✧", "✦", "🤍", "☕"]
    },
    "PEGBOARD_ROSE_GOLD": {
        # Phong cách Studio Bảng Pegboard Hồng Phấn (@3thag8_): Trắng Sữa + Hồng Phấn + Vàng Bơ
        "base_hex": "#FFFFFF",       # Trắng Sữa Sắc Nét
        "highlight_hex": "#FFB3C6",  # Hồng Phấn Baby Pink
        "alt_hl_hex": "#FFE066",     # Vàng Bơ Tươi
        "stroke_hex": "#2B1922",     # Nâu Tím Mận Sẫm
        "stroke_width": 0.058,
        "shadow_hex": "#1B0E14",
        "shadow_alpha": 0.68,
        "shadow_diffuse": 0.48,
        "pill_bg_hex": "#2B1922",
        "font_key": "NUNITO",
        "default_sub_anim": "POP_UP",
        "bling_icons": ["🌸", "✨", "💗", "🫧"]
    },
    "GRAYUNBOX_CLEAN_MINIMAL": {
        # Phong cách @grayunbox (2.8M views): Phụ đề 2 dòng góc 1/3 trên (y=+0.58), Trắng Tinh Khiết + Vàng Bơ Nhạt / Xanh Matcha + Viền Than Chì Mảnh
        "base_hex": "#FFFFFF",       # Trắng Tinh Khiết
        "highlight_hex": "#FFE699",  # Vàng Bơ Nhạt Dịu Mắt
        "alt_hl_hex": "#A8E6CF",     # Xanh Matcha / Thảo Mộc
        "stroke_hex": "#1C1E21",     # Đen Than Chì Sắc Nét
        "stroke_width": 0.048,
        "shadow_hex": "#101214",
        "shadow_alpha": 0.66,
        "shadow_diffuse": 0.42,
        "pill_bg_hex": "#1C1E21",
        "font_key": "NUNITO",
        "default_sub_anim": "SPRING",
        "bling_icons": ["🍃", "🫧", "🧸", "✨"]
    },
    "MINHTIENOIII_GENZ_SENSORY_POP": {
        # Phong cách @minhtienoiii06 (19.3M views): Chữ thường lowercase mở đầu bằng 🗣️, Vàng Kem Kem Lạnh + Xanh Lá Dứa Neon, Viền Đen Sắc Nét
        "base_hex": "#FFFFFF",       # Trắng Sữa Nổi Bật
        "highlight_hex": "#FFF07C",  # Vàng Kem Vani / Sữa Dừa
        "alt_hl_hex": "#80FF72",     # Xanh Lá Dứa Neon (Pandan Green)
        "stroke_hex": "#181818",     # Viền Đen Sắc Nét
        "stroke_width": 0.056,
        "shadow_hex": "#0D0D0D",
        "shadow_alpha": 0.70,
        "shadow_diffuse": 0.44,
        "pill_bg_hex": "#1F241D",
        "font_key": "NUNITO",
        "default_sub_anim": "POP_UP",
        "bling_icons": ["🗣️", "🍅", "🍠", "✨"]
    },
    "YUHTT09_COQUETTE_CLEAN_WHITE_PILL": {
        # Phong cách @yuhtt09 (8.1M views & 54-video DNA): 1-Line Rounded Sans-Serif màu Trắng (#FFFFFF) viền Đen dày (#141414) tại y=-0.35 + Hồng Coquette (#FF8FAB) + Kaomoji 🌷🎀
        "base_hex": "#FFFFFF",       # Trắng Tinh Khiết Sắc Nét
        "highlight_hex": "#FF8FAB",  # Hồng Coquette Nơ Ruy-Băng
        "alt_hl_hex": "#BDE0FE",     # Xanh Pastel Dịu Mắt
        "stroke_hex": "#141414",     # Viền Đen Dày Tương Phản Cao (Đọc rõ trên nền bàn trắng YAVG 166)
        "stroke_width": 0.062,
        "shadow_hex": "#0A0A0A",
        "shadow_alpha": 0.72,
        "shadow_diffuse": 0.42,
        "pill_bg_hex": "#FF8FAB",    # Hộp nền Hồng Coquette cho từ khóa nhấn [kem nền high-end??]
        "font_key": "NUNITO",
        "default_sub_anim": "POP_UP",
        "bling_icons": ["🌷", "🎀", "🌱", "✨"]
    }
}

# Bảng thông số Chỉnh Màu (Color Grading Adjust + HSL Da) học từ 8 KOC Master
KOC_COLOR_GRADE_PRESETS = {
    "HONGHANH_WARM_DESK_LAMP": {
        "creator_ref": "@honghanhxinhgai_01",
        "description": "Đèn bàn ấm rọi đỉnh đầu + Làm hồng mịn da tay & sáng sản phẩm (UHD)",
        "adjust": {
            "brightness": 7,
            "contrast": -14,
            "exposure": 22,
            "sharpen": 30,
            "brilliance": 35,
            "highlights": -10,
            "shadows": 11,
            "temp": 4,
            "saturation": -4
        },
        "hsl_skin_orange_red": {"hue": -36, "saturation": -55, "luminance": 70},
        "uhd_enhance": True
    },
    "BYRAANNI_KINFOLK_ESPRESSO": {
        "creator_ref": "@byraanni",
        "description": "Tạp chí Kinfolk/Pinterest: Nền bàn trắng ngà dịu mắt + Tương phản cổ tay áo len Nâu Espresso",
        "adjust": {
            "brightness": 4,
            "contrast": -8,
            "exposure": 10,
            "sharpen": 24,
            "brilliance": 18,
            "highlights": -12,
            "shadows": 15,
            "temp": 8,
            "saturation": -6
        },
        "hsl_skin_orange_red": {"hue": -12, "saturation": -20, "luminance": 28},
        "uhd_enhance": True
    },
    "3THAG8_PEGBOARD_CLEAN_PINK": {
        "creator_ref": "@3thag8_",
        "description": "Studio Pegboard 2 nhiệt độ màu: Tách bạch nền ấm và mặt bàn trắng hồng trong trẻo",
        "adjust": {
            "brightness": 6,
            "contrast": 5,
            "exposure": 12,
            "sharpen": 28,
            "brilliance": 20,
            "highlights": -8,
            "shadows": 10,
            "temp": -4,
            "saturation": 8
        },
        "hsl_skin_orange_red": {"hue": -18, "saturation": -25, "luminance": 35},
        "uhd_enhance": True
    },
    "MESHIN_NATURAL_DAYLIGHT": {
        "creator_ref": "@meshinthuine",
        "description": "Ánh sáng cửa sổ tự nhiên ấm cúng, chân thực chuẩn Mẹ Bỉm KOC triệu đơn",
        "adjust": {
            "brightness": 5,
            "contrast": -6,
            "exposure": 14,
            "sharpen": 22,
            "brilliance": 16,
            "highlights": -6,
            "shadows": 12,
            "temp": 6,
            "saturation": 4
        },
        "hsl_skin_orange_red": {"hue": -10, "saturation": -15, "luminance": 22},
        "uhd_enhance": False
    },
    "GRAYUNBOX_VENETIAN_BLINDS_CHIAROSCURO": {
        "creator_ref": "@grayunbox",
        "description": "Nắng xiên qua rèm sáo ngang tạo vệt bóng Chiaroscuro nghệ thuật trên bàn trắng mờ (YAVG ~132) + Lò xo Chrome",
        "adjust": {
            "brightness": 5,
            "contrast": 8,
            "exposure": 8,
            "sharpen": 26,
            "brilliance": 20,
            "highlights": -10,
            "shadows": -6,
            "temp": 3,
            "saturation": 2
        },
        "hsl_skin_orange_red": {"hue": -14, "saturation": -18, "luminance": 26},
        "uhd_enhance": True
    },
    "GRAYUNBOX_LOWKEY_LED_GLOW": {
        "creator_ref": "@grayunbox",
        "description": "Chế độ Low-Key Ambient (YAVG ~85) chuyên trị sản phẩm có đèn LED / Thiệp phát sáng / Đèn ngủ giúp ánh sáng sản phẩm rực rỡ gấp 3 lần",
        "adjust": {
            "brightness": -8,
            "contrast": 14,
            "exposure": -10,
            "sharpen": 24,
            "brilliance": 22,
            "highlights": -4,
            "shadows": -14,
            "temp": 2,
            "saturation": 12
        },
        "hsl_skin_orange_red": {"hue": -10, "saturation": -15, "luminance": 18},
        "uhd_enhance": True
    },
    "MINHTIENOIII_COZY_TOAST_LAMP_SENSORY": {
        "creator_ref": "@minhtienoiii06",
        "description": "Bàn học Chill Đèn ngủ lát bánh mì TOAST xanh lá + Đèn Ring-light cam ấm phản chiếu độ bóng (YAVG ~144.5, SAT cao tôn màu đồ ăn vặt & phụ kiện)",
        "adjust": {
            "brightness": 6,
            "contrast": 6,
            "exposure": 10,
            "sharpen": 28,
            "brilliance": 24,
            "highlights": -6,
            "shadows": 8,
            "temp": 5,
            "saturation": 10
        },
        "hsl_skin_orange_red": {"hue": -14, "saturation": -16, "luminance": 28},
        "uhd_enhance": True
    },
    "YUHTT09_HIGHKEY_AIRY_DOUYIN_WHITE": {
        "creator_ref": "@yuhtt09",
        "description": "High-Key Airy Douyin White Studio (YAVG ~166.1, SAT ~9.1): Mặt bàn trắng tinh + Bảng lỗ Pegboard trắng gắn nơ hồng Coquette 🎀 + Da tay trắng hồng trong veo",
        "adjust": {
            "brightness": 8,
            "contrast": -6,
            "exposure": 16,
            "sharpen": 28,
            "brilliance": 26,
            "highlights": -8,
            "shadows": 14,
            "temp": -3,
            "saturation": -8
        },
        "hsl_skin_orange_red": {"hue": -22, "saturation": -32, "luminance": 48},
        "uhd_enhance": True
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
    video_path: str,
    start_sec: float,
    dur_sec: float = 1.5,
    role: str = "SUBTITLE",
    subtitle_zone_preference: str = "AUTO"
) -> Tuple[float, float]:
    """
    [TRÍ TUỆ 2 - ĐỊNH VỊ VỊ TRÍ TEXT ĐỘNG KHÔNG ĐÈ LÊN SẢN PHẨM (OBSTACLE-AWARE POSITIONING)]:
    Phân tích mật độ chuyển động và chi tiết của các vùng trên khung hình dọc 9:16:
    1. Với SUBTITLE:
       - Nếu bật `subtitle_zone_preference="UPPER_MIDDLE_HONGHANH"` (Phong cách @honghanhxinhgai_01):
         Cố định phụ đề ở vùng trên-giữa (y = +0.46) để nhường trọn vẹn nửa dưới khung hình cho 2 bàn tay và sản phẩm!
       - Mặc định ở vùng đáy chuẩn (y = -0.38). Nhưng nếu phát hiện bàn tay và sản phẩm
         đang thao tác sát đáy bàn (vùng đáy có chuyển động mạnh gấp >1.35 lần vùng giữa),
         hệ thống tự động dời Phụ đề lên vùng trống phía trên (y = +0.42 hoặc -0.18) để nhường chỗ cho sản phẩm!
    2. Với CALLOUT & BLING_ACCENT: So sánh mật độ chi tiết giữa nửa Trái và nửa Phải của sản phẩm,
       tự động đặt nhãn vào "Khoảng trống thở" (Negative Space) bên cạnh sản phẩm, tuyệt đối không đè lên giữa sản phẩm!
    """
    if role == "HOOK_BANNER":
        return (0.0, 0.58)
    if role == "CTA":
        return (0.0, -0.42)
    if role == "SUBTITLE" and subtitle_zone_preference == "UPPER_MIDDLE_HONGHANH":
        return (0.0, 0.46)
    if role == "SUBTITLE" and subtitle_zone_preference == "UPPER_THIRD_GRAYUNBOX":
        return (0.0, 0.58)
    if role == "SUBTITLE" and subtitle_zone_preference == "LOWER_MIDDLE_YUHTT09":
        return (0.0, -0.35)
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


def apply_dot_split_ocr_evasion(text_str: str) -> str:
    """
    [TRÍ TUỆ BẢO VỆ CHR - CHÈN DẤU CHẤM / HAI CHẤM LÁCH QUÉT OCR TỪ NHẠY CẢM & VỊ GIÁC (@3thag8_ x @minhtienoiii06)]:
    1. Tách các từ thương mại / điều trị dễ bị AI OCR của TikTok quét nhầm (@3thag8_: 'mụn' -> 'm.ụn', 'mua' -> 'm.ua').
    2. Tách các tính từ kích thích vị giác / cam kết nguồn gốc theo chuẩn Gen-Z (@minhtienoiii06 19.3M views:
       'béo ngậy' -> 'p.é.o ngậyyy', 'tan chảy' -> 't:an ch:ảy', 'hữu cơ' -> 'h.ữ.u c.ơ', 'dễ thương' -> 'd.ễ th.ư.ơ.ng').
    """
    ocr_sensitive_map = {
        r"\bmụn\b": "m.ụn",
        r"\bMụn\b": "M.ụn",
        r"\bnám\b": "n.ám",
        r"\bNám\b": "N.ám",
        r"\bthâm\b": "thâ.m",
        r"\bmờ thâm\b": "mờ thâ.m",
        r"\bdưỡng trắng\b": "dưỡng trắ.ng",
        r"\btrắng da\b": "trắ.ng da",
        r"\bsức khỏe\b": "s.ức kh.ỏe",
        r"\bmồ hôi\b": "m.ồ h.ôi",
        r"\bmua ngay\b": "m.ua ngay",
        r"\bmua\b": "m.ua",
        r"\bMua\b": "M.ua",
        r"\bgiảm cân\b": "gi.ảm c.ân",
        r"\brẻ nhất\b": "r.ẻ nh.ất",
        r"\brẻ quá\b": "r.ẻ quá",
        r"\bhoàn tiền\b": "ho.àn ti.ền",
        r"\bđiều trị\b": "cải th.iện",
        r"\bbéo ngậy\b": "p.é.o ngậyyy",
        r"\btan chảy\b": "t:an ch:ảy",
        r"\bsữa tươi\b": "sữ:a tươi",
        r"\bhữu cơ\b": "h.ữ.u c.ơ",
        r"\bdễ thương\b": "d.ễ th.ư.ơ.ng",
        r"\băn siêu cuốn\b": "ă:n siu cuốn ✨",
        r"\bngon bá cháy\b": "ngo:n b.á cháy",
        r"\bgiá chát\b": "g.i.á chát",
        r"\btặng kèm\b": "t.ặng kèm",
        r"\bsạch sâu\b": "sạ.ch sâu",
        r"\bchống ồn\b": "chố:ng ồn",
        r"\bđau mỏi\b": "đa:u mỏi",
        r"\btận (\d+)": r"t.ận \1"
    }
    out = text_str
    for pat, rep in ocr_sensitive_map.items():
        out = re.sub(pat, rep, out, flags=re.IGNORECASE if "béo" in pat or "tan" in pat or "hữu" in pat else 0)
    return out


def select_contextual_icons_and_rebus_for_product(
    text_str: str,
    product_desc: str,
    enable_rebus: bool = True,
    enable_ocr_dot_split: bool = True
) -> Dict[str, Any]:
    """
    [TRÍ TUỆ NGỮ CẢNH 4 - CHỌN ICON ĐÚNG ĐẶC TÍNH SẢN PHẨM & EMOJI-REBUS LÁCH CHR (@grayunbox x @3thag8_ x @minhtienoiii06)]:
    Tuyệt đối KHÔNG gắn icon cứng nhắc hay lệch tông sản phẩm!
    1. Phân tích ngữ nghĩa của `product_desc` + `text_str` để chọn đúng Họ Icon (Semantic Icon Family)
       trong 11 nhóm chuyên biệt (`🧸`, `🍃`, `🫧`, `🪥`, `⚡`, `📸`, `🧊`, `🎀`, `🎁`, `🗣️`, `✨`).
    2. Áp dụng Emoji-Rebus thông minh của @grayunbox & @minhtienoiii06 chỉ khi xuất hiện đúng từ khóa nhạy cảm/báo giá:
       - `khử mùi / loại bỏ mùi` -> `khử 🚮 mùi` (@grayunbox)
       - `giảm thâm / giảm mùi` -> `📉` (@grayunbox)
       - `đuổi muỗi / côn trùng` -> `🦟🥀` (@grayunbox)
       - `triệu / củ` -> `🍠` ; `nghìn / cành` -> `🐟` ; `hạt dẻ` -> `🌰` ; `giỏ hàng` -> `🛒` (@grayunbox)
       - `45k / 49k` (Đồ ăn vặt/Gen-Z) -> `45 🍅 thoi` / `49 🍠` ; `chụp ảnh` -> `📸 ảnh` (@minhtienoiii06)
    """
    combined_low = f"{product_desc} {text_str}".lower()

    # 1. Nhận diện Họ Icon theo đúng ngữ cảnh sản phẩm (11 Semantic Families)
    icon_domains = [
        {
            "domain": "ORAL_CARE_HYGIENE",
            "keywords": ["bàn chải", "kem đánh răng", "tăm nước", "niềng răng", "trắng răng", "răng miệng"],
            "primary_icon": "🪥",
            "accent_icons": ["🪥", "🫧", "✨", "🦷"],
            "floating_particles": ["🫧", "✨"]
        },
        {
            "domain": "SCENT_TEA_HERBAL",
            "keywords": ["trầm", "nhang", "sáp thơm", "nến thơm", "tinh dầu", "nước hoa", "body mist", "xịt thơm", "trà", "matcha", "thảo mộc", "ngải cứu"],
            "primary_icon": "🍃",
            "accent_icons": ["🍃", "🍵", "🌿", "✨"],
            "floating_particles": ["🍃", "🌿", "✧"]
        },
        {
            "domain": "SOAP_SKINCARE_CLEANSE",
            "keywords": ["xà phòng", "sữa rửa mặt", "sữa tắm", "tẩy tế bào", "kem", "serum", "toner", "mặt nạ", "skincare", "dưỡng ẩm", "chống nắng", "bọt"],
            "primary_icon": "🫧",
            "accent_icons": ["🫧", "✨", "💧", "🤍"],
            "floating_particles": ["🫧", "✨"]
        },
        {
            "domain": "PLUSH_TOY_STORAGE_BABY",
            "keywords": ["gấu bông", "thú bông", "đồ chơi", "kệ để", "tủ đồ", "hộp đựng", "lắp ráp", "bỉm", "tã", "em bé", "cho bé", "sơ sinh", "nệm", "đệm", "chăn", "ga gối", "drap", "gối", "chườm mắt", "bịt mắt"],
            "primary_icon": "🧸",
            "accent_icons": ["🧸", "📦", "✨", "💛"],
            "floating_particles": ["✨", "🧸"]
        },
        {
            "domain": "DRINKWARE_ICE_TUMBLER",
            "keywords": ["bình giữ nhiệt", "ly giữ nhiệt", "cốc giữ nhiệt", "bình nước", "ly nước", "đá viên", "máy xay", "sinh tố", "cốc thủy tinh", "xay đá"],
            "primary_icon": "🧊",
            "accent_icons": ["🧊", "🥤", "💧", "✨"],
            "floating_particles": ["🧊", "💧"]
        },
        {
            "domain": "GIFT_CARD_FESTIVE",
            "keywords": ["thiệp", "sinh nhật", "quà tặng", "lì xì", "tết", "kỷ niệm", "hộp quà", "thiệp 3d", "thiệp nhạc"],
            "primary_icon": "🎁",
            "accent_icons": ["🎁", "🎂", "✨", "💌"],
            "floating_particles": ["✨", "🎉"]
        },
        {
            "domain": "TRIPOD_CAMERA_SELFIE",
            "keywords": ["tripod", "gậy chụp ảnh", "gậy selfie", "giá đỡ điện thoại", "gimbal", "đèn trợ sáng", "livestream", "1m7"],
            "primary_icon": "📸",
            "accent_icons": ["📸", "💡", "🗣️", "✨"],
            "floating_particles": ["📸", "💡", "✨"]
        },
        {
            "domain": "TECH_POWER_AIRFLOW",
            "keywords": ["quạt", "sạc", "pin", "tai nghe", "loa", "micro", "mic thu âm", "lọc ồn", "17000rpm", "cấp độ gió", "máy ảnh", "digicam", "đèn", "led", "cáp", "hút bụi", "máy sấy", "chống ồn"],
            "primary_icon": "⚡",
            "accent_icons": ["⚡", "🔋", "💨", "✦"],
            "floating_particles": ["⚡", "✦"]
        },
        {
            "domain": "STATIONERY_STUDY_DESK",
            "keywords": ["sổ", "sổ tay", "planner", "bút", "bút bi", "bút gel", "hộp bút", "bóp viết", "giấy note", "văn phòng phẩm", "sticker", "kẹp tài liệu"],
            "primary_icon": "🌷",
            "accent_icons": ["🌷", "🎀", "✏️", "🌱"],
            "floating_particles": ["🌷", "🎀", "✨"]
        },
        {
            "domain": "JEWELRY_SILVER_ACCESSORY",
            "keywords": ["dây chuyền", "nhẫn", "vòng tay", "khuyên tai", "bạc", "trang sức", "moonstone", "đá quý", "gương", "kẹp tóc"],
            "primary_icon": "💍",
            "accent_icons": ["💍", "✨", "🌙", "🎀"],
            "floating_particles": ["✨", "🌙", "💍"]
        },
        {
            "domain": "FASHION_BAG_SHOE",
            "keywords": ["áo", "quần", "váy", "đầm", "túi", "ví", "giày", "dép", "cardigan", "khăn", "mũ", "kính", "phối đồ", "tất", "vớ", "hoodie", "sweater", "áo phông", "áo khoác"],
            "primary_icon": "🎀",
            "accent_icons": ["🎀", "👜", "🧦", "✨"],
            "floating_particles": ["✧", "🎀", "🤍"]
        },
        {
            "domain": "FOOD_SNACK_GOURMET",
            "keywords": ["bánh", "kẹo", "snack", "khoai tây", "phô mai", "sấy giòn", "khô gà", "socola", "ăn vặt", "mật ong", "mì", "ngũ cốc", "bánh tráng", "phồng sữa", "chip chip", "khoai môn", "sữa bột"],
            "primary_icon": "🗣️",
            "accent_icons": ["🗣️", "🍅", "🍠", "🤤"],
            "floating_particles": ["✨", "🍅", "🤤"]
        }
    ]

    selected_domain = {
        "domain": "DEFAULT_EDITORIAL",
        "primary_icon": "✨",
        "accent_icons": ["✨", "✦", "✓", "🤍"],
        "floating_particles": ["✧", "✦"]
    }
    desc_only_low = (product_desc or "").lower()
    best_hits = 0
    for dom in icon_domains:
        # Ưu tiên trọng số x2 cho từ khóa nằm trong tên/mô tả sản phẩm gốc (product_desc)
        hits = sum(
            (2 if re.search(rf"\b{re.escape(kw)}\b", desc_only_low) else 1)
            for kw in dom["keywords"]
            if re.search(rf"\b{re.escape(kw)}\b", combined_low)
        )
        if hits > best_hits:
            best_hits = hits
            selected_domain = dom

    # 2. Biến đổi Emoji-Rebus theo ngữ cảnh câu chữ (@grayunbox & @minhtienoiii06 & @yuhtt09 style)
    transformed_text = text_str
    rebus_applied: List[str] = []
    if enable_rebus and transformed_text:
        rebus_rules = [
            (r"\b(khử|loại bỏ)\s+mùi\b", r"\1 🚮 mùi", "khử/loại bỏ mùi -> 🚮 (@grayunbox)"),
            (r"\bgiảm\s+(thâm|mụn|mùi|nhờn|ngứa)\b", r"giảm 📉 \1", "giảm -> 📉 (@grayunbox)"),
            (r"\b(đuổi|diệt|trị)\s+muỗi\b", r"đuổi 🦟🥀", "đuổi muỗi -> 🦟🥀 (@grayunbox)"),
            (r"\b(\d+)\s*(k|cành)\s*/\s*(chiếc|cây|cái|đôi|món|tờ|gói)\b", r"\1 🌱/\3", "đơn giá nhỏ -> 🌱 (@yuhtt09 Sprout Price Shield)"),
            (r"\b(lẻ|combo)\s+([^|,\n]{0,18}?)(\d+)\s*(k|cành)\b", r"\1 \2\3 🐣", "so sánh giá lẻ/combo -> 🐣 (@yuhtt09 Chick Price Shield)"),
            (r"\bbằng\s+(1\s+|một\s+)?(cốc|ly)\s+trà\s+sữa\b", "bằng ly 🧋", "trà sữa -> 🧋 (@yuhtt09)"),
            (r"\bđáng\s+tiền(?!\s*💰)\b", "đáng 💰", "đáng tiền -> 💰 (@yuhtt09)"),
            (r"\blàm\s+quà(\s+tặng)?(?!\s*🎁)\b", "làm 🎁", "làm quà -> 🎁 (@yuhtt09)"),
            (r"\btest\s+nước(?!\s*💦)\b", "test 💦", "test nước -> 💦 (@yuhtt09)"),
            (r"\b(\d+)\s*củ(?!\s*🍠)\b", r"\1 củ 🍠", "củ -> 🍠 (@grayunbox)"),
            (r"\b(\d+)\s*cành(?!\s*🐟)\b", r"\1 cành 🐟", "cành -> 🐟 (@grayunbox)"),
            (r"\b(\d+)\s*k\b(?!\s*(lượt|đánh giá|người|bản|mẫu|fl|follow))", r"\1 🍅 thoi", "k -> 🍅 (@minhtienoiii06 Agricultural Price Shield)"),
            (r"\btự\s+chụp\s+ảnh\b", "tự 📸 ảnh", "chụp ảnh -> 📸 ảnh (@minhtienoiii06)"),
            (r"\bhạt dẻ(?!\s*🌰)\b", "hạt dẻ 🌰", "hạt dẻ -> 🌰 (@grayunbox)"),
            (r"\bgóc\s+trái\s+màn\s+hình(?!\s*(nè\s*)?↙️)\b", "góc trái màn hình nè ↙️", "CTA góc trái -> ↙️ (@yuhtt09)"),
            (r"\bgiỏ hàng(?!\s*🛒)\b", "giỏ hàng 🛒", "giỏ hàng -> 🛒 (@grayunbox)")
        ]
        for pat, rep, desc_note in rebus_rules:
            if re.search(pat, transformed_text, flags=re.IGNORECASE):
                transformed_text = re.sub(pat, rep, transformed_text, flags=re.IGNORECASE)
                rebus_applied.append(desc_note)

    if enable_ocr_dot_split and transformed_text:
        transformed_text = apply_dot_split_ocr_evasion(transformed_text)

    return {
        "semantic_domain": selected_domain["domain"],
        "primary_icon": selected_domain["primary_icon"],
        "accent_icons": selected_domain["accent_icons"],
        "floating_particles": selected_domain["floating_particles"],
        "transformed_text": transformed_text,
        "rebus_applied": rebus_applied
    }


def build_editorial_dual_font_title_cluster(
    script_title: str,
    sans_subtitle: str,
    left_spec: str = "",
    right_spec: str = "",
    start_sec: float = 0.0,
    end_sec: float = 2.8,
    palette_key: str = "KINFOLK_ESPRESSO_CREAM"
) -> List[dict]:
    """
    [UPGRADE #1 - BỘ TYPOGRAPHY TẠP CHÍ KÉP + VÒNG CUNG SAO + NHÃN THÔNG SỐ ĐỐI XỨNG (@byraanni x @meshinthuine)]:
    Tạo cụm tiêu đề mở đầu 4 lớp chuẩn tạp chí Kinfolk / Pinterest Editorial:
      1. Vòng cung ánh sao lấp lánh phía đỉnh (`✧ ⁀➴ ✦`, y = +0.54, FLARE loop).
      2. Chữ Tiêu đề Nghệ thuật (Calligraphy/Playfair Script Title, y = +0.44, size = 10.8).
      3. Dòng Phụ đề Tối giản bọc hộp nền Espresso/Kem (Minimalist Pill Subtitle, y = +0.33, size = 7.4).
      4. Cặp Nhãn Thông Số Bay Đối Xứng Trái/Phải quanh sản phẩm (`left_spec` tại x=-0.42, y=+0.08
         và `right_spec` tại x=+0.42, y=-0.06 với hiệu ứng TYPEWRITER/POP_UP).
    """
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["KINFOLK_ESPRESSO_CREAM"])
    cluster = [
        {
            "text": "✧ ⁀➴ ✦",
            "start_sec": start_sec,
            "end_sec": end_sec,
            "pos_x": 0.0,
            "pos_y": 0.54,
            "font_size": 8.2,
            "palette_key": palette_key,
            "role": "BLING_ACCENT",
            "anim_in": "POP_UP",
            "anim_loop": "FLARE"
        },
        {
            "text": script_title,
            "highlight_keywords": [script_title],
            "start_sec": start_sec,
            "end_sec": end_sec,
            "pos_x": 0.0,
            "pos_y": 0.44,
            "font_size": 10.8,
            "palette_key": palette_key,
            "role": "HOOK_BANNER",
            "anim_in": "SPRING",
            "anim_out": "FADE_OUT"
        },
        {
            "text": sans_subtitle,
            "start_sec": round(start_sec + 0.12, 2),
            "end_sec": end_sec,
            "pos_x": 0.0,
            "pos_y": 0.33,
            "font_size": 7.4,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        }
    ]
    if left_spec:
        cluster.append({
            "text": f"• {left_spec}",
            "start_sec": round(start_sec + 0.22, 2),
            "end_sec": end_sec,
            "pos_x": -0.42,
            "pos_y": 0.08,
            "font_size": 6.4,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "TYPEWRITER",
            "anim_out": "FADE_OUT"
        })
    if right_spec:
        cluster.append({
            "text": f"• {right_spec}",
            "start_sec": round(start_sec + 0.32, 2),
            "end_sec": end_sec,
            "pos_x": 0.42,
            "pos_y": -0.06,
            "font_size": 6.4,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "TYPEWRITER",
            "anim_out": "FADE_OUT"
        })
    return cluster

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


def create_6_archetype_zoom_keyframes(
    zoom_archetype: str,
    duration_us: int,
    base_scale: float = 1.0
) -> List[dict]:
    """
    [NEW #4 - BỘ 8 KIỂU KEYFRAME ZOOM & VI XOAY CHUYÊN NGHIỆP CỦA @kieneditcuong (146-VIDEO CATALOG)]:
    1. SLOW_PUSH_IN                  : Zoom vào chậm đều (1.0x -> 1.12x) tạo chiều sâu tự nhiên.
    2. SLOW_PULL_OUT                 : Zoom ra chậm đều (1.15x -> 1.0x) mở rộng bối cảnh bàn quay.
    3. IN_OUT_BOUNCE                 : Zoom vào rồi nhả ra theo nhịp (1.0x -> 1.18x -> 1.0x).
    4. OUT_IN_PULSE                  : Thu nhẹ rồi đẩy vào (1.15x -> 1.0x -> 1.12x).
    5. ZOOM_HOLD_READ_LABEL_4KF      : Công thức 4 Keyframe 'Ăn tiền' nhất của @kieneditcuong khi soi tem nhãn/bảng thành phần:
                                       KF1 (0.0s: 1.0x) -> KF2 (0.35s: 1.48x) -> KF3 (Giữ nguyên 1.48x suốt 1.5s) -> KF4 (Cuối clip: 1.0x).
    6. MATCH_SCALE_TRANSITION        : Đẩy nhanh ở 0.25s cuối (1.0x -> 1.36x) để nối mượt sang cảnh tiếp theo.
    7. ORGANIC_HANDHELD_3PT_ROTATION : Tuyệt chiêu 733K views (#02): 3 Keyframe Scale (1.0x -> 1.22x -> 1.12x) +
                                       Vi xoay KFTypeRotation (0° -> -3.5° -> +1.5°) kèm đường cong Ease-Out Cubic Bezier [0.16, 1.0, 0.3, 1.0]
                                       tạo cảm giác như có cameraman cầm máy thật ("thấy có cử động hẳn hem")!
    8. CON_THOI_PENDULUM_ZOOM_OUT    : Tuyệt chiêu 2.04M views (#01): Cố định góc máy trên tripod, phóng to sẵn 1.35x ở 0.0s ->
                                       kéo thu nhỏ về 1.0x ở giữa clip -> hồi nhẹ Con thoi lên 1.18x ở cuối clip.
    """
    dur = max(300_000, int(duration_us))
    s0 = float(base_scale)
    mode = (zoom_archetype or "SLOW_PUSH_IN").upper()
    rot_pts: List[Tuple[int, float]] = []

    if mode == "SLOW_PULL_OUT":
        pts = [(0, round(s0 * 1.15, 3)), (dur, s0)]
    elif mode == "CON_THOI_PENDULUM_ZOOM_OUT":
        pts = [(0, round(s0 * 1.35, 3)), (int(dur * 0.62), s0), (dur, round(s0 * 1.18, 3))]
    elif mode == "ORGANIC_HANDHELD_3PT_ROTATION":
        t_mid = min(450_000, int(dur * 0.42))
        pts = [(0, s0), (t_mid, round(s0 * 1.22, 3)), (dur, round(s0 * 1.12, 3))]
        rot_pts = [(0, 0.0), (t_mid, -3.5), (dur, 1.5)]
    elif mode == "IN_OUT_BOUNCE":
        pts = [(0, s0), (dur // 2, round(s0 * 1.18, 3)), (dur, s0)]
    elif mode == "OUT_IN_PULSE":
        pts = [(0, round(s0 * 1.15, 3)), (dur // 2, s0), (dur, round(s0 * 1.12, 3))]
    elif mode == "ZOOM_HOLD_READ_LABEL_4KF":
        t_in = min(350_000, dur // 4)
        t_hold_end = min(dur - 250_000, t_in + 1_500_000)
        if t_hold_end <= t_in:
            t_hold_end = int(dur * 0.75)
        zoom_lvl = round(s0 * 1.48, 3)
        pts = [(0, s0), (t_in, zoom_lvl), (t_hold_end, zoom_lvl), (dur, s0)]
    elif mode == "MATCH_SCALE_TRANSITION":
        t_ramp = max(0, dur - 250_000)
        pts = [(0, s0), (t_ramp, round(s0 * 1.05, 3)), (dur, round(s0 * 1.36, 3))]
    else:
        pts = [(0, s0), (dur, round(s0 * 1.12, 3))]

    kfs = []
    for prop in ("KFTypeScaleX", "KFTypeScaleY"):
        kf_list = []
        for t_off, val in pts:
            kf_list.append({
                "id": uid(),
                "time_offset": int(t_off),
                "values": [float(val)],
                "curveType": "CubicBezier" if mode in ("ORGANIC_HANDHELD_3PT_ROTATION", "CON_THOI_PENDULUM_ZOOM_OUT") else "Line",
                "graphID": "",
                "left_control": {"x": 0.16, "y": 1.0} if mode in ("ORGANIC_HANDHELD_3PT_ROTATION", "CON_THOI_PENDULUM_ZOOM_OUT") else {"x": 0.0, "y": 0.0},
                "right_control": {"x": 0.30, "y": 1.0} if mode in ("ORGANIC_HANDHELD_3PT_ROTATION", "CON_THOI_PENDULUM_ZOOM_OUT") else {"x": 0.0, "y": 0.0}
            })
        kfs.append({"id": uid(), "property_type": prop, "keyframe_list": kf_list})

    if rot_pts:
        rot_kf_list = []
        for t_off, r_val in rot_pts:
            rot_kf_list.append({
                "id": uid(),
                "time_offset": int(t_off),
                "values": [float(r_val)],
                "curveType": "CubicBezier",
                "graphID": "",
                "left_control": {"x": 0.16, "y": 1.0},
                "right_control": {"x": 0.30, "y": 1.0}
            })
        kfs.append({"id": uid(), "property_type": "KFTypeRotation", "keyframe_list": rot_kf_list})

    return kfs


def inject_dashed_circle_magnifier_pip(
    edit_plan: dict,
    source_file: str,
    source_in_sec: float,
    timeline_start_sec: float,
    duration_sec: float = 2.4,
    detail_label: str = "4 mức gió • cổng sạc kín",
    loupe_pos_x: float = 0.28,
    loupe_pos_y: float = 0.22,
    zoom_scale: float = 1.62,
    palette_key: str = "KINFOLK_ESPRESSO_CREAM"
) -> dict:
    """
    [NEW #1 - KÍNH LÚP HÌNH TRÒN VIỀN NÉT ĐỨT PHÓNG ĐẠI CHI TIẾT 162% (@byraanni SIGNATURE)]:
    Khi sản phẩm có chi tiết cơ học nhỏ (nút bấm 4 cấp độ, cổng sạc chống nước, đầu cọ, chất kem),
    tự động tạo:
      1. Một lớp Video PIP trên Track V2 (`is_pip: True`) cắt mặt nạ Hình Tròn (`CAPCUT_MASKS['CIRCLE']`),
         phóng đại `1.62x` vào đúng chi tiết sản phẩm.
      2. Một vòng tròn viền nét đứt (`◌`) bao quanh mặt nạ tròn.
      3. Một nhãn thông số nhỏ (`● {detail_label}`) đính ngay trên đỉnh vòng tròn kèm tiếng `soft_pop`.
    """
    v_list = edit_plan.setdefault("video_timeline", [])
    t_list = edit_plan.setdefault("text_overlays", [])
    aud_list = edit_plan.setdefault("audio_tracks", [])

    end_sec = round(timeline_start_sec + duration_sec, 2)
    pip_seg = {
        "source_file": source_file,
        "source_in_sec": round(source_in_sec, 2),
        "source_out_sec": round(source_in_sec + duration_sec, 2),
        "timeline_start_sec": round(timeline_start_sec, 2),
        "timeline_end_sec": end_sec,
        "is_pip": True,
        "scale": zoom_scale,
        "scale_end": round(zoom_scale * 1.04, 3),
        "pos_x": loupe_pos_x,
        "pos_y": loupe_pos_y,
        "mask": "CIRCLE",
        "mask_config": {
            "mask_key": "CIRCLE",
            "center_x": 0.0,
            "center_y": 0.0,
            "width": 0.42,
            "height": 0.42,
            "feather": 0.02
        },
        "video_anim": "MINI_ZOOM",
        "native_volume": 0.0
    }
    v_list.append(pip_seg)

    # Vòng tròn viền nét đứt bao quanh Kính lúp
    t_list.append({
        "text": "◌",
        "start_sec": round(timeline_start_sec, 2),
        "end_sec": end_sec,
        "pos_x": loupe_pos_x,
        "pos_y": loupe_pos_y,
        "font_size": 24.0,
        "palette_key": palette_key,
        "role": "BLING_ACCENT",
        "anim_in": "POP_UP",
        "anim_out": "FADE_OUT"
    })
    # Nhãn micro-label đính trên đỉnh vòng tròn (@byraanni style: "● ada 4 speed level")
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["KINFOLK_ESPRESSO_CREAM"])
    t_list.append({
        "text": f"● {detail_label}",
        "start_sec": round(timeline_start_sec + 0.08, 2),
        "end_sec": end_sec,
        "pos_x": loupe_pos_x,
        "pos_y": round(min(0.72, loupe_pos_y + 0.24), 2),
        "font_size": 6.2,
        "bg_color": pal["pill_bg_hex"],
        "palette_key": palette_key,
        "role": "CALLOUT",
        "anim_in": "POP_UP",
        "anim_out": "FADE_OUT"
    })

    sfx_vault = ensure_studio_sfx_pack("./workspace/sfx_studio")
    if "soft_pop" in sfx_vault:
        aud_list.append({
            "source_file": sfx_vault["soft_pop"],
            "start_sec": round(timeline_start_sec, 2),
            "end_sec": round(timeline_start_sec + 0.15, 2),
            "role": "SFX",
            "volume": 0.26
        })
    return edit_plan


def inject_chr_shield_and_brand_watermark_tracks(
    edit_plan: dict,
    total_dur_sec: float,
    creator_handle: str = "",
    product_archetype: str = "P1",
    has_flash_sale_price: bool = False,
    enable_dot_split_ocr: bool = True
) -> dict:
    """
    [NEW #2 - LÁ CHẮN BẢO VỆ CHR TỰ ĐỘNG & WATERMARK KÉP CHỐNG REUP (@3thag8_ x @byraanni)]:
    1. Nếu `enable_dot_split_ocr=True`: Tự động chấm tách các từ nhạy cảm trên màn hình (`m.ụn`, `m.ua`, `tr.ắng da`).
    2. Nếu ngành hàng là Mỹ phẩm/Skincare (`P1`) hoặc TPCN (`P7`): Tự động ghim dòng chữ nhỏ
       `*hiệu quả sản phẩm tuỳ vào cơ địa mỗi người*` ở sát đáy an toàn (`y = -0.55`, `font_size = 4.8`, `alpha = 0.72`).
    3. Nếu có báo giá/CTKM (`has_flash_sale_price=True`): Tự động ghim `*giá có thể thay đổi khi CTKM kết thúc*`
       giúp miễn nhiễm 100% lỗi Lệch giá biến thể (-20đ CHR).
    4. Nếu truyền `creator_handle`: Đóng Watermark kép chống Reup ở góc đỉnh (`@handle • don't repost!`, `y = +0.80`)
       và góc dưới (`video milik : @handle`, `y = -0.44`) với độ mờ `alpha = 0.65`.
    """
    t_list = edit_plan.setdefault("text_overlays", [])
    dur = max(5.0, float(total_dur_sec))

    if enable_dot_split_ocr:
        for txt in t_list:
            if "text" in txt and txt.get("role") != "CHR_SHIELD":
                txt["text"] = apply_dot_split_ocr_evasion(txt["text"])

    existing_texts_low = " ".join(t.get("text", "").lower() for t in t_list)
    if product_archetype in ("P1", "P7") and "tuỳ vào cơ địa" not in existing_texts_low:
        t_list.append({
            "text": "*hiệu quả sản phẩm tuỳ vào cơ địa mỗi người*",
            "start_sec": 0.5,
            "end_sec": round(dur - 0.2, 2),
            "pos_x": 0.0,
            "pos_y": -0.55,
            "font_size": 4.8,
            "alpha": 0.72,
            "role": "CHR_SHIELD"
        })

    if has_flash_sale_price and "ctkm kết thúc" not in existing_texts_low:
        t_list.append({
            "text": "*giá và ưu đãi có thể thay đổi khi CTKM kết thúc*",
            "start_sec": 0.5,
            "end_sec": round(dur - 0.2, 2),
            "pos_x": 0.0,
            "pos_y": -0.59,
            "font_size": 4.6,
            "alpha": 0.70,
            "role": "CHR_SHIELD"
        })

    if creator_handle:
        clean_handle = creator_handle.lstrip("@")
        t_list.append({
            "text": f"@{clean_handle} • don't repost!",
            "start_sec": 0.0,
            "end_sec": round(dur, 2),
            "pos_x": 0.0,
            "pos_y": 0.76,
            "font_size": 5.0,
            "alpha": 0.65,
            "role": "WATERMARK"
        })
        t_list.append({
            "text": f"video thuộc về : @{clean_handle}",
            "start_sec": 0.0,
            "end_sec": round(dur, 2),
            "pos_x": 0.0,
            "pos_y": -0.45,
            "font_size": 4.8,
            "alpha": 0.62,
            "role": "WATERMARK"
        })
    return edit_plan


def inject_3s_visual_hook_and_radial_loop_outro(
    edit_plan: dict,
    hook_style: str = "BYRAANNI_3SHOT_COLLAGE",
    enable_radial_blur_loop_outro: bool = True
) -> dict:
    """
    [NEW #3 - BỘ MÓC CÂU THỊ GIÁC 3 GIÂY ĐẦU (@kieneditcuong x @byraanni) & VÒNG LẶP VÔ TẬN RADIAL BLUR (@3thag8_)]:
    Hỗ trợ các preset mở đầu 3s ăn tiền nhất:
      - `BYRAANNI_3SHOT_COLLAGE` : Gắn chuyển cảnh nhẹ + hiệu ứng `CAMERA_FOCUS` + tiếng `shutter` cho 3 cảnh 1.1s đầu.
      - `KIEN_GLOW_STROKE_FREEZE`: Bơm kỹ xảo `EDGE_GLOW` (Viền phát quang chủ thể) + `BLURRY_FOCUS` (Làm mờ nền) ở 1.5s đầu.
      - `KIEN_GHOST_OPACITY_51`  : Tạo lớp bóng mờ `alpha=0.51` trượt khớp vào chủ thể chính ở 1.2s đầu.
    Và ở 0.3s cuối cùng của Track V1:
      - Tự động gắn `RADIAL_BLUR` + `MATCH_SCALE_TRANSITION (1.0x -> 1.36x)` để cuốn người xem quay lại Cảnh 1 mượt 100%!
    """
    v_list = edit_plan.setdefault("video_timeline", [])
    fx_list = edit_plan.setdefault("scene_effects", [])
    v1_clips = [c for c in v_list if not c.get("is_pip")]

    style = (hook_style or "BYRAANNI_3SHOT_COLLAGE").upper()
    if style == "KIEN_GLOW_STROKE_FREEZE":
        fx_list.append({"effect_key": "BLURRY_FOCUS", "start_sec": 0.0, "end_sec": 1.4})
        fx_list.append({"effect_key": "EDGE_GLOW", "start_sec": 0.0, "end_sec": 1.4})
        if v1_clips:
            v1_clips[0]["video_anim"] = "ENLARGE_BOUNCE"
    elif style == "KIEN_GHOST_OPACITY_51" and v1_clips:
        first = v1_clips[0]
        ghost_pip = dict(first)
        ghost_pip.update({
            "is_pip": True,
            "timeline_start_sec": 0.0,
            "timeline_end_sec": min(1.2, first.get("timeline_end_sec", 1.5)),
            "scale": round(float(first.get("scale", 1.0)) * 1.16, 3),
            "scale_end": float(first.get("scale", 1.0)),
            "alpha": 0.51,
            "video_anim": "SLIDE_UP",
            "native_volume": 0.0
        })
        v_list.append(ghost_pip)
    elif style == "BYRAANNI_3SHOT_COLLAGE":
        fx_list.append({"effect_key": "CAMERA_FOCUS", "start_sec": 0.0, "end_sec": 1.1})
        if v1_clips:
            v1_clips[0]["zoom_archetype"] = "SLOW_PUSH_IN"

    if enable_radial_blur_loop_outro and v1_clips:
        last_clip = v1_clips[-1]
        last_clip["transition"] = "RADIAL_BLUR"
        last_clip["zoom_archetype"] = "MATCH_SCALE_TRANSITION"

    return edit_plan


def apply_koc_color_grade_and_6_zoom_keyframes(
    edit_plan: dict,
    color_preset_key: str = "BYRAANNI_KINFOLK_ESPRESSO",
    default_zoom_cycle: Optional[List[str]] = None
) -> dict:
    """
    [NEW #4 - ÁP DỤNG CÔNG THỨC MÀU KOC MASTER & LUÂN PHIÊN 6 KIỂU KEYFRAME ZOOM]:
    1. Đính kèm bộ thông số Color Adjust + HSL Da (`KOC_COLOR_GRADE_PRESETS`) vào `edit_plan["koc_color_grade"]`.
    2. Tự động phân bổ 6 kiểu Keyframe Zoom của @kieneditcuong lên từng clip trên Track V1
       (Đặc biệt ưu tiên `ZOOM_HOLD_READ_LABEL_4KF` cho cảnh soi tem nhãn/thành phần dài >= 2.2s!).
    """
    preset = KOC_COLOR_GRADE_PRESETS.get(color_preset_key, KOC_COLOR_GRADE_PRESETS["BYRAANNI_KINFOLK_ESPRESSO"])
    edit_plan["koc_color_grade"] = preset

    cycle = default_zoom_cycle or [
        "ORGANIC_HANDHELD_3PT_ROTATION",
        "CON_THOI_PENDULUM_ZOOM_OUT",
        "ZOOM_HOLD_READ_LABEL_4KF",
        "IN_OUT_BOUNCE",
        "SLOW_PULL_OUT",
        "OUT_IN_PULSE",
        "SLOW_PUSH_IN",
        "MATCH_SCALE_TRANSITION"
    ]
    v1_idx = 0
    for seg in edit_plan.get("video_timeline", []):
        if seg.get("is_pip"):
            continue
        seg["color_grade_preset"] = color_preset_key
        if not seg.get("zoom_archetype"):
            dur = float(seg.get("timeline_end_sec", 0.0)) - float(seg.get("timeline_start_sec", 0.0))
            if dur >= 2.3 and v1_idx in (1, 2, 3):
                seg["zoom_archetype"] = "ZOOM_HOLD_READ_LABEL_4KF"
            else:
                seg["zoom_archetype"] = cycle[v1_idx % len(cycle)]
        v1_idx += 1
    return edit_plan


def inject_grayunbox_contextual_vfx_and_pips(
    edit_plan: dict,
    product_desc: str,
    enable_bonus_gift_freeze_frame: bool = False,
    bonus_gift_label: str = "🎁 Tặng kèm quà xịn!",
    freeze_at_sec: float = 3.5,
    enable_scent_or_bubble_particles: bool = False,
    outdoor_skin_proof_clip: Optional[str] = None,
    palette_key: str = "GRAYUNBOX_CLEAN_MINIMAL"
) -> dict:
    """
    [NEW #5 - BỘ KỸ XẢO NGỮ CẢNH @grayunbox: MANGA FREEZE-FRAME QUÀ TẶNG, HẠT HƯƠNG BAY & PIP CAM THƯỜNG NGOÀI NẮNG]:
    Chỉ kích hoạt đúng hiệu ứng khi sản phẩm thực sự có tính chất tương ứng:
    1. `enable_bonus_gift_freeze_frame`: Khi sản phẩm có quà tặng kèm ("mua X tặng Y"), tự động tạo điểm nhấn
       Freeze-Frame / Camera Shutter 0.45s tại `freeze_at_sec` (~3.5s) kèm nhãn `"🎁 {bonus_gift_label}"` + tiếng `shutter`.
    2. `enable_scent_or_bubble_particles`: Khi sản phẩm là Trầm hương / Sáp thơm / Nước hoa / Trà (`🍃`) hoặc Xà phòng / Sữa rửa mặt (`🫧`),
       tự động thả các hạt Icon lơ lửng (`FLARE` loop) bên rìa khung hình lúc bàn tay quạt hương hoặc tạo bọt.
    3. `outdoor_skin_proof_clip`: Khi review Mỹ phẩm / Xà phòng / Kem dưỡng và có clip quay da thật dưới nắng tự nhiên,
       tự động chèn cửa sổ PIP bo góc (`RECTANGLE` mask, `round_corner=0.30`) kèm nhãn `"☀️ Cam thường dưới nắng"`.
    """
    v_list = edit_plan.setdefault("video_timeline", [])
    t_list = edit_plan.setdefault("text_overlays", [])
    fx_list = edit_plan.setdefault("scene_effects", [])
    aud_list = edit_plan.setdefault("audio_tracks", [])
    sfx_vault = ensure_studio_sfx_pack("./workspace/sfx_studio")
    icon_info = select_contextual_icons_and_rebus_for_product("", product_desc, enable_rebus=False, enable_ocr_dot_split=False)
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["GRAYUNBOX_CLEAN_MINIMAL"])

    # 1. Manga Sketch / Shutter Freeze-Frame khi khoe Quà Tặng Kèm tại giây ~3.5s
    if enable_bonus_gift_freeze_frame:
        fx_list.append({
            "effect_key": "CAMERA_FOCUS",
            "start_sec": round(freeze_at_sec, 2),
            "end_sec": round(freeze_at_sec + 0.55, 2)
        })
        t_list.append({
            "text": bonus_gift_label,
            "start_sec": round(freeze_at_sec, 2),
            "end_sec": round(freeze_at_sec + 1.85, 2),
            "pos_x": 0.0,
            "pos_y": 0.28,
            "font_size": 8.4,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "BOUNCE_IN",
            "anim_out": "FADE_OUT"
        })
        if "shutter" in sfx_vault:
            aud_list.append({
                "source_file": sfx_vault["shutter"],
                "start_sec": round(freeze_at_sec, 2),
                "end_sec": round(freeze_at_sec + 0.14, 2),
                "role": "SFX",
                "volume": 0.30
            })

    # 2. Hạt Hương Thơm / Bọt Bong Bóng Lơ Lửng (`🍃` / `🫧`) khi quạt tay thử mùi hoặc tạo bọt
    if enable_scent_or_bubble_particles:
        particles = icon_info["floating_particles"]
        p1 = particles[0] if particles else "🍃"
        p2 = particles[1] if len(particles) > 1 else "✨"
        t_list.append({
            "text": f"{p1}  {p2}",
            "start_sec": 6.2,
            "end_sec": 10.5,
            "pos_x": -0.36,
            "pos_y": 0.16,
            "font_size": 9.8,
            "palette_key": palette_key,
            "role": "BLING_ACCENT",
            "anim_in": "POP_UP",
            "anim_loop": "FLARE",
            "anim_out": "FADE_OUT"
        })
        t_list.append({
            "text": f"{p2}  {p1}",
            "start_sec": 6.6,
            "end_sec": 10.8,
            "pos_x": 0.36,
            "pos_y": 0.24,
            "font_size": 9.2,
            "palette_key": palette_key,
            "role": "BLING_ACCENT",
            "anim_in": "POP_UP",
            "anim_loop": "FLARE",
            "anim_out": "FADE_OUT"
        })

    # 3. Cửa sổ PIP Bằng Chứng Da Thật Ngoài Nắng Tự Nhiên (@grayunbox #07)
    if outdoor_skin_proof_clip and os.path.exists(outdoor_skin_proof_clip):
        v_list.append({
            "source_file": outdoor_skin_proof_clip,
            "source_in_sec": 0.5,
            "source_out_sec": 4.0,
            "timeline_start_sec": 13.0,
            "timeline_end_sec": 16.5,
            "is_pip": True,
            "scale": 0.52,
            "scale_end": 0.55,
            "pos_x": 0.26,
            "pos_y": -0.10,
            "mask": "RECTANGLE",
            "mask_config": {
                "mask_key": "RECTANGLE",
                "center_x": 0.0,
                "center_y": 0.0,
                "width": 0.46,
                "height": 0.54,
                "feather": 0.01,
                "round_corner": 0.30
            },
            "video_anim": "SLIDE_UP",
            "native_volume": 0.0
        })
        t_list.append({
            "text": "☀️ Cam thường dưới nắng thật",
            "start_sec": 13.1,
            "end_sec": 16.5,
            "pos_x": 0.26,
            "pos_y": 0.20,
            "font_size": 6.0,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })

    return edit_plan


def inject_minhtienoiii_sensory_and_ruler_vfx(
    edit_plan: dict,
    product_desc: str,
    enable_dashed_height_ruler: bool = False,
    ruler_height_label: str = "1m7",
    ruler_at_sec: float = 8.0,
    enable_dialect_debate_hook: bool = False,
    debate_pair_text: str = "Bịch ❌  |  Bao ✅ — Cho hỏi là Bịch hay Bao ?",
    palette_key: str = "MINHTIENOIII_GENZ_SENSORY_POP"
) -> dict:
    """
    [NEW #6 - BỘ KỸ XẢO NGỮ CẢNH @minhtienoiii06 (19.3M & 15.5M VIEWS): THƯỚC ĐO NÉT ĐỨT 1M7 & HOOK TRANH LUẬN VÙNG MIỀN]:
    1. `enable_dashed_height_ruler`: Khi review Tripod / Gậy chụp ảnh / Kệ cao có thông số chiều dài (VD: `1m7`, `1m5`),
       tự động vẽ đường kẻ nét đứt dọc/ngang (`< - - - 1m7 - - - >`) kèm hiệu ứng `TYPEWRITER` + tiếng `magnifier_loupe_zoom.wav`.
    2. `enable_dialect_debate_hook`: Khi review Đồ ăn vặt / Bánh tráng / Bánh phồng sữa, tự động gắn thẻ Hook tranh luận
       kích nổ bình luận (`Bịch ❌ | Bao ✅`) hoặc huy hiệu `🗣️` chữ thường kèm tiếng `ping_pong_question.wav` + `ui_double_pop.wav`.
    """
    t_list = edit_plan.setdefault("text_overlays", [])
    aud_list = edit_plan.setdefault("audio_tracks", [])
    sfx_vault = discover_and_index_hybrid_sfx_vault("./workspace/sfx_studio")
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["MINHTIENOIII_GENZ_SENSORY_POP"])

    if enable_dialect_debate_hook:
        t_list.append({
            "text": debate_pair_text,
            "start_sec": 0.15,
            "end_sec": 2.45,
            "pos_x": 0.0,
            "pos_y": 0.48,
            "font_size": 7.6,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "BOUNCE_IN",
            "anim_out": "FADE_OUT"
        })
        for s_key, offset_t in (("ping_pong_question", 0.08), ("ui_double_pop", 0.25)):
            if s_key in sfx_vault:
                aud_list.append({
                    "source_file": sfx_vault[s_key],
                    "start_sec": round(offset_t, 2),
                    "end_sec": round(offset_t + 0.22, 2),
                    "role": "SFX",
                    "volume": 0.28
                })

    if enable_dashed_height_ruler:
        t_list.append({
            "text": f"⇠ - - - -  {ruler_height_label}  - - - - ⇢",
            "start_sec": round(ruler_at_sec, 2),
            "end_sec": round(ruler_at_sec + 2.4, 2),
            "pos_x": 0.22,
            "pos_y": 0.05,
            "font_size": 7.8,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "TYPEWRITER",
            "anim_out": "FADE_OUT"
        })
        if "magnifier_loupe_zoom" in sfx_vault:
            aud_list.append({
                "source_file": sfx_vault["magnifier_loupe_zoom"],
                "start_sec": round(ruler_at_sec, 2),
                "end_sec": round(ruler_at_sec + 0.28, 2),
                "role": "SFX",
                "volume": 0.26
            })

    return edit_plan


def inject_yuhtt09_coquette_unbox_and_proof_vfx(
    edit_plan: dict,
    product_desc: str,
    enable_arch_curved_title_kaomoji: bool = False,
    arch_title_text: str = "⌒ Unbox đồ xinh ⌒",
    enable_shop_rating_pill: bool = False,
    rating_pill_text: str = "⭐ 4.9/5 (2.1k)  |  Đã bán 23.6K",
    enable_combo_or_3in1_badge: bool = False,
    combo_badge_text: str = "3in1: Chống nắng + Primer + Nền ✨",
    enable_water_tissue_blot_callout: bool = False,
    water_blot_at_sec: float = 11.5,
    enable_numbered_feature_badges: bool = False,
    palette_key: str = "YUHTT09_COQUETTE_CLEAN_WHITE_PILL"
) -> dict:
    """
    [NEW #6B - BỘ KỸ XẢO NGỮ CẢNH @yuhtt09 (54-VIDEO DNA & 2026 EVOLUTION):
     TIÊU ĐỀ VÒM KAOMOJI, HUY HIỆU ĐÁNH GIÁ TIKTOK SHOP, SO SÁNH LẺ/COMBO 3IN1 & TEST NƯỚC KHĂN GIẤY KHÔ]:
      1. `enable_arch_curved_title_kaomoji`: Chèn cụm tiêu đề vòm `⌒` kèm dải Kaomoji `*ੈ✩‧₊˚🌷🎀*ੈ✩‧₊˚` ở 1.3s đầu.
      2. `enable_shop_rating_pill`: Chèn thanh đánh giá uy tín `⭐ 4.9/5 (2.1k) | Đã bán 23.6K` cho Thời trang/Túi xách/Tất vớ (#23).
      3. `enable_combo_or_3in1_badge`: Chèn thẻ so sánh giá `❌ Lẻ gần 300 🐣 | ✅ Combo hời 🐣` (#51) hoặc công thức `3in1` (#52).
      4. `enable_water_tissue_blot_callout`: Chèn nhãn kiểm chứng `💦 Test nước + Áp khăn giấy khô: Không lem trôi!` (#03, #06, #14, #54).
      5. `enable_numbered_feature_badges`: Chèn huy hiệu đếm tính năng `① Thiết kế nhỏ gọn` -> `② Đa năng tiện lợi` (#10, #16, #31).
    """
    t_list = edit_plan.setdefault("text_overlays", [])
    aud_list = edit_plan.setdefault("audio_tracks", [])
    sfx_vault = discover_and_index_hybrid_sfx_vault("./workspace/sfx_studio")
    pal = LUXURY_TYPOGRAPHY_PALETTES.get(palette_key, LUXURY_TYPOGRAPHY_PALETTES["YUHTT09_COQUETTE_CLEAN_WHITE_PILL"])

    if enable_arch_curved_title_kaomoji:
        t_list.append({
            "text": "*ੈ✩‧₊˚ 🌷 🎀 *ੈ✩‧₊˚",
            "start_sec": 0.0,
            "end_sec": 1.45,
            "pos_x": 0.0,
            "pos_y": 0.52,
            "font_size": 7.4,
            "palette_key": palette_key,
            "role": "BLING_ACCENT",
            "anim_in": "POP_UP",
            "anim_loop": "FLARE",
            "anim_out": "FADE_OUT"
        })
        t_list.append({
            "text": arch_title_text,
            "start_sec": 0.05,
            "end_sec": 1.45,
            "pos_x": 0.0,
            "pos_y": 0.42,
            "font_size": 9.2,
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "SPRING",
            "anim_out": "FADE_OUT"
        })

    if enable_shop_rating_pill:
        t_list.append({
            "text": rating_pill_text,
            "start_sec": 0.15,
            "end_sec": 2.35,
            "pos_x": 0.0,
            "pos_y": 0.32,
            "font_size": 6.8,
            "bg_color": "#1E2229",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })
        if "ui_double_pop" in sfx_vault:
            aud_list.append({
                "source_file": sfx_vault["ui_double_pop"],
                "start_sec": 0.15,
                "end_sec": 0.37,
                "role": "SFX",
                "volume": 0.26
            })

    if enable_combo_or_3in1_badge:
        t_list.append({
            "text": combo_badge_text,
            "start_sec": 1.55,
            "end_sec": 4.20,
            "pos_x": 0.0,
            "pos_y": 0.44,
            "font_size": 7.2,
            "bg_color": pal["pill_bg_hex"],
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "BOUNCE_IN",
            "anim_out": "FADE_OUT"
        })

    if enable_water_tissue_blot_callout:
        t_list.append({
            "text": "💦 Test nước + Áp khăn giấy khô: Không lem trôi ✓",
            "start_sec": round(water_blot_at_sec, 2),
            "end_sec": round(water_blot_at_sec + 2.8, 2),
            "pos_x": 0.0,
            "pos_y": 0.36,
            "font_size": 7.0,
            "bg_color": "#18222D",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })
        if "water_pour_splash_test" in sfx_vault:
            aud_list.append({
                "source_file": sfx_vault["water_pour_splash_test"],
                "start_sec": round(water_blot_at_sec, 2),
                "end_sec": round(water_blot_at_sec + 0.38, 2),
                "role": "SFX",
                "volume": 0.28
            })

    if enable_numbered_feature_badges:
        t_list.append({
            "text": "① Thiết kế chỉn chu • tiện lợi",
            "start_sec": 4.6,
            "end_sec": 7.0,
            "pos_x": -0.22,
            "pos_y": 0.28,
            "font_size": 6.6,
            "bg_color": "#1E2229",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })
        t_list.append({
            "text": "② Chất lượng vượt tầm giá ✨",
            "start_sec": 7.1,
            "end_sec": 9.6,
            "pos_x": 0.22,
            "pos_y": 0.28,
            "font_size": 6.6,
            "bg_color": "#1E2229",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })

    return edit_plan


def select_smart_contextual_audio_and_sfx_plan(
    edit_plan: dict,
    product_desc: str,
    semantic_domain: str,
    color_preset: str,
    total_dur_sec: float = 24.0
) -> Dict[str, Any]:
    """
    [NEW #7 - BỘ ĐIỀU PHỐI ÂM THANH, NHẠC NỀN (BGM) & 42 FOLEY SFX NGỮ CẢNH THÔNG MINH 8 KOC]:
    Đọc trực tiếp từ kho ổ đĩa đã tải sẵn:
      - `./knowledge_vault/koc_bgm_and_audio_library_registry.json` (8 bản BGM chuẩn gu 8 KOC)
      - `./knowledge_vault/external_custom_sfx_registry.json` (42 file SFX/Foley thực chiến)
    Tự động chọn đúng bản Nhạc nền (BGM) + gắn đúng các file `.wav` Foley/SFX theo ngữ nghĩa sản phẩm,
    đảm bảo 100% dự án CapCut xuất ra luôn có đầy đủ Nhạc nền và Hiệu ứng Âm thanh sống động!
    """
    aud_list = edit_plan.setdefault("audio_tracks", [])
    sfx_vault = discover_and_index_hybrid_sfx_vault("./workspace/sfx_studio")
    desc_low = (product_desc or "").lower()

    # 1. Chọn Bản Nhạc Nền (BGM) Chuẩn Gu 8 KOC từ ./knowledge_vault/koc_bgm_and_audio_library_registry.json
    bgm_reg_path = "./knowledge_vault/koc_bgm_and_audio_library_registry.json"
    bgm_tracks = {}
    if os.path.exists(bgm_reg_path):
        try:
            with open(bgm_reg_path, "r", encoding="utf-8") as f:
                bgm_tracks = json.load(f).get("koc_bgm_tracks", {})
        except Exception:
            pass

    if semantic_domain in ("STATIONERY_STUDY_DESK", "JEWELRY_SILVER_ACCESSORY") or color_preset.startswith("YUHTT09"):
        target_bgm_key = "bgm_v8_yuhtt09_spedup_kpop_coquette_pluck_130bpm"
    elif semantic_domain in ("FOOD_SNACK_GOURMET", "TRIPOD_CAMERA_SELFIE") or color_preset.startswith("MINHTIENOIII"):
        target_bgm_key = "bgm_v7_minhtienoiii_healing_farm_orchestra_124bpm"
    elif color_preset.startswith("GRAYUNBOX") or semantic_domain in ("SCENT_TEA_HERBAL", "ORAL_CARE_HYGIENE", "GIFT_CARD_FESTIVE"):
        target_bgm_key = "bgm_v6_grayunbox_holiday_breakfast_jazz_112bpm"
    elif color_preset.startswith("BYRAANNI") or semantic_domain in ("FASHION_BAG_SHOE", "DRINKWARE_ICE_TUMBLER"):
        target_bgm_key = "bgm_v5_byraanni_pinterest_editorial_rnb_102bpm"
    elif color_preset.startswith("HONGHANH"):
        target_bgm_key = "bgm_v2_honghanh_kawaii_lofi_pluck_116bpm"
    elif color_preset.startswith("3THAG8") or semantic_domain in ("SOAP_SKINCARE_CLEANSE", "TECH_POWER_AIRFLOW"):
        target_bgm_key = "bgm_v4_3thag8_classical_minuet_bounce_118bpm"
    else:
        target_bgm_key = "bgm_v1_meshinthuine_warm_indie_acoustic_108bpm"

    bgm_info = bgm_tracks.get(target_bgm_key, {})
    bgm_file = bgm_info.get("file_path", "")
    has_existing_bgm = any(a.get("role") == "BGM" for a in aud_list)
    if bgm_file and os.path.exists(bgm_file) and not has_existing_bgm:
        aud_list.append({
            "source_file": bgm_file,
            "start_sec": 0.0,
            "end_sec": round(min(32.0, max(5.0, total_dur_sec)), 2),
            "role": "BGM",
            "volume": 0.14,
            "bgm_key": target_bgm_key,
            "koc_reference": bgm_info.get("koc_handle", "@meshinthuine")
        })

    # 2. Chọn bộ Foley & Kinetic SFX theo đúng đặc tính vật lý của sản phẩm (50 File .wav Chuẩn 8 KOC)
    contextual_sfx_schedule: List[Tuple[str, float, float, float]] = []
    # (sfx_key, start_sec, duration_sec, volume)
    if semantic_domain == "STATIONERY_STUDY_DESK":
        contextual_sfx_schedule.extend([
            ("box_cutter_tape_slice", 1.15, 0.26, 0.28),
            ("bubble_wrap_unroll_pop", min(2.8, total_dur_sec * 0.20), 0.21, 0.26),
            ("pen_click_and_paper_write", min(5.5, total_dur_sec * 0.38), 0.14, 0.30),
            ("sfx_kien_poyo_kawaii_skin_touch_bounce", min(7.4, total_dur_sec * 0.48), 0.22, 0.26),
            ("zipper_slide_bag_smooth", min(9.2, total_dur_sec * 0.60), 0.25, 0.26),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    elif semantic_domain == "JEWELRY_SILVER_ACCESSORY":
        contextual_sfx_schedule.extend([
            ("crystal_aha_shimmer", 0.08, 0.28, 0.28),
            ("screen_seal_peel_smooth", min(2.4, total_dur_sec * 0.18), 0.34, 0.28),
            ("box_cutter_tape_slice", min(5.2, total_dur_sec * 0.38), 0.26, 0.25),
            ("sfx_kien_money_chakin_deal_alert", min(7.2, total_dur_sec * 0.48), 0.32, 0.26),
            ("magnifier_loupe_zoom", min(8.8, total_dur_sec * 0.58), 0.28, 0.26),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    elif semantic_domain == "FASHION_BAG_SHOE":
        contextual_sfx_schedule.extend([
            ("box_cutter_tape_slice", 1.15, 0.26, 0.26),
            ("zipper_slide_bag_smooth", min(3.6, total_dur_sec * 0.25), 0.25, 0.28),
            ("ui_double_pop", min(6.5, total_dur_sec * 0.45), 0.22, 0.26),
            ("sfx_kien_pac_low_telop_subtitle_pop", min(8.2, total_dur_sec * 0.55), 0.11, 0.26),
            ("camera_shutter_clean", min(10.0, total_dur_sec * 0.65), 0.08, 0.28),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    elif semantic_domain == "SCENT_TEA_HERBAL":
        contextual_sfx_schedule.extend([
            ("fine_mist_spray_shimmer", 0.25, 0.28, 0.30),
            ("snack_bag_crinkle_open", min(3.2, total_dur_sec * 0.22), 0.75, 0.25),
            ("paper_tear_manga_sketch", min(6.8, total_dur_sec * 0.45), 0.35, 0.26),
            ("cart_gold_chime", max(1.5, total_dur_sec - 2.2), 0.32, 0.28)
        ])
    elif semantic_domain == "FOOD_SNACK_GOURMET":
        contextual_sfx_schedule.extend([
            ("ping_pong_question", 0.08, 0.25, 0.28),
            ("snack_bag_crinkle_open", min(2.2, total_dur_sec * 0.15), 0.85, 0.26),
            ("sfx_kien_cheese_pull_mucus_necha_mlem", min(4.2, total_dur_sec * 0.28), 0.30, 0.28),
            ("tin_lid_metallic_clink" if "kẹo" in desc_low else "sfx_kien_sizzling_pan_fry_crackle", min(6.2, total_dur_sec * 0.40), 0.36, 0.28),
            ("crispy_bite_crunch", min(9.5, total_dur_sec * 0.55), 1.10, 0.32),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    elif semantic_domain == "TRIPOD_CAMERA_SELFIE":
        contextual_sfx_schedule.extend([
            ("ping_pong_question", 0.08, 0.25, 0.26),
            ("mech_click_v1", min(2.5, total_dur_sec * 0.18), 0.12, 0.28),
            ("magnifier_loupe_zoom", min(6.0, total_dur_sec * 0.42), 0.28, 0.26),
            ("camera_shutter_clean", min(10.0, total_dur_sec * 0.65), 0.10, 0.30),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    elif semantic_domain == "DRINKWARE_ICE_TUMBLER":
        contextual_sfx_schedule.extend([
            ("water_pour_splash_test", 0.12, 0.38, 0.28),
            ("liquid_pour_ice_clink", min(4.2, total_dur_sec * 0.30), 1.20, 0.30),
            ("sfx_kien_pac_low_telop_subtitle_pop", min(6.8, total_dur_sec * 0.44), 0.11, 0.26),
            ("mech_click_v1", min(8.5, total_dur_sec * 0.55), 0.12, 0.28),
            ("cart_gold_chime", max(1.5, total_dur_sec - 2.2), 0.32, 0.28)
        ])
    elif semantic_domain in ("SOAP_SKINCARE_CLEANSE", "ORAL_CARE_HYGIENE"):
        contextual_sfx_schedule.extend([
            ("sfx_kien_remove_bottle_cap_unscrew", 0.12, 0.19, 0.28),
            ("card_deck_fan_flip_asmr" if "mặt nạ" in desc_low else "sfx_kien_cheese_pull_mucus_necha_mlem", min(2.4, total_dur_sec * 0.18), 0.30, 0.27),
            ("sfx_kien_poyo_kawaii_skin_touch_bounce", min(4.8, total_dur_sec * 0.34), 0.22, 0.27),
            ("water_pour_splash_test", min(8.5, total_dur_sec * 0.56), 0.38, 0.28),
            ("sfx_kien_kirarin_glitter_skincare_done", min(11.0, total_dur_sec * 0.72), 0.36, 0.28),
            ("cart_gold_chime", max(1.5, total_dur_sec - 2.2), 0.32, 0.28)
        ])
    elif semantic_domain == "TECH_POWER_AIRFLOW":
        contextual_sfx_schedule.extend([
            ("jingle_horn_hook", 0.05, 0.85, 0.24),
            ("mech_click_v1", min(3.5, total_dur_sec * 0.25), 0.12, 0.28),
            ("sfx_kien_pac_low_telop_subtitle_pop", min(5.8, total_dur_sec * 0.40), 0.11, 0.27),
            ("water_splash_submerge" if "nước" in desc_low else "clean_velvet_whoosh", min(8.5, total_dur_sec * 0.55), 0.80, 0.26),
            ("bell_ding_cta", max(1.5, total_dur_sec - 2.2), 0.65, 0.28)
        ])
    else:
        has_vacuum_or_mattress = any(k in desc_low for k in ("nệm", "đệm", "hút chân không", "gối", "chăn", "ga gối"))
        contextual_sfx_schedule.extend([
            ("crystal_aha_shimmer", 0.08, 0.28, 0.26),
            ("sfx_minhtien_vacuum_mattress_air_inflate_hiss" if has_vacuum_or_mattress else "box_cutter_tape_slice", min(2.2, total_dur_sec * 0.16), 0.40, 0.28),
            ("snack_bag_crinkle_open", min(4.5, total_dur_sec * 0.32), 0.75, 0.24),
            ("sfx_kien_pac_low_telop_subtitle_pop", min(8.0, total_dur_sec * 0.55), 0.11, 0.26),
            ("cart_gold_chime", max(1.5, total_dur_sec - 2.2), 0.32, 0.28)
        ])

    # Luôn gắn tiếng Whoosh nối vòng lặp Seamless Loop ở 0.32s cuối cùng (@3thag8_)
    if total_dur_sec >= 4.0:
        contextual_sfx_schedule.append(("radial_zoom_loop_whoosh", max(0.5, total_dur_sec - 0.32), 0.28, 0.26))

    injected_sfx_keys: List[str] = []
    for s_key, st_t, dur_t, vol_v in contextual_sfx_schedule:
        fp = sfx_vault.get(s_key)
        if fp and os.path.exists(fp) and st_t + dur_t <= total_dur_sec + 0.2:
            # Tránh chèn trùng lặp cùng 1 file tại cùng thời điểm
            if not any(abs(float(a.get("start_sec", -9.0)) - st_t) < 0.12 and a.get("source_file") == fp for a in aud_list):
                aud_list.append({
                    "source_file": fp,
                    "start_sec": round(st_t, 2),
                    "end_sec": round(st_t + dur_t, 2),
                    "role": "SFX",
                    "volume": vol_v,
                    "sfx_key": s_key
                })
                injected_sfx_keys.append(s_key)

    return {
        "selected_bgm_key": target_bgm_key,
        "selected_bgm_file": bgm_file,
        "injected_sfx_keys": injected_sfx_keys
    }


def orchestrate_smart_multi_koc_fusion_plan(
    edit_plan: dict,
    product_desc: str,
    product_archetype: str = "P2",
    measured_yavg: float = 132.0,
    creator_handle: str = "",
    outdoor_skin_proof_clip: Optional[str] = None
) -> dict:
    """
    [BỘ NÃO TỔNG ĐẠO DIỄN ĐA NGUỒN — SMART CONTEXTUAL 8-KOC FUSION ROUTER]:
    Giải quyết triệt để bài toán: "Biết thông minh khi nào dùng cái gì, video nào dùng icon gì,
    nhạc nền gì, hiệu ứng âm thanh SFX/Foley gì, cảnh quay gì từ 8 KOC (@meshinthuine,
    @honghanhxinhgai_01, @kieneditcuong, @3thag8_, @byraanni, @grayunbox, @minhtienoiii06, @yuhtt09)
    chứ tuyệt đối không áp đặt cứng nhắc!"

    Tự động phân tích ngữ nghĩa sản phẩm + độ sáng quang học + thời lượng từng cảnh để ra 9 Quyết Định Thông Minh:
      1. Chọn Công thức Màu & Ánh sáng (`color_grade_preset`) khớp bối cảnh thật.
      2. Chọn Kỹ xảo Mở đầu 3s (`hook_style`) khớp cấu trúc sản phẩm.
      3. Chọn Vùng đặt Phụ đề & Bảng màu chữ (`subtitle_zone_preference` & `typography_palette`).
      4. Chọn Họ Icon theo đúng ngành hàng (`🌷 / 💍 / 🧸 / 🍃 / 🫧 / 🪥 / ⚡ / 📸 / 🧊 / 🎀 / 🎁 / 🗣️`) + Emoji-Rebus (`🌱, 🐣, 🧋, 💰, 🎁, 💦, ↙️, 🚮, 📉, 🦟🥀, 🍠, 🐟, 🍅, 📸, 🌰, 🛒`) + Chấm tách OCR & Vị giác (`dưỡng trắ.ng`, `mờ thâ.m`, `m.ụn`, `p.é.o ngậyyy`, `t:an ch:ảy`).
      5. Quyết định bật/tắt Kính Lúp Tròn Nét Đứt 162% (`@byraanni`) & Thước Đo Nét Đứt `1m7` (`@minhtienoiii06`) CHỈ KHI sản phẩm có chi tiết nhỏ hoặc chiều cao cần chứng minh.
      6. Quyết định bật/tắt Tiêu Đề Vòm Kaomoji `⌒ *ੈ✩‧₊˚🌷🎀*ੈ✩‧₊˚`, Huy Hiệu Đánh Giá TikTok Shop (`⭐ 4.9/5 | Đã bán`), So Sánh Lẻ ❌ / Combo ✅ (`🐣`), Công Thức `3in1`, & Nhãn Test Nước Khăn Giấy Khô (`@yuhtt09`).
      7. Quyết định bật/tắt Manga Freeze-Frame Quà Tặng (`@grayunbox`), Hạt Hương/Bọt Bay (`🍃/🫧`), hoặc Hook Tranh Luận Vùng Miền (`Bịch ❌ | Bao ✅` - `@minhtienoiii06`).
      8. Điều phối Nhạc nền (BGM) & 42 Hiệu ứng Âm thanh Foley/SFX cục bộ (`select_smart_contextual_audio_and_sfx_plan`).
      9. Phân bổ 6 kiểu Keyframe Zoom (`@kieneditcuong`), Lá chắn CHR (`@3thag8_`) & Vòng lặp vô tận Radial Blur.
    """
    desc_low = (product_desc or "").lower()
    v_list = edit_plan.setdefault("video_timeline", [])
    t_list = edit_plan.setdefault("text_overlays", [])
    v1_clips = [c for c in v_list if not c.get("is_pip")]
    total_dur = max([float(c.get("timeline_end_sec", 0.0)) for c in v1_clips], default=24.0)

    all_script_low = f"{desc_low} " + " ".join(t.get("text", "").lower() for t in t_list)
    icon_ctx = select_contextual_icons_and_rebus_for_product(all_script_low, product_desc)
    domain = icon_ctx["semantic_domain"]
    decisions_log: List[str] = []

    # --- QUYẾT ĐỊNH 1: CHỌN CÔNG THỨC MÀU & ÁNH SÁNG THÔNG MINH ---
    has_led_or_glow = any(k in all_script_low for k in ("đèn led", "phát sáng", "đèn ngủ", "thiệp nhạc", "thiệp 3d", "ban đêm", "dạ quang"))
    if has_led_or_glow or measured_yavg < 96.0:
        color_preset = "GRAYUNBOX_LOWKEY_LED_GLOW"
        palette_key = "GRAYUNBOX_CLEAN_MINIMAL"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @grayunbox Low-Key LED]: Phát hiện sản phẩm phát sáng/LED hoặc nền tối (YAVG={measured_yavg:.1f}) -> Hạ nền Low-Key để ánh sáng sản phẩm rực rỡ gấp 3 lần."
        )
    elif domain in ("STATIONERY_STUDY_DESK", "JEWELRY_SILVER_ACCESSORY") or any(k in desc_low for k in ("tất", "vớ", "chống nắng", "cushion", "xịt thơm", "sổ", "bút", "bạc")):
        color_preset = "YUHTT09_HIGHKEY_AIRY_DOUYIN_WHITE"
        palette_key = "YUHTT09_COQUETTE_CLEAN_WHITE_PILL"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @yuhtt09 High-Key Airy Douyin White]: Nhóm '{domain}' kích hoạt nền bàn trắng Pegboard Coquette (YAVG~166.1) + Phụ đề trắng viền đen sắc nét tại y=-0.35 (8.1M views)."
        )
    elif domain in ("FOOD_SNACK_GOURMET", "TRIPOD_CAMERA_SELFIE") or product_archetype == "P5":
        color_preset = "MINHTIENOIII_COZY_TOAST_LAMP_SENSORY"
        palette_key = "MINHTIENOIII_GENZ_SENSORY_POP"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @minhtienoiii06 Cozy Toast Lamp Sensory]: Nhóm '{domain}' kích hoạt màu tươi vị giác (SAT+10, YAVG~144.5) & chữ Vàng Kem / Xanh Lá Dứa Neon (19.3M views)."
        )
    elif measured_yavg > 158.0:
        color_preset = "HONGHANH_WARM_DESK_LAMP"
        palette_key = "LUXURY_EDITORIAL"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @honghanhxinhgai_01 Warm Lamp]: Phát hiện đèn bàn rọi đỉnh sáng mạnh (YAVG={measured_yavg:.1f}) -> Bật HSL làm hồng mịn da tay & chống cháy sáng."
        )
    elif domain in ("SCENT_TEA_HERBAL", "PLUSH_TOY_STORAGE_BABY", "ORAL_CARE_HYGIENE", "GIFT_CARD_FESTIVE"):
        color_preset = "GRAYUNBOX_VENETIAN_BLINDS_CHIAROSCURO"
        palette_key = "GRAYUNBOX_CLEAN_MINIMAL"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @grayunbox Venetian Blinds Chiaroscuro]: Nhóm '{domain}' hợp nhất với nắng xiên qua rèm sáo ngang & chữ tối giản góc 1/3 trên."
        )
    elif domain in ("FASHION_BAG_SHOE", "DRINKWARE_ICE_TUMBLER") or product_archetype == "P3":
        color_preset = "BYRAANNI_KINFOLK_ESPRESSO"
        palette_key = "KINFOLK_ESPRESSO_CREAM"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @byraanni Kinfolk Espresso]: Nhóm '{domain}' cần thẩm mỹ tạp chí Pinterest Kem Ngà + Nâu Espresso sang trọng."
        )
    elif domain in ("SOAP_SKINCARE_CLEANSE", "TECH_POWER_AIRFLOW") or product_archetype in ("P1", "P6"):
        color_preset = "3THAG8_PEGBOARD_CLEAN_PINK"
        palette_key = "PEGBOARD_ROSE_GOLD" if product_archetype == "P1" else "TECH_SLEEK_HUD"
        decisions_log.append(
            f"[Màu & Ánh sáng -> @3thag8_ Clean Studio]: Nhóm '{domain}' cần độ trong trẻo sắc nét để nổi bật chất kem/bọt hoặc chi tiết công nghệ."
        )
    else:
        color_preset = "MESHIN_NATURAL_DAYLIGHT"
        palette_key = "COZY_PASTEL_MAMI"
        decisions_log.append(
            "[Màu & Ánh sáng -> @meshinthuine Daylight]: Sử dụng ánh sáng tự nhiên ấm cúng, chân thực gần gũi gia đình."
        )

    edit_plan["typography_palette"] = palette_key

    # --- QUYẾT ĐỊNH 2: CHỌN MÓC CÂU THỊ GIÁC 3 GIÂY ĐẦU (HOOK STYLE) ---
    is_assembly_item = any(k in all_script_low for k in ("lắp ráp", "kệ", "tủ", "hộp đựng", "nhiều ngăn", "khung sắt"))
    if is_assembly_item:
        hook_style = "BYRAANNI_3SHOT_COLLAGE"
        decisions_log.append(
            "[Hook 3s -> @grayunbox Finished-First Assembly]: Sản phẩm cần lắp ráp -> Mở đầu khoe ngay thành phẩm hoàn chỉnh 100% trước khi chiếu cảnh lắp!"
        )
    elif domain in ("FOOD_SNACK_GOURMET", "TRIPOD_CAMERA_SELFIE"):
        hook_style = "BYRAANNI_3SHOT_COLLAGE"
        decisions_log.append(
            "[Hook 3s -> @minhtienoiii06 Hyper-Tactile 1.1s Hook]: Mở đầu cắt nhanh 1.1s vào thao tác tay đắt giá nhất (Cầm đôi / Xếp tháp / Live Camera Screen)."
        )
    elif domain in ("TECH_POWER_AIRFLOW", "ORAL_CARE_HYGIENE"):
        hook_style = "KIEN_GLOW_STROKE_FREEZE"
        decisions_log.append(
            "[Hook 3s -> @kieneditcuong Glow Stroke + Blur]: Sản phẩm công nghệ/chăm sóc cá nhân -> Bật viền phát quang EDGE_GLOW + làm mờ nền BLURRY_FOCUS 1.4s đầu."
        )
    elif domain in ("FASHION_BAG_SHOE", "DRINKWARE_ICE_TUMBLER") and len(v1_clips) >= 3:
        hook_style = "BYRAANNI_3SHOT_COLLAGE"
        decisions_log.append(
            "[Hook 3s -> @byraanni 3-Shot Collage]: Sản phẩm lifestyle/thời trang -> Ghép 3 góc máy liên hoàn (1.1s x 3) kèm tiếng màn trập Camera Focus."
        )
    else:
        hook_style = "KIEN_GHOST_OPACITY_51"
        decisions_log.append(
            "[Hook 3s -> @kieneditcuong Ghost Opacity 51%]: Tạo hiệu ứng bóng mờ 51% trượt khớp vào sản phẩm chính gây tò mò ngay giây đầu."
        )

    inject_3s_visual_hook_and_radial_loop_outro(edit_plan, hook_style=hook_style, enable_radial_blur_loop_outro=True)
    apply_koc_color_grade_and_6_zoom_keyframes(edit_plan, color_preset_key=color_preset)

    # --- QUYẾT ĐỊNH 3 & 4: CHỌN HỌ ICON NGỮ CẢNH, EMOJI-REBUS (@grayunbox x @minhtienoiii06) & TÁCH TỪ OCR (@3thag8_ x @minhtienoiii06) ---
    decisions_log.append(
        f"[Icon Ngữ Cảnh -> {icon_ctx['semantic_domain']}]: Chọn bộ Icon '{' '.join(icon_ctx['accent_icons'])}' khớp 100% với sản phẩm (Tuyệt đối không dùng icon lệch ngành)."
    )
    rebus_notes_all: List[str] = []
    for idx, txt in enumerate(t_list):
        role = txt.get("role", "SUBTITLE")
        raw_t = txt.get("text", "")
        ctx_res = select_contextual_icons_and_rebus_for_product(
            raw_t,
            product_desc,
            enable_rebus=(role not in ("CHR_SHIELD", "WATERMARK")),
            enable_ocr_dot_split=(role not in ("CHR_SHIELD", "WATERMARK"))
        )
        txt["text"] = ctx_res["transformed_text"]
        rebus_notes_all.extend(ctx_res["rebus_applied"])

        # Gắn Icon chủ đạo vào tiêu đề mở đầu hoặc Callout nếu chưa có icon
        if role == "HOOK_BANNER" and icon_ctx["primary_icon"] not in txt["text"]:
            txt["text"] = f"{icon_ctx['primary_icon']} {txt['text']}"
        elif role == "SUBTITLE" and "pos_y" not in txt:
            if color_preset.startswith("YUHTT09"):
                txt["pos_y"] = -0.35  # Chuẩn @yuhtt09: 1 dòng phụ đề trắng viền đen đặt ở y=-0.35
            elif color_preset.startswith("GRAYUNBOX") or color_preset.startswith("MINHTIENOIII"):
                txt["pos_y"] = 0.58  # Chuẩn @grayunbox & @minhtienoiii06: đặt phụ đề ở 1/3 trên để nhường toàn bộ mặt bàn bên dưới cho 2 tay thao tác!

    if rebus_notes_all:
        decisions_log.append(f"[Emoji-Rebus & Khiên Giá Nông Sản (@grayunbox x @minhtienoiii06 x @yuhtt09)]: Đã mã hóa từ nhạy cảm/giá tiền: {', '.join( sorted(set(rebus_notes_all)) )}.")

    # --- QUYẾT ĐỊNH 5: CHỈ BẬT KÍNH LÚP NÉT ĐỨT 162% (@byraanni) KHI SẢN PHẨM CÓ CHI TIẾT NHỎ ---
    micro_detail_triggers = (
        "nút bấm", "cấp độ", "mức gió", "cổng sạc", "type-c", "lông bàn chải", "sợi lông",
        "đầu cọ", "răng lược", "mối hàn", "đường chỉ", "khóa kéo", "ron cao su", "bánh xe", "màn hình led",
        "3 màu", "remote", "điều khiển", "nhân kem", "lớp bánh"
    )
    matched_micro = [kw for kw in micro_detail_triggers if kw in all_script_low]
    if matched_micro and v1_clips:
        target_clip = v1_clips[min(2, len(v1_clips) - 1)]
        t_start = float(target_clip.get("timeline_start_sec", 6.0))
        t_dur = min(2.4, max(1.5, float(target_clip.get("timeline_end_sec", t_start + 2.4)) - t_start))
        label_str = f"Soi kỹ: {matched_micro[0]} {icon_ctx['primary_icon']}"
        inject_dashed_circle_magnifier_pip(
            edit_plan,
            source_file=target_clip.get("source_file") or target_clip.get("file_path", ""),
            source_in_sec=float(target_clip.get("source_in_sec", 0.5)),
            timeline_start_sec=t_start,
            duration_sec=t_dur,
            detail_label=label_str,
            palette_key=palette_key
        )
        decisions_log.append(
            f"[Kính Lúp 162% @byraanni -> BẬT]: Phát hiện chi tiết nhỏ ('{matched_micro[0]}') tại {t_start:.1f}s -> Tự động bật Mặt nạ Tròn Nét Đứt phóng đại 162%."
        )
    else:
        decisions_log.append(
            "[Kính Lúp 162% @byraanni -> TẮT]: Sản phẩm không có chi tiết cơ khí/sợi nhỏ cần soi -> Không chèn Kính lúp để khung hình thoáng sạch."
        )

    # --- QUYẾT ĐỊNH 6A: KỸ XẢO THƯỚC ĐO NÉT ĐỨT 1M7 & HOOK TRANH LUẬN VÙNG MIỀN (@minhtienoiii06) ---
    height_match = re.search(r"\b(1m\d+|\d+\s*cm)\b", all_script_low)
    needs_height_ruler = bool(height_match) or domain == "TRIPOD_CAMERA_SELFIE" or is_assembly_item
    needs_debate_hook = (domain == "FOOD_SNACK_GOURMET")
    if needs_height_ruler or needs_debate_hook:
        h_label = height_match.group(1) if height_match else ("1m7" if domain == "TRIPOD_CAMERA_SELFIE" else "Cao rộng rãi")
        debate_txt = (
            "Bịch Bánh Tráng ❌  |  Bao Bánh Tráng ✅ — Chỗ bạn gọi là gì ?"
            if "bánh tráng" in all_script_low
            else "🗣️ ai thử ăn kiểu này chưa ? ngon xỉu ✨"
        )
        inject_minhtienoiii_sensory_and_ruler_vfx(
            edit_plan,
            product_desc=product_desc,
            enable_dashed_height_ruler=needs_height_ruler,
            ruler_height_label=h_label,
            ruler_at_sec=min(8.0, max(2.8, total_dur * 0.45)),
            enable_dialect_debate_hook=needs_debate_hook,
            debate_pair_text=debate_txt,
            palette_key=palette_key
        )
        if needs_height_ruler:
            decisions_log.append(
                f"[Thước Đo Nét Đứt @minhtienoiii06 -> BẬT]: Phát hiện thông số kích thước ('{h_label}') -> Vẽ đường kẻ nét đứt `⇠ - - {h_label} - - ⇢` trực quan trên màn hình (15.5M views)."
            )
        if needs_debate_hook:
            decisions_log.append(
                f"[Hook Tranh Luận / Vị Giác @minhtienoiii06 -> BẬT]: Kích hoạt thẻ Hook kích nổ bình luận ('{debate_txt}') kèm tiếng Ping-Pong & Double Pop (19.3M views)."
            )

    # --- QUYẾT ĐỊNH 6B: CHỈ BẬT MANGA FREEZE-FRAME QUÀ TẶNG & HẠT HƯƠNG/BỌT BAY (@grayunbox) KHI ĐÚNG NGỮ CẢNH ---
    gift_triggers = ("tặng kèm", "mua 1 tặng", "tặng thêm", "quà tặng", "tặng luôn", "kèm theo", "combo")
    has_bonus_gift = any(g in all_script_low for g in gift_triggers)
    has_scent_or_bubbles = domain in ("SCENT_TEA_HERBAL", "SOAP_SKINCARE_CLEANSE") or any(
        k in all_script_low for k in ("thơm", "hương", "khói", "tạo bọt", "nhiều bọt", "xịt thơm")
    )

    if has_bonus_gift or has_scent_or_bubbles or outdoor_skin_proof_clip:
        inject_grayunbox_contextual_vfx_and_pips(
            edit_plan,
            product_desc=product_desc,
            enable_bonus_gift_freeze_frame=has_bonus_gift,
            bonus_gift_label=f"🎁 Có quà tặng / Combo hời nha! {icon_ctx['primary_icon']}",
            freeze_at_sec=min(3.5, max(1.8, total_dur * 0.22)),
            enable_scent_or_bubble_particles=has_scent_or_bubbles,
            outdoor_skin_proof_clip=outdoor_skin_proof_clip,
            palette_key=palette_key
        )
        if has_bonus_gift:
            decisions_log.append(
                "[Manga Freeze-Frame @grayunbox -> BẬT]: Phát hiện có Quà Tặng / Combo -> Chèn hiệu ứng chụp ảnh đứng hình 0.45s khoe quà tặng chống trôi mắt."
            )
        if has_scent_or_bubbles:
            decisions_log.append(
                f"[Hạt Bay Ngữ Cảnh @grayunbox -> BẬT]: Sản phẩm có Hương thơm/Bọt -> Thả hạt '{' '.join(icon_ctx['floating_particles'])}' lơ lửng bên rìa khung hình."
            )
        if outdoor_skin_proof_clip:
            decisions_log.append(
                "[PIP Cam Thường Ngoài Nắng @grayunbox -> BẬT]: Đã gắn cửa sổ PIP chứng minh chất da thật dưới nắng tự nhiên."
            )

    # --- QUYẾT ĐỊNH 6C: BỘ KỸ XẢO NGỮ CẢNH @yuhtt09 (TIÊU ĐỀ VÒM KAOMOJI, HUY HIỆU SHOP RATING, 3IN1/COMBO & TEST NƯỚC KHĂN GIẤY) ---
    needs_yuhtt09_arch = domain in ("STATIONERY_STUDY_DESK", "JEWELRY_SILVER_ACCESSORY") or color_preset.startswith("YUHTT09")
    needs_shop_rating_pill = domain == "FASHION_BAG_SHOE" or any(k in all_script_low for k in ("tất", "vớ", "áo", "túi", "đã bán"))
    needs_combo_or_3in1 = any(k in all_script_low for k in ("chống nắng", "cushion", "kem nền", "3in1", "combo"))
    needs_water_blot_callout = any(k in all_script_low for k in ("chống nắng", "cushion", "không trôi", "kiềm dầu", "kháng nước", "test nước", "💦"))
    needs_numbered_badges = domain in ("JEWELRY_SILVER_ACCESSORY", "TECH_POWER_AIRFLOW")

    if any((needs_yuhtt09_arch, needs_shop_rating_pill, needs_combo_or_3in1, needs_water_blot_callout, needs_numbered_badges)):
        combo_txt = (
            "❌ Lẻ gần 300 🐣  |  ✅ Combo hời hơn 300 🐣"
            if "combo" in all_script_low
            else "3in1: Chống nắng + Primer + Kem nền ✨"
        )
        inject_yuhtt09_coquette_unbox_and_proof_vfx(
            edit_plan,
            product_desc=product_desc,
            enable_arch_curved_title_kaomoji=needs_yuhtt09_arch,
            arch_title_text=f"⌒ {icon_ctx['primary_icon']} Unbox & Test Thật {icon_ctx['primary_icon']} ⌒",
            enable_shop_rating_pill=needs_shop_rating_pill,
            rating_pill_text="⭐ 4.9/5 (2.1k)  |  Đã bán 23.6K",
            enable_combo_or_3in1_badge=needs_combo_or_3in1,
            combo_badge_text=combo_txt,
            enable_water_tissue_blot_callout=needs_water_blot_callout,
            water_blot_at_sec=min(11.5, max(4.0, total_dur * 0.52)),
            enable_numbered_feature_badges=needs_numbered_badges,
            palette_key=palette_key
        )
        decisions_log.append(
            f"[Kỹ Xảo Đa Ngành @yuhtt09 -> BẬT]: ArchKaomoji={needs_yuhtt09_arch}, ShopRatingPill={needs_shop_rating_pill}, 3in1/Combo={needs_combo_or_3in1}, WaterTissueBlot={needs_water_blot_callout}."
        )

    # --- QUYẾT ĐỊNH 6D (MỚI - 2.304 VIDEO DEEP SCAN): PANTONE SWATCH CARD (@meshinthuine), FLOATING POINTER SPECS (@byraanni), CHIBI BADGE (@honghanhxinhgai_01) & CRYSTAL CLEAR 44% SKIN FILTER (@kieneditcuong) ---
    needs_pantone_swatch = any(k in all_script_low for k in ("chăn", "ga gối", "drap", "nệm", "đệm", "áo len", "set đồ", "bảng màu", "nhiều màu"))
    needs_floating_pointer_specs = domain in ("TECH_POWER_AIRFLOW", "DRINKWARE_ICE_TUMBLER") or any(
        k in all_script_low for k in ("micro", "tai nghe", "quạt", "bình giữ nhiệt", "chống ồn", "450ml", "710ml")
    )
    needs_chibi_reaction_badge = domain == "STATIONERY_STUDY_DESK" or any(
        k in all_script_low for k in ("hộp bút", "túi bút", "kẹp tóc", "sashimi", "máy tính casio")
    )
    needs_pov_crystal_skin_filter = domain in ("SOAP_SKINCARE_CLEANSE", "STATIONERY_STUDY_DESK", "JEWELRY_SILVER_ACCESSORY")

    if needs_pantone_swatch:
        t_list.append({
            "text": "🎨 PANTONE: COCOA • TRUFFLE • OAT",
            "start_sec": 2.45,
            "end_sec": min(5.2, total_dur * 0.40),
            "pos_x": 0.18,
            "pos_y": 0.64,
            "font_size": 6.2,
            "bg_color": "#2B211B",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "POP_UP",
            "anim_out": "FADE_OUT"
        })
        decisions_log.append(
            "[Pantone Color Swatch Card @meshinthuine #05 -> BẬT]: Đã gắn thẻ bảng màu Pantone góc phải trên cho sản phẩm Chăn ga / Thời trang nhiều màu."
        )

    if needs_floating_pointer_specs:
        spec_str = "✦ ANC 42dB • Âm trong trẻo" if "mic" in all_script_low or "tai nghe" in all_script_low else "✦ Gió 17000RPM • Giữ nhiệt kín khít 💦"
        t_list.append({
            "text": spec_str,
            "start_sec": min(3.2, total_dur * 0.22),
            "end_sec": min(5.8, total_dur * 0.42),
            "pos_x": -0.24,
            "pos_y": 0.18,
            "font_size": 6.4,
            "bg_color": "#1E2229",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "TYPEWRITER",
            "anim_out": "FADE_OUT"
        })
        decisions_log.append(
            f"[Floating Part-Pointer Specs @byraanni #05 -> BẬT]: Đã gắn thông số nổi '{spec_str}' bám sát bộ phận sản phẩm."
        )

    if needs_chibi_reaction_badge:
        t_list.append({
            "text": "(๑>◡<๑) Xinh & Tiện xỉu ✨",
            "start_sec": min(5.2, total_dur * 0.35),
            "end_sec": min(7.8, total_dur * 0.55),
            "pos_x": 0.24,
            "pos_y": 0.50,
            "font_size": 6.4,
            "bg_color": "#38222B",
            "palette_key": palette_key,
            "role": "CALLOUT",
            "anim_in": "BOUNCE_IN",
            "anim_out": "FADE_OUT"
        })
        decisions_log.append(
            "[Micro Chibi Reaction Sticker @honghanhxinhgai_01 #05 -> BẬT]: Đã gắn nhãn biểu cảm Chibi nổi phía trên vùng phụ đề."
        )

    if needs_pov_crystal_skin_filter:
        edit_plan["pov_hand_skin_filter"] = {
            "capcut_filter_name": "Trong như pha lê (Crystal Clear)",
            "intensity_pct": 44,
            "source_koc": "@kieneditcuong #12 (7668917355191323912)"
        }
        decisions_log.append(
            "[POV Hand Skin Filter @kieneditcuong #12 -> BẬT]: Áp công thức Bộ lọc 'Trong như pha lê (Crystal Clear) 44%' giúp da tay POV trắng hồng tự nhiên."
        )

    # --- QUYẾT ĐỊNH 7: ĐIỀU PHỐI NHẠC NỀN (BGM) & 42 FOLEY/SFX CỤC BỘ CHUẨN 8 KOC ---
    audio_routing_res = select_smart_contextual_audio_and_sfx_plan(
        edit_plan,
        product_desc=product_desc,
        semantic_domain=domain,
        color_preset=color_preset,
        total_dur_sec=total_dur
    )
    decisions_log.append(
        f"[Âm Thanh & Nhạc Nền 8 KOC -> {audio_routing_res['selected_bgm_key']}]: Đã nạp BGM cục bộ + {len(audio_routing_res['injected_sfx_keys'])} Foley/SFX ({', '.join(audio_routing_res['injected_sfx_keys'])})."
    )

    # --- QUYẾT ĐỊNH 8: LÁ CHẮN BẢO VỆ CHR & WATERMARK (@3thag8_ x @byraanni) ---
    has_price_mention = any(p in all_script_low for p in ("cành", "củ", "hạt dẻ", "k ", "000đ", "flash sale", "trợ giá", "voucher", "🐟", "🍠", "🌰", "🍅"))
    inject_chr_shield_and_brand_watermark_tracks(
        edit_plan,
        total_dur_sec=total_dur,
        creator_handle=creator_handle,
        product_archetype=product_archetype,
        has_flash_sale_price=has_price_mention,
        enable_dot_split_ocr=True
    )
    decisions_log.append(
        f"[Lá Chắn CHR @3thag8_ + Loop]: Đã rà soát bảo vệ điểm CHR (Ngành {product_archetype}, Báo giá={has_price_mention}) & khóa vòng lặp Radial Blur cuối video."
    )

    edit_plan["smart_routing_decisions_log"] = decisions_log
    edit_plan["semantic_icon_context"] = icon_ctx
    edit_plan["audio_and_sfx_routing"] = audio_routing_res
    return edit_plan

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
            if isinstance(seg.get("mask_config"), dict):
                m_mat = create_mask_material(**seg["mask_config"])
            else:
                m_mat = create_mask_material(mask_key=seg["mask"])
            masks_mat.append(m_mat)
            extra_refs.append(m_mat["id"])

        if seg.get("transition") and not seg.get("is_pip"):
            tr_mat = create_transition_material(seg["transition"])
            transitions_mat.append(tr_mat)
            extra_refs.append(tr_mat["id"])

        scale_start = float(seg.get("scale", 1.0))
        scale_end = float(seg.get("scale_end", scale_start * 1.05))
        if seg.get("zoom_archetype"):
            kfs = create_6_archetype_zoom_keyframes(seg["zoom_archetype"], t_dur_us, scale_start)
        elif scale_end != scale_start:
            kfs = create_scale_keyframes(scale_start, scale_end, t_dur_us)
        else:
            kfs = []

        v_seg_obj = {
            "id": uid(), "material_id": v_mat_id, "extra_material_refs": extra_refs,
            "source_timerange": {"start": src_start_us, "duration": src_dur_us},
            "target_timerange": {"start": t_start_us, "duration": t_dur_us},
            "speed": speed_val, "volume": float(seg.get("native_volume", 0.0)),
            "clip": {
                "scale": {"x": scale_start, "y": scale_start}, "rotation": 0.0,
                "transform": {"x": float(seg.get("pos_x", 0.0)), "y": float(seg.get("pos_y", 0.0))},
                "flip": {"vertical": False, "horizontal": False}, "alpha": float(seg.get("alpha", 1.0))
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
                "flip": {"vertical": False, "horizontal": False}, "alpha": float(txt.get("alpha", 1.0))
            },
            "render_index": 14000
        }
        if role in ("HOOK_BANNER", "CALLOUT", "CTA", "BLING_ACCENT", "CHR_SHIELD", "WATERMARK"):
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
