import os


def get_syscall_dict():
    syscall_dict = {}

    # retrieve syscall indices from glibc of running kernel
    # see https://unix.stackexchange.com/questions/445507/syscall-number-%E2%86%92-name-mapping-at-runtime
    command = 'awk \'BEGIN { print "#include <sys/syscall.h>" } /p_syscall_meta/ { syscall = substr($NF, 19); ' \
              'printf "SYS_%s=%s\\n", syscall, syscall }\' /proc/kallsyms ' \
              '| sort -u | gcc -E -P - | less'
    output = os.popen(command).read()

    lines = output.split("\n")
    for line in lines:
        if line == "":
            break
        index = line.split("=")[0]
        value = line.split("=")[1]
        if index.isnumeric():
            syscall_dict[int(index)] = value

    return syscall_dict


def parse_syscalls(syslog_input):
    lines = syslog_input.split("\n")
    syscalls = []

    for line in lines:
        if line == "":
            break
        num = line.split("syscall=")[1].split(" ")[0]
        syscalls.append(int(num))

    syscalls.sort()


    syscall_dict = get_syscall_dict()

    # strip duplicates
    unique_syscalls = []
    prev_num = -1
    for i in range(len(syscalls)):
        if syscalls[i] != prev_num:
            unique_syscalls.append(syscall_dict[syscalls[i]])
            prev_num = syscalls[i]
            continue

    return unique_syscalls