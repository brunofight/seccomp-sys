import subprocess
from lib.helper_functions import *

image = "nginx:latest"
profile = "./profiles/all_log.json"

# start tail subprocess for extracting syscalls logged through seccomp
grep_string = "audit: type=1326"

p_tail = subprocess.Popen(["sudo", "tail", "-f", "/var/log/syslog"], stdout=subprocess.PIPE, text=True)
p_grep = subprocess.Popen(["grep", grep_string], stdin=p_tail.stdout, stdout=subprocess.PIPE, text=True)

p_docker = subprocess.Popen(["sudo", "docker", "run", "--rm", "--security-opt", "seccomp=" + profile,
                             "-p", "127.0.0.1:8000:80/tcp", image], stdout=subprocess.PIPE, text=True)

while True:
    output = p_docker.stdout.readline()
    print(output.strip())
    exit_flag = input()

    # print image startup sequence to the point where tests can be run
    if exit_flag == "x":
        break

# insert tests here


# gracefully terminate docker to stop running image
p_docker.terminate()
output = p_docker.communicate()

# terminate tail and grep to flush the pipes to output
p_tail.terminate()
p_tail.communicate()
p_grep.terminate()

output, err = p_grep.communicate()
syscalls = parse_syscalls(output)

for syscall in syscalls:
    print(syscall)

