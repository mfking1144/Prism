# >>>PrismStart
import nuke

if not nuke.env["studio"] and nuke.env.get("gui"):
    import os
    import sys

    Dir = os.path.join(PRISMROOT, "Scripts")
    if Dir not in sys.path:
        sys.path.append(Dir)

    import PrismCore

    pcore = PrismCore.PrismCore(app="Nuke")
# <<<PrismEnd
