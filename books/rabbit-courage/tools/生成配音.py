# -*- coding: utf-8 -*-
"""
《小豆的勇氣》一鍵配音生成器
使用微軟 Edge 神經語音（免註冊、免金鑰、免費）

執行後會在同一層產生 audio/ 資料夾，內含 22 個 MP3。
把 audio/ 跟「小豆的勇氣.html」放在一起，繪本就會自動改播這些配音。
"""

import asyncio, sys, os, subprocess, shutil

# ── 自動安裝相依套件 ────────────────────────────────────────────
try:
    import edge_tts
except ImportError:
    print("正在安裝語音套件 edge-tts ...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "edge-tts"])
    import edge_tts

# ── 角色音色設定（想換聲音就改這裡）─────────────────────────────
# 可用的台灣中文音色：
#   zh-TW-HsiaoChenNeural  曉臻（女，溫暖清晰）
#   zh-TW-HsiaoYuNeural    曉雨（女，柔和年輕）
#   zh-TW-YunJheNeural     雲哲（男，沉穩）
ROLES = {
    "旁白": {"voice": "zh-TW-HsiaoChenNeural", "pitch": 0,  "vol": 0},
    "媽媽": {"voice": "zh-TW-HsiaoYuNeural",   "pitch": -4, "vol": -6},
    "小豆": {"voice": "zh-TW-HsiaoYuNeural",   "pitch": 30, "vol": 0},   # 音高拉高 → 童聲
}
# 小豆聽起來太尖？把上面的 30 改小（例如 20）。太成熟？改大（例如 40）。

# ── 22 句配音表 ────────────────────────────────────────────────
# (檔名, 角色, 唸稿, 語速%, 額外音高Hz, 額外音量%)
LINES = [
    ("p1-1", "旁白", "小豆是一隻小兔子。他走到哪裡，都牽著媽媽的手。",           -14,   0,   0),
    ("p1-2", "旁白", "連睡覺的時候，也要抓著媽媽軟軟的耳朵。",                   -18,  +2,  -4),

    ("p2-1", "旁白", "森林裡的小兔子，都會自己去採紅蘿蔔。",                      -8,  +6,   0),
    ("p2-2", "旁白", "只有小豆，躲在媽媽身後，偷偷看。",                         -16,  +2, -18),
    ("p2-3", "旁白", "他好想跟大家一起去，可是他的腳，動不了。",                 -20,  -8, -10),

    ("p3-1", "旁白", "有一天早上，媽媽蹲下來，輕輕地說，",                       -12,   0,   0),
    ("p3-2", "媽媽", "小豆，今天你自己去採一根紅蘿蔔，好嗎？",                   -16,  +4,   0),
    ("p3-3", "旁白", "小豆的心，噗通，噗通，跳得好快。",                          +6, +14,  +4),

    ("p4-1", "旁白", "小豆走出家門。一步，兩步，三步。",                         -22,  +4,  -6),
    ("p4-2", "旁白", "森林好大好大，風吹過樹葉，沙、沙、沙。",                   -18,  -2, -22),
    ("p4-3", "旁白", "他好想回頭，可是，他沒有。",                               -14,  -4,   0),

    ("p5-1", "旁白", "走著走著，小豆迷路了。",                                   -20, -10, -10),
    ("p5-2", "旁白", "天色慢慢暗了，小豆蹲在大石頭旁邊，哭了。",                 -24,  -8, -20),
    ("p5-3", "小豆", "媽媽……我好想你。",                                        -30,  +6, -16),

    ("p6-1", "旁白", "哭著哭著，小豆想起媽媽說過的話。",                         -14,  +2,  -6),
    ("p6-2", "媽媽", "勇敢，不是不害怕。",                                       -28,  -2,  -4),
    ("p6-3", "媽媽", "是害怕的時候，還願意，再往前走一步。",                     -26,  -2,  -4),

    ("p7-1", "旁白", "小豆深深吸了一口氣，站了起來。",                           -16,  -4,   0),
    ("p7-2", "旁白", "他擦掉眼淚，順著月光，一步一步往前走。",                   -10,  +2,  +4),
    ("p7-3", "旁白", "然後他看見了，一整片胖胖的紅蘿蔔！",                        +8, +20, +10),

    ("p8-1", "旁白", "小豆回到家的時候，媽媽正站在門口等他。",                   -16,   0,   0),
    ("p8-2", "旁白", "他把最大的那一根紅蘿蔔，遞給媽媽。",                       -16,   0,   0),
    ("p8-3", "小豆", "媽媽，明天我還要自己去。",                                  -8, +12,  +6),
]

def _book_dir():
    """自動找到繪本 HTML 所在的資料夾，音檔就生在它旁邊。
    不管這支程式放在繪本同一層、或放在 tools/ 子資料夾裡，都能正確運作。"""
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (here, os.path.dirname(here)):
        for name in ("index.html", "小豆的勇氣.html"):
            if os.path.exists(os.path.join(d, name)):
                return d
    return here


OUT = os.path.join(_book_dir(), "audio")
FORCE = "--force" in sys.argv          # 加上 --force 會強制全部重新生成


def fmt(n, unit):
    return f"{'+' if n >= 0 else ''}{n}{unit}"


async def one(name, role, text, rate, dpitch, dvol):
    cfg = ROLES[role]
    path = os.path.join(OUT, name + ".mp3")
    if not FORCE and os.path.exists(path) and os.path.getsize(path) > 1200:
        print(f"  – {name}.mp3  已存在，跳過")
        return
    c = edge_tts.Communicate(
        text,
        cfg["voice"],
        rate=fmt(rate, "%"),
        pitch=fmt(cfg["pitch"] + dpitch, "Hz"),
        volume=fmt(cfg["vol"] + dvol, "%"),
    )
    await c.save(path)
    kb = os.path.getsize(path) / 1024
    print(f"  ✓ {name}.mp3  [{role}] {kb:5.1f} KB   {text[:18]}")


async def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 58)
    print(f"  《小豆的勇氣》配音生成中 —— 共 {len(LINES)} 句")
    print("=" * 58)
    ok, fail = 0, []
    for i, item in enumerate(LINES, 1):
        try:
            await one(*item)
            ok += 1
        except Exception as e:
            fail.append((item[0], str(e)[:90]))
            print(f"  ✗ {item[0]}.mp3 失敗：{str(e)[:90]}")
        await asyncio.sleep(0.35)          # 對服務友善一點，避免被限速

    print("-" * 58)
    print(f"完成 {ok} / {len(LINES)} 句 → {OUT}")
    if fail:
        print("\n以下失敗，請重跑一次腳本（只會補生成缺的）：")
        for n, e in fail:
            print(f"  {n}: {e}")

    # 若電腦上有 ffmpeg，順便把音量統一（沒有就跳過，不影響使用）
    if shutil.which("ffmpeg"):
        print("\n偵測到 ffmpeg，正在統一音量 ...")
        for name, *_ in LINES:
            src = os.path.join(OUT, name + ".mp3")
            if not os.path.exists(src):
                continue
            tmp = src + ".tmp.mp3"
            r = subprocess.run(
                ["ffmpeg", "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                 "-ar", "44100", "-ac", "1", "-b:a", "96k", tmp],
                capture_output=True,
            )
            if r.returncode == 0:
                os.replace(tmp, src)
            elif os.path.exists(tmp):
                os.remove(tmp)
        print("音量統一完成。")
    else:
        print("\n（沒偵測到 ffmpeg，略過音量統一 —— 不影響播放）")

    print("\n最後一步：把 audio 資料夾跟「小豆的勇氣.html」放在同一層，")
    print("重新打開繪本，右上角就會顯示 🎧 配音檔。\n")


if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
