#!/bin/bash
S=/tmp/claude-0/-home-user/4bd2e5dd-e98b-59cc-9aab-5a467b605418/scratchpad; P=$S/hf/frescura
python3 -c "
import sys; src=open('$S/scripts/index.src.html').read(); caps=open('$S/work/captions.json').read()
open('$P/index.html','w').write(src.replace('__CAPTIONS__',caps))"
