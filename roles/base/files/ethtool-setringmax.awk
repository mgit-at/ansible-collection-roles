#!/usr/bin/gawk -f

BEGIN {
  section="none"
  ifname=""
  max["rx"] = 0
  max["tx"] = 0
  current["rx"] = 0
  current["tx"] = 0
}
tolower($0) ~ /parameters for/ {
  sub(/:/, "", $NF)
  ifname=$NF
  FS=":[[:space:]]+"
}
tolower($0) ~ /pre-set maximums/ {
  section="max"
}
tolower($0) ~ /current hardware settings/ {
  section="current"
}
tolower($1) ~ /^(tx|rx)$/ {
  if(section == "max") {
    max[tolower($1)]=$2
  } else if(section == "current") {
    current[tolower($1)]=$2
  }
}
END {
  print("interface: "ifname)
  print("  max:     tx "max["tx"]" rx "max["rx"])
  print("  current: tx "current["tx"]" rx "current["rx"])

  cmd=""
  if(max["tx"] != current["tx"]) {
     cmd=" tx "max["tx"]
  }
  if(max["rx"] != current["rx"]) {
    cmd=cmd" rx "max["rx"]
  }
  if(cmd != "") {
    exec="ethtool -G "ifname" "cmd
    print("executing: "exec)
    ret=system(exec)
    if(ret > 512){
      print("ethtool was killed by signal: "(ret-512)" (core dumped)")
    } else if(ret > 256) {
      print("ethtool was killed by signal: "(ret-256))
    } else {
      print("ethtool exited with status: "ret)
    }
  } else {
    print("current values are already set to the maximum - nothing to do here")
  }
}
