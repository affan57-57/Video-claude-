# Video 5: "Tidur wangi semerbak" (cerita → rahsia → beg kuning)

**Status: PREVIEW**, `preview/preview_v1.mp4` (1080x1920, draft, tag PREVIEW). Final akan dirender selepas diluluskan.

- Asal: 2 klip disambung (59.0 s + 6.5 s = 65.5 s). Selepas edit: **52.2 s** (50.7 s suara + 1.5 s kad penutup).
- Gaya: minimalist luxury, rancak (ikut Video 4 v3 yang diluluskan). Animasi laju dengan zoom punch, bunyi "top" pada setiap teks dan "whip" pada setiap peralihan, kilatan pada impak. Muzik lembut 90 bpm (~−26 dB di bawah suara), SFX kuat, mix −13 LUFS.
- Muka: **0.9 s sahaja** (4.80–5.70 s, "Korang, aku…"; ikut permintaan, bawah 1 saat). Diambil dari rakaman 1.3–2.2 s di mana mata pandang tepat ke lensa (berniqab, jadi tiada isu lip-sync). Hanya 4 saat pertama rakaman yang pandang kamera; selebihnya telefon terdongak ke siling, jadi diganti sepenuhnya dengan B-roll dan motion graphics.
- Suara: lokasi rakaman bising (lantai bunyi ~−30 dBFS). Segmen disamakan level, kemudian RNNoise + FFT denoise, noise gate, EQ (kehangatan, potong "box", presence, air), de-esser, compressor ringan, exciter, dan gandaan tetap ke −14 LUFS.

## Apa yang dibuang / dipindah
| Masa asal | Tindakan | Sebab |
|---|---|---|
| 37.9–42.1 "Satu bilik tidur tu jadi wangi, terus auto macam luxury hotel" | **dipindah ke 0:00** | hook paling kuat (flash-forward) |
| 4.2–5.3 | dibuang | jeda |
| 12.6–13.3 | dibuang | jeda |
| 32.7–34.5 | dibuang | jeda 1.9 s |
| 46.4–55.0 | dibuang | ulangan "Bau dia pun memang melekat kat kulit, lepas tu rasa fresh, premium" + jeda 3.3 s |
| 64.8–65.5 "Okay" | dibuang | hujung |
| 6 jeda pendek | dirapatkan | pace |

## Storyboard (masa selepas edit)
| Masa | Suara | Visual | SFX |
|---|---|---|---|
| 0.00–2.85 | Satu bilik tidur tu jadi wangi | B-roll bilik hotel + "jadi WANGI" + kilauan | boom, shimmer |
| 2.85–4.80 | Terus auto macam luxury hotel | Koridor hotel mewah + "LUXURY hotel" emas | boom |
| 4.80–5.70 | Korang, aku… | **Muka (0.9 s)** + "KORANG," | whip |
| 5.70–6.80 | …ada satu perangai tau | Kinetic type gelap: "PERANGAI tau!" | whip, boom |
| 6.80–10.85 | Mak aku selalu bising… mengada-ngada | "SELALU BISING" + bubble "MAK: Mengada-ngada!" (taip, bergegar) + "!!" | boom, click |
| 10.85–15.60 | Sebab apa? Nak tidur, badan mesti wangi semerbak | "SEBAB APA?" + bilik tidur senja + lilin | boom, shimmer |
| 15.60–18.85 | Body yang ada standard | "BODY yang ada" + lencana STANDARD ✓ | boom, chime |
| 18.85–22.90 | Sebelum panjat katil, jenuh aku spray | Katil hotel + "PANJAT KATIL" + "SPRAY!" dengan percikan | foam |
| 22.90–26.60 | Perfume mahal-mahal kat badan, baju, bantal | Rak perfume + "MAHAL-MAHAL" + label "RM RM RM" + chip BADAN/BAJU/BANTAL | click, top |
| 26.60–30.70 | Poket menangis, membazir gila | Duit + dompet + bar "BAKI POKET" susut ke merah + "membazir gila!" | boom ×2 |
| 30.70–34.05 | Satu hari aku terjumpa satu rahsia | Latar gelap + "RAHSIA" emas + **reveal botol duo** | riser, boom, shimmer |
| 34.05–36.75 | Mandi malam sebelum tidur | Shower + bulan + "MANDI MALAM" | boom |
| 36.75–38.90 | Bau dia melekat kat kulit | **Klip pam Woman Glory berbuih, latar ivory** + "MELEKAT kat kulit" | foam, boom |
| 38.90–40.95 | Fresh, premium and expensive | Foto diagonal + chip FRESH / PREMIUM / EXPENSIVE | top ×3, chime |
| 40.95–42.90 | Tak payah membazir perfume mahal | "PERFUME MAHAL" dicoret + ✕ | whip, boom |
| 42.90–45.10 | Tidur pun ada vibes mahal | Lilin-lilin + "VIBES mahal" | boom, shimmer |
| 45.10–50.70 | Geng nak tidur wangi semerbak… tekan beg kuning sekarang, sebelum habis | Foto duo kayu + butang TEKAN BEG KUNING + bar "SEBELUM HABIS" | whip, pop, click, boom |
| 50.70–52.20 | (penutup) | FRESCURA BODY, tidur wangi semerbak + butang | chime |

## Perlu pengesahan
- Ayat CTA: whisper dengar "So **geng body** yang nak tidur wangi semerbak malam ni". Caption tunjuk "So geng body…". Kalau maksudnya lain, beritahu.

## Sumber
- B-roll: [Mixkit](https://mixkit.co) (Mixkit Free License). Klip: 4196, 34613, 3111, 6925, 4198, 21694, 18304, 18299, 21766, 4433, 48498. Klip tanpa orang (bilik, katil, lilin, shower) dipilih untuk elak aurat.
- Klip pam: dari Video 4 (`pump_ivory.mp4`, latar pantai ditukar ke ivory).
- SFX & muzik: disintesis sendiri (`make_audio.py`).
- Komposisi: HyperFrames v0.9.10 (`video5/project/`).

## Cara build semula
```bash
cd video5
ffmpeg -i src/part1.mov -i src/part2.mov -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" src/main.mp4
python3 -I ../scripts/edit_audio.py src/main.mp4 sh.rnnn audio cuts.json        # cuts.json sets quiet_db -30 (noisy location)
./voice_studio.sh
python3 -I ../scripts/transcribe.py audio/voice16k.wav audio/words.json
python3 -I prep_broll.py mixkit project/assets/broll src/main.mp4
python3 -I build.py project
python3 make_audio.py project/assets/audio/voice.wav project/assets/audio
ffmpeg -i project/assets/audio/mix_raw.wav -af loudnorm=I=-13:TP=-1:LRA=9 -ar 48000 project/assets/audio/mix.wav
cd project && npx hyperframes@0.9.10 render -q draft -o ../preview/preview_v1.mp4
```
