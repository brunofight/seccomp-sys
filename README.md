# seccomp-sys

## Components

### Syscall Extractor

The Syscall Extractor will produce a markup or textfile containing all System Calls utilized by a container over an unspecified period of time. Together with the **Workload Simulation** this will approximate the Set of used System Calls.

This can be achieved either using the strace-utility or a dummy Seccomp Profile, setting all syscalls to ``SCMP_ACT_LOG``.

### Workload Simulation

Using the most prelavent Docker images as a basis for analysis, the workload simulation will execute ususal operations on the image utilized, e.g. on a database:

- logging in
- modifying configurations
- creating, modifying and deleting tables or databases

This will roughly reproduce what should be expected of the image in a production environment. Thereby it should be noted that this procedure resembles the definition of tests which will unlikely cover all scenarios of application usage.

### Profile Generator

The Profile Generator uses the List of System Calls extracted by the **Syscall Extractor** to identify the subgroups of syscalls according to the *System Call Systematization*. This will create a more permissive profile to avoid issues produced due to a lack of test coverage.

If critical Systemcalls are permitted through this procedure, they will be raised to an ``SCMP_ACT_LOG`` status for notification to a SIEM.

For quick lookup the generator uses two lists: 

- one containing each Systemcall as a search key and its corresponding group as value
- one containing each group as indexing attribute containing a list of key-value pairs of Syscall and their attributes (severity, deprecation status)


