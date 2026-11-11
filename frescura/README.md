# FRESCURA BODY — iklan testimoni (PREVIEW)

Struktur: **Intro (video 6.MOV) → Testimoni (F9.MOV) → Closing (6.MOV) → End card**, ±31 saat, 1080×1920.

| Masa | Babak | Visual |
|---|---|---|
| 0.0–1.5 | Hook "Masih ragu-ragu nak cuba FRESCURA BODY?" | B-roll pump di pantai, tajuk kinetik besar, impact + whoosh |
| 1.5–2.8 | "Sebelum korang buat keputusan" | Kad editorial ivory, B-roll pump buih, ticker Aromatherapy/Ocean Salt/Gentle Foaming, toggle RAGU→YAKIN |
| 2.8–5.3 | "Tengok dulu apa kata pelanggan kami" | 3 polaroid testimoni, ★★★★★, transisi buka ke testimoni |
| 5.3–19.3 | Testimoni | A-roll pelanggan (punch-in setiap potongan), callout Lembut/Wangi, cop "100% jujur", checklist, cutaway buih + "Rahsia di sebalik keharuman", "fresh." |
| 19.4–28.0 | Closing | Dah yakin ✓, jam "jangan tangguh", meter stok terhad, beg kuning + checkout, kad harga TikTok Shop |
| 28.0–30.9 | End card | Produk, wordmark FRESCURA BODY, CTA "Tekan beg kuning sekarang" |

## Pipeline
1. `scripts/transcribe.py` — faster-whisper large-v3 (BM), cap masa setiap perkataan → `transcript/`
2. Demucs (htdemucs_ft) asingkan suara → `scripts/run_df.py` DeepFilterNet3 buang noise → EQ/de-ess/kompresor "studio"
3. `scripts/edit.py` — potongan intro/testimoni/closing, buang jeda & ayat berulang, laju 1.13× (suara anda) / 1.07× (testimoni), rubberband (pitch kekal); video testimoni dipotong sama (sync tepat frame)
4. `scripts/sound.py` — 19 sound FX + muzik 120 BPM disintesis (tiada sampel pihak ketiga), duck bawah suara, mix −12 LUFS
5. `scripts/build.py` — jana komposisi HyperFrames `project/index.html` (GSAP, masa ikut perkataan)
6. Render: `cd project && npx hyperframes render . -q draft` (preview) / `-q delivery` (final, tanpa `--preview` watermark)

Font: Bodoni Moda (italic, aksen) + Manrope (caption). Palet: ivory, rose #9B1B30, blush, champagne gold.
