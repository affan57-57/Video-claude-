# FRESCURA Body — Night City Edit (PREVIEW)

Konsep: **luxury minimalis, malam di bandar**: KLCC, Bukit Bintang, Komtar (Pulau Pinang) dan Menara Alor Setar (Kedah).
Dibina dengan **HyperFrames** (HTML → video, GSAP). Format 1080×1920, 30 fps.

> Ini **preview draft** sahaja, belum render final. Bila awak setuju, render final guna `-q delivery`.

## Dua video

| Video | Sumber | Tempoh asal → selepas potong | Gaya |
|---|---|---|---|
| **V1** | `5_6298316097858838616.MOV` (suara sahaja, kamera tunjuk sofa) | 54.4s → 47.2s (+1s hujung) | Penuh motion graphic + B-roll, tiada A-roll |
| **V2** | `5_6298316097858838513.MOV` (muka bercakap) | 57.0s → 50.4s (+1s hujung) | A-roll dalam bingkai emas atas latar bandar + B-roll + motion graphic |

B-roll: `tekan pump yg baru .MOV` (tekan pam, buih di tapak tangan, sapuan buih).

## Audio
- Buang bising: **DeepFilterNet3** (had 18 dB supaya suara tak jadi robot).
- Suara studio: high-pass 85 Hz, kurang "muddy" 250 Hz, presence +3 dB @3 kHz, de-esser, compressor 3:1, loudness −15 LUFS.
- Buang jeda janggal: setiap senyap > 0.2s dipendekkan ke ~0.11s (potong ikut frame, lip-sync kekal).
- Buang ayat berulang (V2): "Tekan dan cek out sekarang." (53.1–54.9s) dibuang; tinggal "Tekan beg kuning dan cek out sekarang."
- Muzik: "Kleiber (Deep House Mix)" oleh Hasenchat (Jamendo, **CC BY 3.0**), ~129 BPM, perlahan bawah suara. **Wajib letak kredit** bila post.
- SFX (Pixabay, bebas guna): whoosh, impact bass, pop, ping, sparkle, click, riser, glitch.

## Transkrip & plan visual

### V1
| Masa | Ayat | Visual | SFX |
|---|---|---|---|
| 0.0 | "Oh! Sebelum kau beli sabun mandi baru…" | HOOK: **JANGAN / BELI SABUN / dulu…** atas KLCC | impact bass |
| ~2.7 | "tengok ni dulu" | **TENGOK / ni dulu.** slam | whoosh, pop |
| ~3.6 | "Jangan sampai duit kau terbazir" | **DUIT** emas + syiling RM jatuh, *terbazir.* merah | impact, glitch |
| ~5.7 | "Tiga benda yang sabun biasa tak boleh bagi…" | Angka **3** gergasi + "Benda" | whoosh cinematic |
| ~8.5 | "…tapi Frescura Body boleh!" | Botol naik atas podium + halo + kilauan | impact, sparkle |
| ~10.7 | "Pertama, buih siap-siap" | **01 Buih siap-siap** (Bukit Bintang, monorel) | ping |
| ~12.8 | "Tak perlu span, tak perlu gosok" | Kad kaca ✕ span ✕ gosok | pop ×2 |
| ~14.6 | "tekan pam, buih lembut terus ada di tangan" | B-roll tekan pam → buih di tapak tangan | whoosh, click, sparkle |
| ~17.2 | "Yang kedua, sea salt / garam laut" | **02 Ocean salt** (Komtar) | ping |
| ~20.4 | "yang kaya mineral semula jadi" | Kristal garam 3D + kad edukasi **Mg · Ca · K** | pop ×3 |
| ~22.2 | "kulit rasa segar macam baru lepas mandi laut" | B-roll sapuan buih "Segar macam mandi laut" | whoosh |
| ~24.4 | "Yang ketiga, wangi perfume" | **03 Wangi perfume** + botol perfume line-art + kabus (Menara Alor Setar) | sparkle |
| ~27.2 | "Pilih Bombshell… atau Midnight Fantasy…" | Kad **Bombshell** (fresh · feminine) & **Midnight Fantasy** (manis · fruity · malam) | whoosh, pop |
| ~33.3 | "Keluar bilik air je, terus wangi" | **terus wangi.** + aura zarah | sparkle |
| ~35.0 | "Kau nak beli sabun biasa lagi atau…" | Perbandingan *Sabun biasa* VS *Frescura* + gelembung "Pakai perfume apa ni?" | whoosh, pop |
| ~41.3 | "Pilihan kat tangan kau" | **Pilihan / di tangan kau.** | impact |
| ~41.7 | "Tapi ingat, stok kami dah tak banyak" | Bar **STOK terhad** menyusut | whoosh |
| ~44.7 | "Tekan beg kuning sekarang… checkout" | Beg kuning berdenyut + anak panah ke bakul + butang **CHECKOUT SEKARANG** | riser→impact, click |

