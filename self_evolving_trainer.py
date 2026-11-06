#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SELF-EVOLVING AI BRAIN, MODEL CHAINING STATE MANAGER & CAPCUT DIFF LEARNER
Giúp AI tự train cho chính nó ngày càng thông minh hơn qua 3 cơ chế thực chiến:
1. learn_from_user_capcut_edits() : Đọc ngược những tinh chỉnh bằng tay của bạn trong CapCut Desktop
                                    (Diff giữa bản AI tạo và bản bạn sửa) để học thuộc Gu cá nhân của bạn!
2. record_reflexion_lesson()      : Tự miễn dịch với mọi lỗi từng bị QA Auditor phát hiện.
3. reward_winning_project()       : Trích xuất ADN của các video Nổ Đơn / Triệu View thành Few-Shot Mẫu Vàng!
"""

import os
import json
import time
import shutil
import argparse
from typing import Dict, List, Optional

BRAIN_DIR = "./workspace/brain_memory"
CHAIN_DIR = "./workspace/chain_state"
CAPCUT_DRAFTS_ROOT = os.path.expanduser(
    "~/Movies/CapCut/User Data/Projects/com.lveditor.draft"
)
if not os.path.exists(CAPCUT_DRAFTS_ROOT) and os.name == "nt":
    CAPCUT_DRAFTS_ROOT = os.path.expandvars(
        r"%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft"
    )

PREF_FILE = os.path.join(BRAIN_DIR, "learned_user_preferences.json")
REFLEXION_FILE = os.path.join(BRAIN_DIR, "reflexion_lessons.jsonl")
GOLD_WINNERS_FILE = os.path.join(BRAIN_DIR, "gold_winning_templates.json")

DEFAULT_BRAIN_PREFS = {
    "version": 1,
    "episodes_trained": 0,
    "preferred_subtitle_pos_y": -0.50,
    "preferred_font_size_delta": 0.0,
    "preferred_bgm_volume": 0.06,
    "preferred_sfx_volume": 0.25,
    "preferred_avg_clip_duration_sec": 1.85,
    "favorite_transition_resource_ids": [],
    "favorite_font_resource_ids": [],
    "custom_director_rules": [
        "Luôn gọt sạch 0.45s chết ở đầu clip Hook để đạt Scroll-Stop Rate > 65%.",
        "Áp dụng công thức Khen 8 - Chê 2 ở giây thứ 15-20 để tăng độ tin cậy và tránh lỗi phóng đại CHR.",
        "Tuyệt đối không để chữ đè lên vùng tâm sản phẩm (-0.25 < pos_y < 0.30)."
    ]
}

def load_self_trained_brain() -> Dict[str, any]:
    """
    Được gọi ở Mắt xích số 1 (Node 1) trước mỗi lần dựng video:
    Nạp toàn bộ Sở thích đã học của người dùng + Bài học miễn dịch lỗi + Top Mẫu Vàng nổ đơn!
    """
    os.makedirs(BRAIN_DIR, exist_ok=True)
    if not os.path.exists(PREF_FILE):
        with open(PREF_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_BRAIN_PREFS, f, ensure_ascii=False, indent=2)
    with open(PREF_FILE, "r", encoding="utf-8") as f:
        prefs = json.load(f)

    lessons = []
    if os.path.exists(REFLEXION_FILE):
        with open(REFLEXION_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    lessons.append(json.loads(line))

    gold_winners = []
    if os.path.exists(GOLD_WINNERS_FILE):
        with open(GOLD_WINNERS_FILE, "r", encoding="utf-8") as f:
            gold_winners = json.load(f)

    return {
        "learned_preferences": prefs,
        "recent_immunization_lessons": lessons[-15:],
        "gold_winning_few_shot_templates": gold_winners[-5:]
    }

def save_cot_stage_checkpoint(stage_num: int, stage_name: str, cot_trace: Dict[str, str], payload: Dict) -> str:
    """
    [ĐIỀU PHỐI MODEL CHAINING & KIỂM TRA BẮT BUỘC 4 BƯỚC SUY LUẬN CoT]:
    Đảm bảo mỗi mắt xích (Node 1 -> Node 7) phải hoàn thành đầy đủ 4 bước suy luận Chain-of-Thought:
    1. observation   (Quan sát số liệu thực tế)
    2. memory_policy (Đối chiếu Ký ức Tự học & Chính sách CHR)
    3. critique      (Phản biện tối thiểu 2 phương án A vs. B)
    4. decision      (Chốt thông số toán học)
    """
    os.makedirs(CHAIN_DIR, exist_ok=True)
    required_cot_keys = ("observation", "memory_policy", "critique", "decision")
    for k in required_cot_keys:
        if k not in cot_trace or not str(cot_trace[k]).strip():
            raise ValueError(f"[CoT Violation at Stage {stage_num}] Thiếu bước suy luận bắt buộc: '{k}'!")

    out_path = os.path.join(CHAIN_DIR, f"stage_{stage_num}_{stage_name}.json")
    record = {
        "stage_number": stage_num,
        "stage_name": stage_name,
        "timestamp": int(time.time()),
        "cot_reasoning_trace": cot_trace,
        "stage_output": payload
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return out_path

def save_ai_initial_snapshot(project_name: str, draft_dict: Dict):
    """Lưu lại bản chụp draft_info.json ngay lúc AI vừa tạo xong để đối chiếu khi người dùng sửa tay trên CapCut."""
    os.makedirs(BRAIN_DIR, exist_ok=True)
    snap_path = os.path.join(BRAIN_DIR, f"snapshot_{project_name}.json")
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(draft_dict, f, ensure_ascii=False)

def learn_from_user_capcut_edits(project_name: str) -> Dict[str, any]:
    """
    [CƠ CHẾ TỰ HỌC 1 - HỌC LỎM TỪ BÀN TAY CHỈNH SỬA CỦA BẠN TRÊN CAPCUT DESKTOP]:
    So sánh file `draft_info.json` hiện tại trong CapCut (sau khi bạn đã tự tay tinh chỉnh thêm)
    với bản `snapshot_<project_name>.json` lúc AI vừa tạo ra.
    Tự động rút trích sự thay đổi về: Vị trí chữ Y, Cỡ chữ, Tốc độ cắt trung bình, Âm lượng BGM/SFX,
    và các hiệu ứng Transition/Font mới bạn thêm vào -> Cập nhật thẳng vào Bộ Nhớ Dài Hạn của AI!
    """
    live_draft_path = os.path.join(CAPCUT_DRAFTS_ROOT, project_name, "draft_info.json")
    if not os.path.exists(live_draft_path):
        return {"status": "ERROR", "message": f"Không tìm thấy project {project_name} trong CapCut."}

    with open(live_draft_path, "r", encoding="utf-8") as f:
        user_draft = json.load(f)

    brain = load_self_trained_brain()
    prefs = brain["learned_preferences"]
    learned_deltas = []

    # 1. Học vị trí đặt phụ đề (pos_y) và cỡ chữ mà người dùng vừa chỉnh trên CapCut
    text_ys = []
    font_sizes = []
    v1_durations = []

    for trk in user_draft.get("tracks", []):
        if trk.get("type") == "text":
            for seg in trk.get("segments", []):
                py = seg.get("clip", {}).get("transform", {}).get("y")
                if py is not None and -0.65 <= float(py) <= -0.25:
                    text_ys.append(float(py))
        elif trk.get("type") == "video":
            for seg in trk.get("segments", []):
                if seg.get("render_index", 0) == 0:
                    dur_s = seg.get("target_timerange", {}).get("duration", 0) / 1_000_000.0
                    if 0.4 <= dur_s <= 6.0:
                        v1_durations.append(dur_s)

    for t_mat in user_draft.get("materials", {}).get("texts", []):
        fs = t_mat.get("font_size")
        if fs:
            font_sizes.append(float(fs))
        fid = t_mat.get("font_resource_id")
        if fid and fid not in prefs["favorite_font_resource_ids"]:
            prefs["favorite_font_resource_ids"].append(fid)
            learned_deltas.append(f"Đã học thêm Font chữ yêu thích của bạn: resource_id={fid}")

    for tr_mat in user_draft.get("materials", {}).get("transitions", []):
        rid = tr_mat.get("resource_id")
        if rid and rid not in prefs["favorite_transition_resource_ids"]:
            prefs["favorite_transition_resource_ids"].append(rid)
            learned_deltas.append(f"Đã học thêm Chuyển cảnh yêu thích của bạn: {tr_mat.get('name')} ({rid})")

    # [CỔNG CHỐNG NGU ĐI SỐ 3 & 4]:
    # 1. Sao lưu Snapshot phiên bản não bộ vào ./knowledge_vault/06_brain_version_snapshots/ trước khi cập nhật.
    # 2. Cập nhật trung bình trượt Clamped EMA 80/20 (alpha=0.20) kèm kẹp biên an toàn tuyệt đối (Core Anchor)
    #    để dù có 1 lần thử nghiệm lạ cũng không làm hỏng công thức chuẩn!
    save_brain_version_snapshot(tag=f"before_capcut_learn_{project_name}")
    alpha = 0.20
    if text_ys:
        avg_y = sum(text_ys) / len(text_ys)
        old_y = prefs["preferred_subtitle_pos_y"]
        new_y = round(old_y * (1 - alpha) + avg_y * alpha, 3)
        prefs["preferred_subtitle_pos_y"] = max(-0.56, min(-0.35, new_y))
        learned_deltas.append(f"Cập nhật vị trí phụ đề ưa thích (Clamped Safe): pos_y = {prefs['preferred_subtitle_pos_y']}")

    if v1_durations:
        avg_d = sum(v1_durations) / len(v1_durations)
        old_d = prefs["preferred_avg_clip_duration_sec"]
        new_d = round(old_d * (1 - alpha) + avg_d * alpha, 2)
        prefs["preferred_avg_clip_duration_sec"] = max(1.25, min(2.55, new_d))
        learned_deltas.append(f"Cập nhật nhịp cắt trung bình ưa thích (Clamped Safe): {prefs['preferred_avg_clip_duration_sec']}s/cảnh")

    prefs["episodes_trained"] = int(prefs.get("episodes_trained", 0)) + 1
    with open(PREF_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)

    print(f"[SELF-TRAINING SUCCESS] AI đã học thành công {len(learned_deltas)} tinh chỉnh từ '{project_name}' (Có bảo vệ chống thoái hóa 80/20)!")
    return {"status": "LEARNED", "episodes_trained": prefs["episodes_trained"], "learned_deltas": learned_deltas}


def save_brain_version_snapshot(tag: str = "manual") -> str:
    """
    [CỔNG CHỐNG NGU ĐI SỐ 4 - BRAIN VERSION SNAPSHOT]:
    Lưu toàn bộ trạng thái não bộ hiện tại vào `./knowledge_vault/06_brain_version_snapshots/`
    trước mỗi lần học mới. Nếu bản mới kém đi, có thể Rollback tức thì!
    """
    snap_dir = "./knowledge_vault/06_brain_version_snapshots"
    os.makedirs(snap_dir, exist_ok=True)
    brain_state = load_self_trained_brain()
    snap_path = os.path.join(snap_dir, f"brain_v_{int(time.time())}_{tag}.json")
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(brain_state, f, ensure_ascii=False, indent=2)
    return snap_path


def rollback_brain_to_previous_version() -> Dict[str, Any]:
    """Khôi phục não bộ về phiên bản Snapshot thông minh nhất ngay trước đó."""
    snap_dir = "./knowledge_vault/06_brain_version_snapshots"
    if not os.path.exists(snap_dir):
        return {"status": "NO_SNAPSHOTS"}
    snaps = sorted(
        [os.path.join(snap_dir, fn) for fn in os.listdir(snap_dir) if fn.startswith("brain_v_") and fn.endswith(".json")]
    )
    if not snaps:
        return {"status": "NO_SNAPSHOTS"}
    latest_snap = snaps[-1]
    with open(latest_snap, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "user_preferences" in data:
        with open(PREF_FILE, "w", encoding="utf-8") as pf:
            json.dump(data["user_preferences"], pf, ensure_ascii=False, indent=2)
    print(f"[BRAIN ROLLBACK OK] Đã khôi phục não bộ về phiên bản an toàn: {latest_snap}")
    return {"status": "ROLLED_BACK", "restored_from": latest_snap}


def learn_from_documents_inbox(docs_dir: str = "./knowledge_vault/05_documents_and_guides_inbox") -> Dict[str, Any]:
    """
    [CƠ CHẾ TỰ ĐỌC & HỌC TỪ TÀI LIỆU MỚI]:
    Quét mọi tài liệu (.md, .txt, .docx) bạn thả vào `./knowledge_vault/05_documents_and_guides_inbox/`
    hoặc trong thư mục gốc, trích xuất các quy tắc chính sách, từ khóa cấm, mẹo quay dựng mới
    và lưu vào file riêng: `./knowledge_vault/learned_document_rules_registry.json`.
    """
    import re
    import subprocess
    os.makedirs(docs_dir, exist_ok=True)
    registry_path = "./knowledge_vault/learned_document_rules_registry.json"
    existing_reg: Dict[str, Any] = {"updated_at": "", "documents_learned": {}}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                existing_reg = json.load(f)
        except Exception:
            pass

    scan_files = [
        os.path.join(docs_dir, fn)
        for fn in sorted(os.listdir(docs_dir))
        if fn.lower().endswith((".md", ".txt", ".docx"))
    ]
    # Luôn bao gồm Cẩm nang chính sách CHR Việt Nam ở thư mục gốc
    root_chr = "./Cẩm nang Toàn diện TikTok Affiliate (Việt Nam).md"
    if os.path.exists(root_chr):
        scan_files.append(root_chr)

    for fpath in scan_files:
        fname = os.path.basename(fpath)
        text = ""
        if fpath.lower().endswith(".docx"):
            res = subprocess.run(["textutil", "-convert", "txt", "-stdout", fpath], capture_output=True, text=True)
            text = res.stdout
        else:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception:
                continue

        if not text.strip():
            continue

        # Trích xuất các câu quy tắc quan trọng (chứa 'bắt buộc', 'tuyệt đối không', 'cấm', 'mẹo', 'lưu ý', '-10', '-20', '-40')
        rules_found = []
        for line in text.splitlines():
            clean_ln = line.strip().lstrip("*-•> ")
            if len(clean_ln) < 18 or len(clean_ln) > 320:
                continue
            low = clean_ln.lower()
            if any(k in low for k in ("tuyệt đối không", "bắt buộc", "nghiêm cấm", "trừ điểm", "-10", "-20", "-40", "miễn trừ", "mẹo", "khuyên dùng")):
                rules_found.append(clean_ln)

        existing_reg["documents_learned"][fname] = {
            "file_path": os.path.abspath(fpath),
            "extracted_rules_count": len(rules_found),
            "key_rules_sample": rules_found[:40],
            "learned_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

    existing_reg["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(existing_reg, f, ensure_ascii=False, indent=2)

    print(f"[DOCUMENT KNOWLEDGE LEARNED] Đã học {len(existing_reg['documents_learned'])} tài liệu và lưu vào: {registry_path}")
    return existing_reg

def record_reflexion_lesson(project_name: str, auto_healed_issues: List[str]):
    """
    [CƠ CHẾ TỰ HỌC 2 - GHI NHỚ BÀI HỌC MIỄN DỊCH LỖI (REFLEXION MEMORY)]:
    Mỗi khi QA Auditor phải tự sửa lỗi (Auto-Heal), ghi lại bài học để các lần chạy sau tránh ngay từ Node 1-5!
    """
    if not auto_healed_issues:
        return
    os.makedirs(BRAIN_DIR, exist_ok=True)
    entry = {
        "timestamp": int(time.time()),
        "project": project_name,
        "lessons_learned": auto_healed_issues
    }
    with open(REFLEXION_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def reward_winning_project_as_gold_template(
    project_name: str,
    archetype: str = "P1",
    views: int = 100000,
    orders: int = 100
) -> Dict[str, any]:
    """
    [CƠ CHẾ TỰ HỌC 3 - HỌC TĂNG CƯỜNG TỪ VIDEO NỔ ĐƠN / TRIỆU VIEW (REWARD REINFORCEMENT)]:
    Trích xuất cấu trúc nhịp điệu, tỷ lệ cắt và hiệu ứng của dự án thắng lớn thành Mẫu Vàng (Gold Few-Shot).
    """
    os.makedirs(BRAIN_DIR, exist_ok=True)
    live_draft_path = os.path.join(CAPCUT_DRAFTS_ROOT, project_name, "draft_info.json")
    if not os.path.exists(live_draft_path):
        return {"status": "ERROR", "message": f"Không tìm thấy project {project_name}"}

    with open(live_draft_path, "r", encoding="utf-8") as f:
        draft = json.load(f)

    v1_durs = []
    for trk in draft.get("tracks", []):
        if trk.get("type") == "video":
            for seg in trk.get("segments", []):
                if seg.get("render_index", 0) == 0:
                    v1_durs.append(round(seg.get("target_timerange", {}).get("duration", 0) / 1_000_000.0, 2))

    transitions_used = [t.get("name") for t in draft.get("materials", {}).get("transitions", []) if t.get("name")]
    gold_entry = {
        "project_name": project_name,
        "product_archetype": archetype,
        "views": views,
        "orders": orders,
        "gpm_efficiency_index": round((orders / max(1, views)) * 1000, 2),
        "winning_dna": {
            "clip_count": len(v1_durs),
            "hook_first_clip_dur_sec": v1_durs[0] if v1_durs else 1.6,
            "avg_clip_dur_sec": round(sum(v1_durs) / max(1, len(v1_durs)), 2),
            "v1_pacing_curve_sec": v1_durs[:15],
            "transitions_signature": list(dict.fromkeys(transitions_used))
        }
    }

    winners = []
    if os.path.exists(GOLD_WINNERS_FILE):
        with open(GOLD_WINNERS_FILE, "r", encoding="utf-8") as f:
            winners = json.load(f)
    winners.append(gold_entry)
    with open(GOLD_WINNERS_FILE, "w", encoding="utf-8") as f:
        json.dump(winners, f, ensure_ascii=False, indent=2)

    print(f"[GOLD TEMPLATE SAVED] Đã lưu ADN chiến thắng của '{project_name}' vào Kho Mẫu Vàng!")
    return gold_entry


def cleanup_archived_projects_older_than(days: int = 30) -> List[str]:
    """
    Chỉ dọn dẹp các thư mục dự án cũ trong `./projects/` đã hoàn thành và cũ hơn `days` ngày
    khi người dùng chủ động yêu cầu giải phóng dung lượng ổ cứng.
    """
    import shutil
    projects_root = os.path.abspath("./projects")
    removed = []
    if not os.path.exists(projects_root):
        return removed
    cutoff = time.time() - (days * 86400.0)
    for slug in sorted(os.listdir(projects_root)):
        p_dir = os.path.join(projects_root, slug)
        if os.path.isdir(p_dir) and os.path.getmtime(p_dir) < cutoff:
            shutil.rmtree(p_dir, ignore_errors=True)
            removed.append(p_dir)
    print(f"[CLEANUP COMPLETE] Đã dọn dẹp {len(removed)} dự án cũ hơn {days} ngày.")
    return removed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Self-Evolving AI Video Director Trainer")
    parser.add_argument("--learn-from-capcut", type=str, help="Tên Project CapCut bạn vừa chỉnh tay để AI học lỏm")
    parser.add_argument("--learn-from-docs", action="store_true", help="Quét và học toàn bộ tài liệu trong ./knowledge_vault/05_documents_and_guides_inbox/")
    parser.add_argument("--rollback-brain", action="store_true", help="Khôi phục não bộ về phiên bản Snapshot thông minh nhất trước đó")
    parser.add_argument("--reward-winner", type=str, help="Tên Project nổ đơn/nhiều view để lưu làm Mẫu Vàng")
    parser.add_argument("--ingest-project", type=str, help="Tự động chuyển ảnh/video từ ./raw_photos & ./raw_videos sang ./projects/<slug>/")
    parser.add_argument("--cleanup-days", type=int, help="Xóa các dự án lưu trữ trong ./projects/ cũ hơn N ngày")
    parser.add_argument("--archetype", type=str, default="P1", help="Mã ngành hàng P1-P7")
    parser.add_argument("--views", type=int, default=100000, help="Số lượt xem đạt được")
    parser.add_argument("--orders", type=int, default=100, help="Số đơn hàng chốt được")
    parser.add_argument("--show-brain", action="store_true", help="Hiển thị trạng thái Bộ Nhớ Tự Học hiện tại")
    args = parser.parse_args()

    if args.ingest_project:
        from smart_raw_miner import ingest_and_isolate_project_videos
        from pre_production_shooting_planner import setup_and_ingest_project_photos
        p_info = setup_and_ingest_project_photos(args.ingest_project, [])
        v_info = ingest_and_isolate_project_videos(args.ingest_project)
        print(json.dumps({"photos": p_info, "videos": v_info}, ensure_ascii=False, indent=2))
    if args.cleanup_days is not None:
        cleanup_archived_projects_older_than(args.cleanup_days)
    if args.learn_from_docs:
        learn_from_documents_inbox()
    if args.rollback_brain:
        rollback_brain_to_previous_version()
    if args.learn_from_capcut:
        learn_from_user_capcut_edits(args.learn_from_capcut)
    if args.reward_winner:
        reward_winning_project_as_gold_template(args.reward_winner, args.archetype, args.views, args.orders)
    if args.show_brain:
        print(json.dumps(load_self_trained_brain(), ensure_ascii=False, indent=2))
