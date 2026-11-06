# FRESCURA Body — Night City Edit (PREVIEW)

Konsep: **luxury minimalis, malam di bandar**: KLCC, Bukit Bintang, Komtar (Pulau Pinang) dan Menara Alor Setar (Kedah).
Dibina dengan **HyperFrames** (HTML → video, GSAP). Format 1080×1920, 30 fps.

> Ini **preview draft** sahaja, belum render final. Bila awak setuju, render final guna `-q delivery`.

## Video
Satu video sahaja (video muka `5_6298316097858838513.MOV` tersilap upload, tidak digunakan).

| Sumber | Tempoh asal → selepas potong | Gaya |
|---|---|---|
| `5_6298316097858838616.MOV` (suara sahaja) | 54.4s → 47.2s (+1s hujung) | Motion graphic + B-roll atas **gambar & video sebenar** bandar malam |

## Latar bandar (gambar/video SEBENAR, bukan kartun)
| Bahagian | Latar |
|---|---|
| Hook | KLCC + Suria KLCC waktu malam |
| 3 benda / botol reveal | Petronas dari bawah (jambatan langit) |
| 01 Buih siap-siap | **Video** monorel Bukit Bintang waktu malam |
| 02 Ocean salt | Komtar → lampu Pulau Pinang & jambatan dari Bukit Bendera |
| 03 Wangi perfume | Menara Alor Setar → KLCC |
| Soalan "sabun biasa vs Frescura" | Jalan P. Ramlee (orang ramai, Petronas) |
| CTA beg kuning | Skyline KL waktu malam |

Komtar & Menara Alor Setar: tiada gambar malam berlesen bebas-komersial, jadi gambar siang (CC BY) digred jadi suasana malam.
Semua kredit gambar dalam `CREDITS.md` (wajib letak kredit bila post).

B-roll: `tekan pump yg baru .MOV` (tekan pam, buih di tapak tangan, sapuan buih).

## Audio
- Buang bising: **DeepFilterNet3** (had 18 dB supaya suara tak jadi robot).
- Suara studio: high-pass 85 Hz, kurang "muddy" 250 Hz, presence +3 dB @3 kHz, de-esser, compressor 3:1, loudness −15 LUFS.
- Buang jeda janggal: setiap senyap > 0.2s dipendekkan ke ~0.11s (potong ikut frame, lip-sync kekal).
- Muzik: "Kleiber (Deep House Mix)" oleh Hasenchat (Jamendo, **CC BY 3.0**), ~129 BPM, perlahan bawah suara. **Wajib letak kredit** bila post.
- SFX (Pixabay, bebas guna): whoosh, impact bass, pop, ping, sparkle, click, riser, glitch.

## Transkrip & plan visual

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

## B-roll pump: latar bilik air mewah
Latar asal video pump (dinding belang, meja hijau) dibuang dengan AI (HyperFrames remove-background),
diganti dengan bilik air moden minimalis: kaunter kayu + sinki batu + lilin + pancur hujan (syot 1),
sinki kabur (syot 2), ruang shower kaca (sapu buih). Ditambah titisan air pancur beranimasi + wap halus.
Fail penuh: `output/broll/pump_bilik_air_mewah.mp4` (1080×1920, tanpa audio).

## Animasi edukasi
| Point | Animasi |
|---|---|
| Reveal produk | Dua botol sebenar (NOCHE + Woman Glory Bombshell) naik atas podium emas, kilauan cahaya |
| 01 Buih siap-siap | Perbandingan **Sabun biasa: 3 langkah** (basahkan span → gosok lama → baru berbuih, *LECEH*) vs **Frescura: 1 langkah** (tekan pam → terus buih, gelembung pop) |
| 01 (B-roll buih) | Formula animasi **Cecair + Udara = Buih lembut** |
| 02 Ocean salt | Proses **Air laut → Disejat matahari → Kristal garam** (anak panah dilukis, wap naik), kemudian kristal 3D + **Mg · Ca · K** |
| 03 Wangi perfume | **Piramid wangian** perfume dibina bertingkat: Base note (tahan lama) → Heart note (jiwa wangian) → Top note (bau pertama) |
| "terus wangi" | Cincin wangian merebak dari tengah |

Gambar produk: gambar yang awak upload (botol dipotong & diletak atas latar bandar).

## Pembetulan ejaan kapsyen (Whisper)
"fresh kura body" → **Frescura Body**, "sisap/silsat" → **sea salt**, "bombsher" → **Bombshell**,
"mainan/minat fantasi" → **Midnight Fantasy**, "bui" → **buih**, "kuni" → **kuning**, "terahat" → **terhad**, "cek out" → **checkout**.
(Disahkan dari gambar produk: **NOCHE · Midnight Fantasy** dan **Woman Glory · Bombshell**.)

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
