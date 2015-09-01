PID_DO_reg {
  *iCATCache = bool("true");
  EUDATCreatePID(*parent_pid, *source, *ror, *iCATCache, *newPID);
  writeLine("stdout","PID: *newPID");
}
INPUT *source="/cinecaDMPZone/home/pdonorio/023d6d3cf78907fa4776ca09ed4fa4a7cb301975.txt",*parent_pid="None",*ror="None"
OUTPUT ruleExecOut
