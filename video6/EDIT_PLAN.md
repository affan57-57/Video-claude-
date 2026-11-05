# Video 6: "Balik kerja: 5 perkara" (tips → Frescura Body → share)

**Status: PREVIEW**, `preview/preview_v1.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Asal: 58.9 s. Selepas edit: **49.0 s** (47.5 s suara + 1.5 s kad penutup).
- Muka: **0.78 s sahaja** (0.38–1.16 s, "kerja, jangan"; ikut permintaan terakhir: bawah 1 saat). Mata tepat ke lensa; hflip (poster "Massage Your Baby" terbaca betul). Selepas 5 saat pertama rakaman, telefon terdongak ke siling, jadi selebihnya B-roll dan motion graphics sepenuhnya.
- Suara: bilik senyap (lantai ~−45 dBFS). 14 segmen disamakan level, RNNoise + FFT denoise, gate, EQ (kehangatan, potong "box", presence, air), de-esser, compressor ringan, exciter, gandaan tetap −14 LUFS (`voice_studio.sh`). Mix −13 LUFS: suara di depan, SFX kuat, muzik lembut 90 bpm.

## Gaya baru: "Editorial Espresso" (belum pernah digunakan)
- **Tipografi:** Bodoni Moda (serif editorial berkontras tinggi) + Manrope. **Palet:** espresso, pasir, krim, tembaga (brass), sage.
- **Teknik motion baharu:** perkataan sebagai tingkap ("KERJA" dengan footage pejabat di dalam huruf); nombor bab besar bergaris luar (01–05) yang meluncur masuk; bingkai **gerbang (arch)**; **grid bento** 3 jubin; **film-strip** (kad meluncur ke sisi); **marquee** senarai tip; peralihan **blinds** (5 bilah tembaga) setiap bab; **bulatan panduan nafas** (TARIK → HEMBUS); **kad telefon ditolak keluar**, notifikasi jatuh, **suis ON → OFF**; **piring hitam berputar + equalizer** hidup; **letterbox sinematik** untuk keluarga; **pull-quote** editorial; **spec sheet** dengan garis penunjuk pada botol; **senarai semak ringkasan** 5 tip yang ditanda satu-satu; caption tanpa pil (perkataan menyala ikut suara); progress bar **menegak**.

## Maklum balas
- **Tulisan dibesarkan** (~20–30%): caption 62 px (tebal), label 30 px, tajuk Bodoni 124–150 px, italik 70–132 px, senarai semak 56 px, spec 34 px, notifikasi 38 px, butang SHARE 50 px. Ruang kosong, garis halus dan palet dikekalkan supaya rasa luxury tidak hilang; susun atur dilaras supaya tiada pertindihan.

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 4.6–5.5, 9.0–10.5, 15.0–16.3, 18.9–21.1, 25.1–26.5, 31.6–32.1, 35.3–35.8, 38.1–38.4, 43.9–44.8, 49.7–49.9, 52.0–52.9 | jeda | awkward pause |
| 19.3–20.2 | "Haa…" | filler |
| 58.6–58.9 "…selepas ini" | dibuang | rakaman tamat di tengah "ini"; ayat ditamatkan dengan lengkap pada "…tahu cara menjaga diri." |
| 8 jeda pendek | dirapatkan | pace |

## Storyboard (masa selepas edit)
| Masa | Suara | Visual |
|---|---|---|
| 0.00–0.38 | Balik | "Balik" Bodoni italic, punch |
| 0.38–1.16 | kerja, jangan | **Muka (0.78 s)** + "kerja," |
| 1.16–2.26 | terus fikir pasal kerja | "KERJA" dengan footage pejabat di dalam huruf, dicoret tembaga |
| 2.26–3.78 | Cuba buat 5 perkara ini | "5" gergasi bergaris luar + marquee 5 tip |
| 3.78–7.40 | 01 Tarik nafas pelan-pelan, tenangkan fikiran | Arch laut senja + bulatan nafas TARIK/HEMBUS |
| 7.40–11.88 | 02 Jauhkan diri sekejap daripada telefon & media sosial | Kad telefon ditolak keluar, notifikasi jatuh, suis OFF |
| 11.88–14.24 | 03 Dengar lagu yang korang suka | Piring hitam berputar dalam bulatan + equalizer |
| 14.24–18.18 | 04 Luangkan masa dengan keluarga / orang tersayang | Letterbox siluet keluarga senja + hati dilukis |
| 18.18–23.10 | 05 Mandi & nikmati masa untuk diri sendiri | Bento: tab mandi berbuih, lilin, pam berbuih |
| 23.10–26.00 | Kadang-kadang kita tak perlukan sesuatu yang besar untuk berehat | Tuang teh + pull-quote |
| 26.00–29.04 | Cukup dengan beri ruang kepada diri sendiri | Film-strip ke buku + petikan besar |
| 29.04–33.68 | Rutin mandi lebih istimewa, korang kena cuba | Arch produk duo |
| 33.68–39.46 | Frescura Body, mengandungi sea salt & pilihan wangian berinspirasikan perfume | FRESCURA BODY + spec sheet: SEA SALT / PILIHAN WANGIAN / ALA PERFUME |
| 39.46–41.56 | seperti Bombshell dan Midnight Fantasy | Film-strip kad Woman Glory + Noche |
| 41.56–47.51 | Kalau tips ni bermanfaat, share video ni, supaya lebih ramai tahu cara menjaga diri | Senarai semak 5 tip + butang SHARE |
| 47.51–49.00 | (penutup) | FRESCURA BODY, Woman Glory · Noche |

## Perlu pengesahan
- Muka 0.78 s (bawah 1 saat). Borang tulis "2 saat"; kalau mahu 2 saat, beritahu.
- "Mengandungi **sea salt**": whisper dengar "sisa"; label botol tertulis "Ocean Salt". Kalau ayatnya lain, beritahu.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License): 24344, 34363, 14669, 48459, 6213, 47057, 3438, 9267, 1724. Keluarga ditunjuk sebagai siluet.
- Fon: Bodoni Moda, Manrope (SIL Open Font License, google/fonts).
- SFX & muzik: disintesis sendiri (`make_audio.py`). Komposisi: HyperFrames v0.9.10.

## Cara build semula
```bash
cd video6
python3 -I ../scripts/edit_audio.py src/main.mov sh.rnnn audio cuts.json   # snap_win 0.02, quiet_db -36
./voice_studio.sh
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words.json && cp audio/words.json project/assets/audio/
python3 -I prep_broll.py mixkit project/assets/broll src/main.mov
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
