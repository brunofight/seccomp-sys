import json

file_syscalls = open('../resources/syscalls_with_groups.json', 'r')
syscalls_with_groups = json.load(file_syscalls)

file_groups = open('../resources/groups_with_syscalls.json', 'r')
groups_with_syscalls = json.load(file_groups)


def get_group(syscall):
    return syscalls_with_groups[syscall]


def get_groups(syscalls):
    groups = []
    for syscall in syscalls:
        group_name = get_group(syscall)
        if not (group_name in groups):
            groups.append(group_name)
    return groups


def get_group_statistics(result):
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

        group_name = get_group(syscall)
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
    print("Traced Syscalls: " + str(len(result)))
    print("Mined Groups: " + str(len(stats)) + " / 97")
    additional_syscalls = 357 - stats_syscalls_not_in_groups - len(result)
    print("Additional Syscalls through mined groups: " + str(additional_syscalls))
    print("Mined Syscalls: " + str(additional_syscalls + len(result)))
    print("Syscalls in unused groups: " + str(stats_syscalls_not_in_groups) + " / 357")
    print("Percent blocked: " + str(stats_syscalls_not_in_groups / 357 * 100) + "%")
    print(stats)
    print("-------------------")


def compare(l1, l2):
    difference = []
    for entity in l1:
        if not (entity in l2):
            difference.append(entity)
    return difference


def extrapolated_syscalls(syscalls_1, groups_2):
    # taking syscalls from one capture and groups from other capture as input -> get syscalls extrapolated through groups
    for syscall in syscalls_1:
        group_name = get_group(syscall)
        if group_name in groups_2:
            print(syscall + " extrapolated through " + group_name)


def compare_captures(cap1, cap2):
    dif_1_2 = compare(cap1, cap2)
    dif_2_1 = compare(cap2, cap1)

    print("Syscalls in Capture 1, not in 2")
    print(dif_1_2)

    print("Syscalls in Capture 2, not in 1")
    print(dif_2_1)

    print("-------------------")
    groups_cap1 = get_groups(cap1)
    groups_cap2 = get_groups(cap2)

    groups_dif_1_2 = compare(groups_cap1, groups_cap2)
    groups_dif_2_1 = compare(groups_cap2, groups_cap1)

    print("Groups in Capture 1, not in 2")
    print(groups_dif_1_2)
    print("Groups in Capture 2, not in 1")
    print(groups_dif_2_1)
    print("-------------------- Capture 2 enriched by:")

    extrapolated_syscalls(dif_1_2, groups_cap2)

    print("-------------------- Capture 1 enriched by:")

    extrapolated_syscalls(dif_2_1, groups_cap1)

'''
file_result = open('../results/cloudsuite/webServing_memcache.json', 'r')
get_group_statistics(json.load(file_result))
'''

capture1 = json.load(open('../results/ycsb/mongo_a.json', 'r'))
capture2 = json.load(open('../results/ycsb/mongo_b.json', 'r'))

compare_captures(capture1, capture2)
