# -*- coding: utf-8 -*-
"""《我自己來》一鍵配音生成器 — 微軟 Edge 神經語音（免註冊、免金鑰、免費）"""
import asyncio, sys, os, subprocess, shutil
try:
    import edge_tts
except ImportError:
    print("正在安裝語音套件 edge-tts ...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "edge-tts"])
    import edge_tts

# 角色音色（想換聲音改這裡）
# zh-TW-HsiaoChenNeural 曉臻(女,溫暖) / zh-TW-HsiaoYuNeural 曉雨(女,柔和) / zh-TW-YunJheNeural 雲哲(男,沉穩)
ROLES = {
    "旁白": {
        "voice": "zh-TW-HsiaoChenNeural",
        "pitch": 0,
        "vol": 0
    },
    "豆豆": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 28,
        "vol": 0
    },
    "媽媽": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": -6,
        "vol": -4
    }
}

LINES = [
    ("p1-1", "旁白", "小刺蝟豆豆，最喜歡說一句話。", -12, 0, 0),
    ("p1-2", "豆豆", "我、自、己、來！", -30, 0, 0),
    ("p2-1", "旁白", "可是豆豆的扣子，總是扣錯一格。", -14, 0, 0),
    ("p3-1", "旁白", "鞋子呢，常常穿反。", -12, 0, 0),
    ("p3-2", "豆豆", "咦？走起來怪怪的。", -10, 0, 0),
    ("p4-1", "旁白", "喝湯的時候，湯會灑出來。", -12, 0, 0),
    ("p4-2", "旁白", "灑得滿桌子都是。", -8, 0, 0),
    ("p5-1", "旁白", "媽媽想幫忙，豆豆把手縮起來。", -14, 0, 0),
    ("p5-2", "豆豆", "不要！我自己來。", -8, 0, 0),
    ("p6-1", "旁白", "有一天，豆豆要去小鴨家玩。", -10, 0, 0),
    ("p6-2", "豆豆", "今天全部都我自己準備！", -6, 0, 0),
    ("p7-1", "旁白", "第一顆扣子，扣了好久。", -22, 0, 0),
    ("p7-2", "旁白", "第二顆，也扣了好久。", -26, 0, 0),
    ("p7-3", "旁白", "第三顆……終於對了！", -12, 0, 0),
    ("p8-1", "旁白", "鞋子換了一次、兩次、三次。", -16, 0, 0),
    ("p8-2", "豆豆", "這次……對了！", -12, 0, 0),
    ("p9-1", "旁白", "走出家門的時候，太陽已經很高很高了。", -12, 0, 0),
    ("p10-1", "旁白", "小鴨看看太陽，又看看豆豆。", -14, 0, 0),
    ("p10-2", "小鴨", "你怎麼這麼慢呀？", -10, 0, 0),
    ("p11-1", "旁白", "豆豆挺起胸膛，很大聲地說：", -14, 0, 0),
    ("p11-2", "豆豆", "因為，這些全部都是我自己做的。", -22, 0, 0),
    ("p12-1", "旁白", "那天晚上，媽媽幫豆豆脫下外套。", -20, 0, 0),
    ("p12-2", "旁白", "然後她發現，", -20, 0, 0),
    ("p12-3", "旁白", "每一顆扣子，都扣對了。", -30, 0, 0),
]   # (檔名, 角色, 唸稿, 語速%, 額外音高Hz, 額外音量%)

def _book_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (here, os.path.dirname(here)):
        if os.path.exists(os.path.join(d, "index.html")):
            return d
    return here

OUT = os.path.join(_book_dir(), "audio")
FORCE = "--force" in sys.argv

def fmt(n, u): return f"{'+' if n >= 0 else ''}{n}{u}"

async def one(name, role, text, rate, dp, dv):
    cfg = ROLES[role]
    path = os.path.join(OUT, name + ".mp3")
    if not FORCE and os.path.exists(path) and os.path.getsize(path) > 1200:
        print(f"  - {name}.mp3  已存在，跳過"); return
    c = edge_tts.Communicate(text, cfg["voice"], rate=fmt(rate, "%"),
                             pitch=fmt(cfg["pitch"] + dp, "Hz"), volume=fmt(cfg["vol"] + dv, "%"))
    await c.save(path)
    print(f"  OK {name}.mp3  [{role}] {os.path.getsize(path)/1024:5.1f} KB   {text[:16]}")

async def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 58); print(f"  《我自己來》配音生成中 — 共 {len(LINES)} 句"); print("=" * 58)
    ok, fail = 0, []
    for item in LINES:
        try:
            await one(*item); ok += 1
        except Exception as e:
            fail.append(item[0]); print(f"  X {item[0]}.mp3 失敗：{str(e)[:80]}")
        await asyncio.sleep(0.35)
    print("-" * 58); print(f"完成 {ok} / {len(LINES)} 句 -> {OUT}")
    if fail: print("失敗：" + "、".join(fail) + "（再跑一次會自動補生成）")
    if shutil.which("ffmpeg"):
        print("偵測到 ffmpeg，統一音量中 ...")
        for name, *_ in LINES:
            src = os.path.join(OUT, name + ".mp3")
            if not os.path.exists(src): continue
            tmp = src + ".tmp.mp3"
            r = subprocess.run(["ffmpeg", "-y", "-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                                "-ar", "44100", "-ac", "1", "-b:a", "96k", tmp], capture_output=True)
            if r.returncode == 0: os.replace(tmp, src)
            elif os.path.exists(tmp): os.remove(tmp)
        print("音量統一完成。")

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
