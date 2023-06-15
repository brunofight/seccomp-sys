import json
# Analysis Script, which syscalls are blocked by the default docker seccomp by standards of current Linux Kernel

# The blocked syscalls according to https://docs.docker.com/engine/security/seccomp/

f_default_docker = open('../profiles/default_x86.json')

docker_seccomp = json.load(f_default_docker)["syscalls"][0]["names"]

# the actually blocked syscalls going by the blacklist retrieved from difference to Linux Kernel 6.4.0-rc1
f_all_syscalls_6_4 = open('../profiles/all_syscalls_6_4.json')
all_syscalls = json.load(f_all_syscalls_6_4)["syscalls"][0]["names"]

blacklist_docker_seccomp = []

for syscall in all_syscalls:

    add_to_blacklist = True
    for s in docker_seccomp:
        if s == syscall:
            add_to_blacklist = False
            break

    if add_to_blacklist:
        blacklist_docker_seccomp.append(syscall)

print(blacklist_docker_seccomp)