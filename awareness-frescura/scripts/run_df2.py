import sys, types
ta=types.ModuleType("torchaudio"); fn=types.ModuleType("torchaudio.functional"); fn.resample=lambda *a,**k: (_ for _ in ()).throw(RuntimeError("no resample"))
ta.functional=fn; sys.modules["torchaudio"]=ta; sys.modules["torchaudio.functional"]=fn
exec(open(sys.argv.pop(1)).read())
