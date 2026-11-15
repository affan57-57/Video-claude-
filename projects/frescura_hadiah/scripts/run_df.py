import sys, types
m=types.ModuleType("torchaudio.backend"); c=types.ModuleType("torchaudio.backend.common")
class AudioMetaData: pass
c.AudioMetaData=AudioMetaData; m.common=c
sys.modules["torchaudio.backend"]=m; sys.modules["torchaudio.backend.common"]=c
import torch, soundfile as sf, os
from df.enhance import enhance, init_df
model, st, _ = init_df(model_base_dir="models/DF3", log_level="WARNING")
a,sr=sf.read(sys.argv[1], dtype="float32"); assert sr==st.sr(), sr
att=float(os.environ.get("ATT","0")) or None
enh=enhance(model, st, torch.from_numpy(a)[None], atten_lim_db=att)
sf.write(sys.argv[2], enh[0].numpy(), sr, subtype="FLOAT"); print("ok")
