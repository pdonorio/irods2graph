
IntCheck_DO {
    *source = "/cinecaDMPZone/home/pdonorio/023d6d3cf78907fa4776ca09ed4fa4a7cb301975.txt"
    *destination = "/cinecaDMPZone/home/pdonorio/replica/test";
    *logEnabled = bool("true");
    *status_check = EUDATCheckIntegrityDO(*source,*destination,*logEnabled,*response);
    if (*status_check) {
        writeLine("stdout", "Successful check!");
    }
    else {
        writeLine("stdout", "Failed check: *response");
    }
}
OUTPUT ruleExecOut

