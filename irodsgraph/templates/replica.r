
Replication {
    *source = {{ dataobj_source }};
    *destination = {{ dataobj_dest }};
    *registered = bool({{ pid_register }});
    *recursive = bool("true");
    *status = EUDATReplication(*source, *destination, *registered, *recursive, *response);
    if (*status) {
        writeLine("stdout", "Success!");
    }
    else {
        writeLine("stdout", "Failed: *response");
    }
}
OUTPUT ruleExecOut

