import os
import subprocess
FNULL = open(os.devnull, 'w')
for qf in range(1, 100, 1):
    subprocess.call("./demo -f 2.png -o ssim_{} -q {}".format(str(qf), str(qf)), shell=True,
                                stdout=FNULL, stderr=subprocess.STDOUT)
