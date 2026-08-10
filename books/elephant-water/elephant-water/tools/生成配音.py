# -*- coding: utf-8 -*-
"""《小象的一鼻子水》一鍵配音生成器 — 微軟 Edge 神經語音（免註冊、免金鑰、免費）"""
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
    "嘟嘟": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 16,
        "vol": 0
    },
    "小鳥": {
        "voice": "zh-TW-HsiaoYuNeural",
        "pitch": 34,
        "vol": -6
    }
}

LINES = [
    ("p1-1", "旁白", "那一年的夏天，好久好久沒有下雨。", -22, 0, 0),
    ("p1-2", "旁白", "河乾了，草黃了，連風都是燙的。", -24, 0, 0),
    ("p2-1", "旁白", "小象嘟嘟走了好遠，才找到最後一個小水窪。", -16, 0, 0),
    ("p2-2", "旁白", "只剩這麼一點點了。", -26, 0, 0),
    ("p3-1", "旁白", "嘟嘟把水吸進長長的鼻子裡。", -14, 0, 0),
    ("p3-2", "嘟嘟", "我要帶回去給大家喝。", -18, 0, 0),
    ("p4-1", "旁白", "走著走著，他看見一隻小鳥，站在樹枝上。", -14, 0, 0),
    ("p4-2", "小鳥", "我……好渴。", -32, 0, 0),
    ("p5-1", "旁白", "嘟嘟想了一下下。", -24, 0, 0),
    ("p5-2", "旁白", "然後噴出一點點水，剛好裝滿小鳥的嘴巴。", -18, 0, 0),
    ("p6-1", "旁白", "再走一段路，遇到走不動的老烏龜。", -14, 0, 0),
    ("p6-2", "旁白", "他的殼，已經曬得發燙了。", -22, 0, 0),
    ("p7-1", "旁白", "嘟嘟又分了一點。", -18, 0, 0),
    ("p7-2", "旁白", "鼻子裡的水，剩下一半了。", -22, 0, 0),
    ("p8-1", "旁白", "然後是三隻小螞蟻。", -12, 0, 0),
    ("p8-2", "旁白", "然後是一隻找不到花的蝴蝶。", -14, 0, 0),
    ("p8-3", "旁白", "每一次，嘟嘟都分了一點點。", -22, 0, 0),
    ("p9-1", "旁白", "最後，他看見一株快枯掉的小草。", -22, 0, 0),
    ("p9-2", "旁白", "鼻子裡，只剩最後一滴了。", -30, 0, 0),
    ("p10-1", "旁白", "嘟嘟低下頭，把最後一滴水給了它。", -26, 0, 0),
    ("p10-2", "旁白", "回到家的時候，鼻子裡，一滴也不剩。", -24, 0, 0),
    ("p11-1", "旁白", "那天半夜，嘟嘟被聲音吵醒了。", -20, 0, 0),
    ("p11-2", "旁白", "滴答、滴答、滴答，", -26, 0, 0),
    ("p11-3", "嘟嘟", "下雨了！", 2, 0, 0),
    ("p12-1", "旁白", "第二天早上，草綠了，河也回來了。", -12, 0, 0),
    ("p12-2", "旁白", "嘟嘟仰起頭，喝了好大好大一口。", -14, 0, 0),
    ("p12-3", "旁白", "他覺得這場雨，好像特別特別甜。", -30, 0, 0),
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
    print("=" * 58); print(f"  《小象的一鼻子水》配音生成中 — 共 {len(LINES)} 句"); print("=" * 58)
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
