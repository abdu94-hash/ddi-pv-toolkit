# Redraws every figure in the book: runs fm.py and each chNN.py in turn; PNGs go to out/
import glob, os, runpy, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
for script in [os.path.join(here, 'fm.py')] + sorted(glob.glob(os.path.join(here, 'ch[0-9][0-9].py'))):
    runpy.run_path(script, run_name='__main__')
    print('drew', os.path.basename(script))
print('figures:', len(glob.glob(os.path.join(here, 'out', '*.png'))))
