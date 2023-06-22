import json


def get_group_statistics(result):

    file_syscalls = open('../resources/syscalls_with_groups.json', 'r')
    syscalls_with_groups = json.load(file_syscalls)

    file_groups = open('../resources/groups_with_syscalls.json', 'r')
    groups_with_syscalls = json.load(file_groups)

    extended_blacklist = json.load(open('../profiles/default_x86_extended_blacklist.json'))["syscalls"]
    extended_blacklist_block = extended_blacklist[0]["names"]
    extended_blacklist_log = extended_blacklist[1]["names"]

    blacklist_block_hits = []
    blacklist_log_hits = []

    stats = {}
    stats_syscalls_not_in_groups = 0

    for syscall in result:
        # get syscalls blocked / logged according to blacklist
        if syscall in extended_blacklist_block:
            blacklist_block_hits.append(syscall)

        if syscall in extended_blacklist_log:
            blacklist_log_hits.append(syscall)

        group_name = syscalls_with_groups[syscall]
        # get groups from systemization used
        if group_name in stats:
            stats[group_name] += int(result[syscall])
        else:
            stats[group_name] = int(result[syscall])

            # remove group from groups_with syscalls to count how many syscalls would later be blocked
            if group_name in groups_with_syscalls:
                del groups_with_syscalls[group_name]

    for group in groups_with_syscalls:
        stats_syscalls_not_in_groups += len(groups_with_syscalls[group])

    print("Extended Blacklist Block Hits: " + str(len(blacklist_block_hits)))
    print(blacklist_block_hits)
    print("-------------------")
    print("Extended Blacklist Log Hits: " + str(len(blacklist_log_hits)))
    print(blacklist_log_hits)
    print("-------------------")
    print("Mined Syscalls: " + str(len(result)))
    print("Mined Groups: " + str(len(stats)) + " / 97")
    additional_syscalls = 357 - stats_syscalls_not_in_groups - len(result)
    print("Additional Syscalls through mined groups: " + str(additional_syscalls))
    print("Syscalls in unused groups: " + str(stats_syscalls_not_in_groups) + " / 357")
    print(stats)
    print("-------------------")

file_result = open('../results/webServing_db.json', 'r')
result = json.load(file_result)

get_group_statistics(result)






