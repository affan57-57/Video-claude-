# Video 7: "Wanita lebih yakin: 5 perkara" (tips → garam laut → Frescura Body)

**Status: PREVIEW v5**, `preview/preview_v5.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Asal: 57.3 s. Selepas edit: **46.9 s** (45.4 s suara + 1.5 s kad penutup).
- Muka: **0.64 s sahaja**, dari rakaman klien sendiri (wanita berpurdah), 0.00–0.64 s pada "Wanita,"; jelas bawah 1 saat. Mata tepat ke lensa (rakaman 1.40–2.04 s; berpurdah, tiada isu lip-sync); hflip. Selepas 7 saat pertama telefon terdongak ke siling, jadi selebihnya B-roll dan motion graphics sepenuhnya.
- Suara: bilik senyap (~−47 dBFS). 11 segmen disamakan level → RNNoise + FFT denoise, gate, EQ (kehangatan, potong "box", presence, air), de-esser, compressor ringan, exciter, gandaan tetap −14 LUFS (`voice_studio.sh`). Mix −13 LUFS: suara depan, SFX kuat, muzik lembut.

## Maklum balas
- **v2: cakap lebih laju & rancak.** Suara dipercepat ~15% dengan time-stretch yang mengekalkan pitch (`TEMPO=1.15` dalam `voice_studio.sh`) dan jeda dirapatkan lagi. Suara 45.4 s → 39.4 s; video 46.9 s → **41.0 s**. Semua babak/SFX dipetakan semula secara automatik ke suara baru melalui padanan perkataan (`words_scene_timeline.json` → `words.json`), dan sempadan babak yang jatuh di tengah perkataan di-snap (contoh: babak fakta tamat tepat sebelum "Sebab tu"). Muka kini **0.56 s**.

- **v3:** "5" kedengaran berulang. Rakaman sebenarnya: "…diri sendiri, *cuba lima…* cuba buat lima perkara ni" (cubaan pertama tersasul). Bahagian 3.98–5.00 s ("cuba lima") dibuang, jadi kini "…diri sendiri, cuba buat 5 perkara ni" dengan satu "5" sahaja. Muka berpurdah **dicerahkan** bingkai demi bingkai (`face_glow.py`: kulit dilicinkan edge-preserving, pencahayaan diangkat, kulit lebih cerah & rona peach segar, cahaya lembut, mata kekal tajam; wajah tidak diubah). Odometer diberi kesan pudar atas/bawah supaya hanya satu nombor jelas ketika bergolek.

- **v4: klip sambungan** (`part2.mov`, suara sahaja, video gelap): nama penuh wangian dirakam semula dan disisipkan ke ayat akhir: "Kita ada pilihan **Woman Glory by Bombshell** dan **Noche by Midnight Fantasy** untuk menjadikan rutin mandi lebih istimewa." Kedua-dua rakaman digabung jadi `src/voice_sources.wav` (main dipad ke 58.0 s + part2), level disamakan per segmen, rantaian studio + tempo 1.15 yang sama. Polaroid berlabel "Woman Glory by Bombshell" / "Noche by Midnight Fantasy" jatuh tepat pada nama masing-masing. Video kini **41.5 s**.

- **v5: klip penutup** (`part3.mov`, telefon terdongak, jadi motion graphics/B-roll sahaja): "Kalau korang sayangkan diri sendiri, jangan simpan tips ni untuk diri sendiri. Cuba share video ni supaya lebih ramai wanita sedar pentingnya menjaga diri. Dan kalau korang percaya setiap wanita berhak rasa yakin dan istimewa, komen yakin." ("Komen yakin" berulang + "Ok" dibuang.) Tiga babak baru: hati dilukis + "sayangkan diri sendiri" + bookmark dicoret; B-roll wanita bertudung dengan telefon + **rangkaian share**; kotak komen kaca "YAKIN" ditaip + butang hantar + pelekat. Kad penutup dialih ke selepas outro. Video kini **54.8 s**.

## Gaya baru: "Porcelain & Olive" (belum pernah digunakan)
- **Font baru:** Instrument Serif (tajuk, serif editorial moden) + **Outfit** (caption tebal 64 px, sangat jelas). **Palet:** putih tulang, batu, olive, tanah liat (clay), arang.
- **Caption baru:** jalur kaca kabur (frosted) di belakang teks; kata kunci bertukar warna clay dengan garis bawah yang menyapu masuk ikut suara.
- **Teknik baru:** huruf naik satu-satu dengan kabur→tajam; kad **kaca kabur**; **susunan polaroid** yang mengembang; bingkai & pendedahan **pepenjuru**; peralihan **sapuan clay** condong; **nombor odometer** bergolek (1→5, 01–05); garis/bulatan **tulisan tangan** dilukis; **dua lajur B-roll bergerak berlawanan**; **medalion kaca** bulat; **zoom-through** ke dalam laut; bar **segmen gaya IG Stories** di atas.

## Apa yang dibuang
| Masa asal | Dibuang | Sebab |
|---|---|---|
| 0.0–0.8 | senyap | permulaan |
| 6.7–8.3, 11.1–12.4, 15.7–16.6, 20.2–21.3, 24.2–25.5, 28.8–29.9, 34.7–35.9, 42.4–43.2, 46.2–46.8, 50.0–51.1 | jeda | awkward pause |
| 24.0–24.2 "okey?" | dibuang | filler |
| 2 jeda pendek | dirapatkan | pace |

## Storyboard (masa selepas edit)
| Masa | Suara | Visual |
|---|---|---|
| 0.00–0.64 | Wanita, | **Muka klien (0.64 s)** + "Wanita," huruf demi huruf |
| 0.64–3.48 | kalau nak rasa lebih yakin dengan diri sendiri | Wanita bertudung tersenyum + kad kaca: "yakin" + garis tangan |
| 3.48–5.98 | cuba buat 5 perkara ni | Odometer 1→5 + 5 polaroid mengembang |
| 5.98–8.92 | 01 jaga kebersihan diri setiap hari | Basuh tangan (pepenjuru) + polaroid sabun + bulatan tangan |
| 8.92–12.28 | 02 pilih pakaian buat korang rasa selesa | Dua lajur (kain satin / almari) bergerak berlawanan + kad kaca |
| 12.28–15.90 | 03 jaga penampilan walau duduk dekat rumah | Wanita bertudung kemas (pepenjuru) + pelekat "walau di rumah" |
| 15.90–18.56 | 04 luangkan masa untuk diri sendiri | Bunga ditiup angin + medalion kaca |
| 18.56–21.86 | 05 jangan pernah abaikan rutin mandi | Titisan air (pepenjuru) + garis bawah "mandi" |
| 21.86–25.02 | Mandi membantu membersihkan badan | Buih air + kapsul kaca "bersih" |
| 25.02–26.56 | dan membuat korang lebih segar | Ombak memercik + "segar." |
| 26.56–33.28 | Tahukah korang, garam laut mengandungi mineral semula jadi… produk penjagaan diri | Pelekat "Tahukah korang?" + kristal garam di tepi laut + "mineral / semula jadi" + chip |
| 33.28–34.10 | Sebab tu, | Zoom-through ke dalam laut |
| 34.10–39.38 | Frescura Body menggabungkan sea salt dengan wangian inspirasi perfume | Polaroid produk jatuh masuk + "Frescura Body" + SEA SALT + WANGIAN ALA PERFUME |
| 39.38–45.39 | Kita ada pilihan Bombshell dan Midnight Fantasy… rutin mandi lebih istimewa | 2 polaroid kad wangian + "rutin mandi lebih istimewa" + garis tangan |
| 45.39–46.89 | (penutup) | Frescura Body, Woman Glory · Noche |

## Nota
- Fakta "garam laut mengandungi mineral semula jadi dan sering digunakan dalam produk penjagaan diri" adalah kenyataan umum (bukan dakwaan kesihatan) dan dikekalkan seperti diucapkan.
- Caption: "Gempak" → *Keempat*, "Fresh Coral Body" → *Frescura Body*, "menggambungkan" → *menggabungkan*, "menginspirasi" → *inspirasi*.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License): 45655, 33096, 2804, 40229, 35798, 45756, 1187, 106, 44766, 9294, 22402, 2091. Wanita bertudung sahaja.
- Fon: Instrument Serif, Outfit (SIL Open Font License, google/fonts).
- SFX & muzik: disintesis sendiri (`make_audio.py`). Komposisi: HyperFrames v0.9.10.

## Cara build semula
```bash
cd video7
python3 -I ../scripts/edit_audio.py src/main.mov sh.rnnn audio cuts.json
./voice_studio.sh
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words.json && cp audio/words.json project/assets/audio/
python3 -I prep_broll.py mixkit project/assets/broll src/main.mov
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
