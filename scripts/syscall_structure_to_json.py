import json

syscalls_with_groups = {}
groups_with_syscalls = {}

file = open('../resources/Syscall_Groups_Table.csv', 'r', encoding='utf-8-sig')
lines = file.readlines()

for line in lines:
    elements = line.split(";")
    group_name = elements[0].strip()
    syscall_names = elements[1].split(",")

    groups_with_syscalls[group_name] = []

    for syscall in syscall_names:
        syscalls_with_groups[syscall.strip()] = group_name
        groups_with_syscalls[group_name].append(syscall.strip())

with open('../resources/syscalls_with_groups.json', 'w') as out:
    out.write(json.dumps(syscalls_with_groups, indent=1))

with open('../resources/groups_with_syscalls.json', 'w') as out:
    out.write(json.dumps(groups_with_syscalls, indent=1))