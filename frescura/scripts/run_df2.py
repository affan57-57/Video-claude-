import sys, types
ta=types.ModuleType("torchaudio"); ta.__path__=[]; tf=types.ModuleType("torchaudio.functional"); ta.functional=tf; tf.resample=lambda *a,**k: None; sys.modules["torchaudio"]=ta; sys.modules["torchaudio.functional"]=tf
m=types.ModuleType("torchaudio.backend"); c=types.ModuleType("torchaudio.backend.common")
class AudioMetaData: pass
c.AudioMetaData=AudioMetaData; m.common=c
sys.modules["torchaudio.backend"]=m; sys.modules["torchaudio.backend.common"]=c
import torch, soundfile as sf
from df.enhance import enhance, init_df
model, st, _ = init_df(model_base_dir=sys.argv.pop(1), log_level="WARNING")
for src,dst in zip(sys.argv[1::2], sys.argv[2::2]):
    a,sr=sf.read(src, dtype="float32"); assert sr==st.sr(), sr
    enh=enhance(model, st, torch.from_numpy(a)[None], atten_lim_db=float(__import__("os").environ.get("ATT","0")) or None)
    sf.write(dst, enh[0].numpy(), sr, subtype="FLOAT")
    print("wrote", dst)
