import json

# blocked according to https://docs.docker.com/engine/security/seccomp/
docker_online_blocked = ["acct",
"add_key",
"bpf",
"clock_adjtime",
"clock_settime",
"clone",
"create_module",
"delete_module",
"get_mempolicy",
"init_module",
"ioperm",
"iopl",
"kcmp",
"kexec_file_load",
"kexec_load",
"keyctl",
"lookup_dcookie",
"mbind",
"mount",
"move_pages",
"name_to_handle_at",
"nfsservctl",
"open_by_handle_at",
"perf_event_open",
"personality",
"pivot_root",
"process_vm_readv",
"process_vm_writev",
"ptrace",
"query_module",
"quotactl",
"reboot",
"request_key",
"set_mempolicy",
"setns",
"settimeofday",
"stime",
"swapon",
"swapoff",
"sysfs",
"_sysctl",
"umount",
"umount2",
"unshare",
"uselib",
"userfaultfd",
"ustat",
"vm86",
"vm86old"]

docker_actual_blocked = json.load(open("../profiles/default_x86_blacklist.json"))["syscalls"][0]["names"]

old_syscalls = []
new_syscalls = []

for syscall in docker_online_blocked:

    exists_in_both = False

    for s in docker_actual_blocked:
        if s == syscall:
            exists_in_both = True
            break

    if not exists_in_both:
        old_syscalls.append(syscall)

print(old_syscalls)

for syscall in docker_actual_blocked:

    exists_in_both = False

    for s in docker_online_blocked:
        if s == syscall:
            exists_in_both = True
            break

    if not exists_in_both:
        new_syscalls.append(syscall)

print(new_syscalls)
