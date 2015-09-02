
PID_DO_reg {
  *iCATCache = bool("true");
  EUDATCreatePID(*parent_pid, *source, *ror, *iCATCache, *newPID);
  writeLine("stdout","PID: *newPID");
}
INPUT *source={{ irods_file }},*parent_pid="None",*ror="None"
OUTPUT ruleExecOut
