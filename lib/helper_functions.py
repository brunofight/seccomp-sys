
def parse_syscalls(syslog_input):
    lines = syslog_input.split("\n")

    for line in lines:
        num = line.split("syscall=")[1].split(" ")[0]
        print(num)






