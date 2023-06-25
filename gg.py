import subprocess
cmd = "bash -c \"echo -e 'GEJMRDKY\\nGEJMRDKY' | passwd root\""
subprocess.check_call(cmd, shell=True)
