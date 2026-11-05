# Video 11: "3 sebab sabun ni bau perfume mahal" (konsep bandar: KLCC / Kuala Lumpur / New York)

**Status: PREVIEW v1**, `preview/preview_v1.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Sumber: `src/main.mp4` (klien bercakap, 57.0 s) + `src/part2.mp4` (footage pam & buih Woman Glory klien, sama seperti Video 10).
- Selepas edit: **44.9 s** (43.3 s suara + 1.6 s kad penutup).
- Hook: *"Serius, sabun ni bau perfume mahal. Kalau tak percaya, tengok video ni sampai habis."* Muka: **0.80 s sahaja** (bawah 1 saat), mata ke lensa, hflip.
- Suara: bilik senyap (lantai ~−48 dBFS). 8 segmen disamakan level → RNNoise + FFT denoise, gate, EQ, de-esser, compressor, exciter, gandaan tetap −14 LUFS, dipercepat 1.12x tanpa ubah pitch. Mix −13 LUFS.
- Permintaan klien: produk berlatarkan **bandar** (KLCC, Bukit Bintang, Komtar, Menara Kedah, vibe New York), tetap luxury minimalis & estetik, edit tidak terlalu detail.

## Konsep "Metro Noir" (belum pernah digunakan)
- **Produk dalam bandar:** botol dipotong dari gambar produk klien (BiRefNet, `rembg`); piksel botol/label **tidak diubah**, hanya latar dibuang. Botol "terapung" atas footage bandar dengan **pantulan lantai kaca** dan cahaya amber di bawahnya.
- **Lokasi:** KLCC (Menara Berkembar Petronas dari bawah, waktu malam, skyline senja), Kuala Lumpur (siang → malam, trafik malam, skyline siang dengan Menara KL, udara malam), New York (bokeh skyline, Times Square). Pil lokasi di atas kiri setiap babak.
- **Font baru:** **Syncopate** (huruf besar lebar gaya seni bina) + **Figtree** (caption tebal 72 px). **Palet:** malam, krom, neon amber; mawar (Woman Glory) & violet (Noche); kuning hanya untuk beg kedai.
- **Teknik baru:** peralihan **jejak lampu kereta** (streak amber), nombor **berbingkai garis** 01/02/03, footage pam klien dalam **tingkap kaca** atas bandar, garis gelombang wangian, "RM" berbingkai di Times Square, cop "RUGI GILA WEH", butang beg kuning, bar stok, CHECK OUT ✓.
- **Caption baru:** krom putih; kata kunci **menyala neon amber** ketika disebut.

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 5.9–8.5, 18.96–19.14, 37.6–38.4, 46.5–46.9, 52.9–54.9 | jeda | awkward pause |
| 53.1–54.7 "Tekan dan check out sekarang." | dibuang | ulangan (hampir sama dengan ayat terakhir "Tekan beg kuning dan check out sekarang.") |
| jeda dalam ayat | dirapatkan | pace |

## Storyboard (masa selepas edit)
| Masa | Suara | Visual |
|---|---|---|
| 0.00–0.80 | Serius, | **Muka klien (0.80 s)** |
| 0.80–2.97 | sabun ni bau perfume mahal. | KLCC (Petronas dari bawah) + botol Woman Glory + "PERFUME MAHAL" |
| 2.97–4.99 | Kalau tak percaya, tengok video ni sampai habis. | Bokeh New York + "SAMPAI HABIS" + bar |
| 4.99–8.01 | 3 sebab sabun ni bau perfume mahal. Frescura Body. | KL siang → malam + "3" berbingkai + duo botol + FRESCURA BODY |
| 8.01–11.72 | 01 wangian dia memang inspirasi perfume. | Skyline KLCC senja + "INSPIRASI PERFUME" + Woman Glory |
| 11.72–14.16 | Sekali cium, terus bau perfume mahal. | New York malam + garis gelombang wangian |
| 14.16–16.37 | 02 ada 2 bau premium. | Trafik malam KL + Woman Glory & Noche |
| 16.37–19.33 | Bombshell, fresh dan feminine. Sesuai pakai hari-hari, | KL siang + Woman Glory by Bombshell + FRESH / FEMININE / ☀ HARI-HARI |
| 19.33–22.57 | Midnight Fantasy, manis dan fruity. Sesuai untuk malam. | KLCC malam + Noche by Midnight Fantasy + MANIS / FRUITY / ☾ UNTUK MALAM |
| 22.57–25.84 | 03 tekan je terus keluar buih lembut. | Bandar dari udara + **footage pam klien** dalam tingkap kaca |
| 25.84–29.24 | Ada sea salt yang kaya mineral, mandi pun rasa mewah. | Bokeh New York + **buih digosok** + SEA SALT / KAYA MINERAL / "MEWAH" |
| 29.24–31.26 | Kau sanggup beli perfume ratus-ratus. | Times Square + "RM" + "RATUS-RATUS" |
| 31.26–35.14 | Tapi sabun yang bau perfume mahal ni, kau nak lepaskan? | Bokeh New York + duo botol |
| 35.14–36.28 | Rugi gila weh. | "RUGI GILA WEH" |
| 36.28–38.11 | Tekan beg kuning sekarang. Check out sekarang. | Trafik KL + butang beg kuning ditekan |
| 38.11–41.43 | Sebab stok kami memang dah tak banyak. Sangat-sangat terhad. | Petronas dari bawah + bar stok surut + TERHAD |
| 41.43–43.28 | Tekan beg kuning dan check out sekarang. | Butang CHECK OUT → ✓ + konfeti |
| 43.28–44.88 | (penutup) | KLCC malam + duo botol + FRESCURA BODY + TEKAN BEG KUNING |

## Nota
- **Komtar dan Menara Alor Setar** tiada dalam stok video percuma (Mixkit); preview guna KLCC / Kuala Lumpur dan New York. Kalau klien ada footage Komtar / Menara Kedah sendiri, boleh dimasukkan.
- Caption: "Fresh kurang bodi" → *Frescura Body*, "sisat/silsat" → *sea salt*, "perasaan" → *pun rasa*, "back kuning" → *beg kuning*, "minat fantasi" → *Midnight Fantasy*, "100-100" → *ratus-ratus*.

## Sumber
- Footage klien: `part2.mp4`. Gambar produk klien: duo_white (dipotong; dipecah kepada botol tunggal Woman Glory & Noche).
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License): 20137, 20122, 20121, 30988, 20128, 39442, 49873, 4330, 4087, 24516.
- Fon: Syncopate (Apache License 2.0), Figtree (SIL OFL), google/fonts.
- SFX & muzik: disintesis sendiri (`make_audio.py`; kalimba 104 bpm Am9–G6–Fmaj7–Em7). Komposisi: HyperFrames v0.9.10.

## Cara build semula
```bash
cd video11
python3 -I ../scripts/edit_audio.py src/main.mp4 sh.rnnn audio cuts.json
./voice_studio.sh
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words_seg.json && cp audio/words_seg.json project/assets/audio/words.json
python3 -I prep_broll.py mixkit project/assets/broll src/main.mp4 src/part2.mp4
python3 cutout.py ../video4/project/assets/product/duo_white.jpg   # rembg BiRefNet cut-out (*_cut.png), then split into glory_single / noche_single
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
