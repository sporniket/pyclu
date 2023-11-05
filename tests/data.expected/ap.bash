#!/usr/bin/env bash

ap_help() {
  cli_name=${0##*/}
  echo -e "
\e[90m${cli_name}\e[0m
\e[90m---===<{\e[93map\e[96m, Assemble Project, by Sporniket -- version 0.0.0-SNAPSHOT\e[90m}>===---\e[0m

\e[96mUsage:\e[0m ${cli_name} \e[93m[command]\e[0m
\e[96mCommands:\e[0m
  \e[93m*\e[0m         Help
"
  exit 1
}

case "$1" in
  *)
    ap_help
    ;;
esac
