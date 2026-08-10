# 小小繪本書架 🐰

會說故事的 HTML 幼兒互動繪本。按下播放鍵，就有人陪孩子一起唸。

## 線上閱讀

啟用 GitHub Pages 後：`https://<你的帳號>.github.io/<repo 名稱>/`

## 目錄結構

```
.
├── index.html                        書架入口（列出所有繪本）
├── .nojekyll                         讓 GitHub Pages 原樣輸出靜態檔
├── README.md
└── books/
    └── rabbit-courage/               ← 一本繪本 = 一個資料夾
        ├── index.html                繪本本體
        ├── audio/                    這本的配音（p1-1.mp3 ~ p8-3.mp3）
        └── tools/
            ├── 生成配音.py
            ├── 一鍵生成配音.bat
            └── 配音腳本.md
```

規則只有一條：**每本繪本的 `index.html` 和它的 `audio/` 必須在同一層**（程式用相對路徑 `audio/pX-Y.mp3` 找音檔）。

## 怎麼新增下一本繪本

1. 在 `books/` 底下建一個新資料夾，例如 `books/seed-patience/`
2. 把新繪本的 `index.html`、`audio/`、`tools/` 放進去
3. 打開根目錄的 `index.html`，在 `BOOKS` 陣列加一筆：

```js
{
  id:'seed-patience',
  title:'一顆很慢很慢的種子',
  en:'THE SLOW LITTLE SEED',
  desc:'一顆種子怎麼也長不快，其他花都開了，只有它還埋在土裡……',
  tags:['耐心','成長'],
  age:'4-6 歲',
  pages:8, mins:3,
  href:'books/seed-patience/index.html',
  cover:'generic'          // 還沒畫封面就先用 generic
}
```

篩選標籤會自動從 `tags` 產生，不用另外設定。

想畫專屬封面就在 `COVERS` 裡加一個函式（回傳 400×260 的 SVG 內容），再把 `cover` 改成那個名字。

## 現有繪本

| 繪本 | 年齡 | 頁數 | 主題 |
|---|---|---|---|
| 小豆的勇氣 | 4-6 歲 | 8 | 勇氣 ・ 獨立 ・ 親子 |

## 產生配音

進到該繪本的 `tools/` 資料夾，Windows 雙擊 `一鍵生成配音.bat`；其他系統：

```bash
pip install edge-tts
python books/rabbit-courage/tools/生成配音.py
```

使用微軟 Edge 神經語音（免註冊、免 API 金鑰、免費），音檔會自動生成到該繪本的 `audio/`。

沒有音檔也能正常閱讀 —— 繪本會自動改用瀏覽器內建語音朗讀。
