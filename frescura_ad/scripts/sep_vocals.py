# Vocal separation with HTDemucs built from config + safetensors weights (no pickle loading).
# usage: python sep_vocals.py CONFIG.json WEIGHTS.safetensors in.wav out.wav [in2 out2 ...]
import sys, json, torch, numpy as np, soundfile as sf
from safetensors.torch import load_file
from demucs.htdemucs import HTDemucs
from demucs.apply import apply_model

cfg = json.load(open(sys.argv[1]))["kwargs"]
model = HTDemucs(**cfg)
sd = {k[len("state."):] if k.startswith("state.") else k: v for k, v in load_file(sys.argv[2]).items()}
missing, unexpected = model.load_state_dict(sd, strict=False)
print("missing", missing, "unexpected", unexpected)
model.eval()
vi = cfg["sources"].index("vocals")
torch.set_num_threads(4)
for src, dst in zip(sys.argv[3::2], sys.argv[4::2]):
    a, sr = sf.read(src, dtype="float32", always_2d=True)
    assert sr == cfg["samplerate"], sr
    if a.shape[1] == 1: a = np.repeat(a, 2, 1)
    wav = torch.from_numpy(a.T.copy())
    ref = wav.mean(0); m, s = ref.mean(), ref.std()
    x = (wav - m) / s
    with torch.no_grad():
        out = apply_model(model, x[None], shifts=1, split=True, overlap=0.25, progress=False)[0]
    voc = out[vi] * s + m
    sf.write(dst, voc.T.numpy(), sr, subtype="FLOAT")
    print("wrote", dst)
