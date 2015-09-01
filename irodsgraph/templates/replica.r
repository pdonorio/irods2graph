
Replication {
    *source = "/cinecaDMPZone/home/pdonorio/023d6d3cf78907fa4776ca09ed4fa4a7cb301975.txt";
    *destination = "/cinecaDMPZone/home/pdonorio/replica/test";
    *registered = bool("true");
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