### V2
| Masa | Ayat | Visual |
|---|---|---|
| 0.0 | "Serius, sabun ni bau perfume mahal." | Muka dalam bingkai emas + **SABUN NI BAU / perfume mahal?** |
| ~3.2 | "Kalau tak percaya, tengok video ni sampai habis." | **Tak percaya? / tengok sampai habis.** |
| ~5.5 | "Tiga sebab… Frescura Body." | **3 Sebab** → botol reveal |
| ~9.3 | "Sebab pertama, wangian dia memang inspirasi perfume." | A-roll penuh + chip **01 Inspirasi perfume** + punch-in |
| ~13.5 | "Sekali cium, terus bau perfume mahal." | Botol perfume line-art + kabus, **terus mahal.** |
| ~16.4 | "Yang kedua, ada dua bau premium." | **02 Dua bau premium.** atas bingkai A-roll |
| ~19.1 | "Bombshell… Midnight Fantasy…" | Kad wangian (hari-hari / untuk malam) |
| ~26.2 | "Yang ketiga, tekan je terus keluar buih lembut." | **03 Tekan je** → B-roll tekan → buih |
| ~30.9 | "Ada sea salt yang kaya mineral" | Kristal garam + **Mg · Ca · K** |
| ~33.3 | "mandi pun rasa mewah" | B-roll sapuan buih "Mandi pun rasa mewah" |
| ~34.5 | "Kau sanggup beli perfume ratus-ratus." | Botol perfume + tanda harga **RM ratus-ratus** + **Sanggup?** |
| ~37.2 | "Tapi sabun yang bau perfume mahal ni, kau nak lepaskan?" | A-roll + **kau nak lepas?** |
| ~41.9 | "Rugi gila weh." | **RUGI** merah slam + punch-in + glitch |
| ~42.7 | "Tekan beg kuning… stok terhad… checkout sekarang" | CTA beg kuning + stok terhad + butang checkout |

## Pembetulan ejaan kapsyen (Whisper)
"fresh kura body" → **Frescura Body**, "sisap/silsat" → **sea salt**, "bombsher" → **Bombshell**,
"mainan/minat fantasi" → **Midnight Fantasy**, "bui" → **buih**, "kuni" → **kuning**, "terahat" → **terhad**, "cek out" → **checkout**.
(Nama "Midnight Fantasy" ialah tekaan saya dari bunyi "minat fantasi". Sila sahkan.)

## Tipografi (baru, lain dari sebelum ni)
- **Syne** (700/800): kapsyen & tajuk, besar dan jelas.
- **Bodoni Moda Italic**: perkataan penting (emas), rasa luxury/fashion.
- **Syncopate**: label kecil (lokasi, "Frescura Body").

## Render semula
```bash
python3 tools/build.py v1 <scratch>    # jana projek HyperFrames
cd proj_v1 && npx hyperframes render -q draft     # preview
cd proj_v1 && npx hyperframes render -q delivery  # FINAL (bila dah approve)
```
