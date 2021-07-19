#!/bin/sh
# This script will fetch WireGuard configuration from WgMeshAPI.

API_KEY=''
API_URL=''
BASENAME=$(basename $0)
WORKDIR="/etc/wireguard"
WG_INTERFACE="wg0"
WG_CONFIG="$WORKDIR/$WG_INTERFACE.conf"
LOG_FILE="$BASENAME.log"
FETCHED_CONFIG=''

main() {
  create_backup
  fetch_config; sed -i "s|PLACEHOLDER|$WG_PRIVATE_KEY|" "$WG_CONFIG" || return $?
  restart_wireguard
  return $?
}

create_backup() {
  : > "$WG_CONFIG.bak"; mv "$WG_CONFIG" "$WG_CONFIG.bak"
  : > "$WG_CONFIG"
}

fetch_config() {
  curl -X GET -H "x-access-token: $API_KEY" "$API_URL" > "$WG_CONFIG"
  exit_code=$?
  [ "$exit_code" -eq "0" ] || log_error "curl exited with $exit_code" "fetching config failed"
  return "$exit_code"
}

restart_wireguard() {
  wg-quick down "$WG_INTERFACE"; wg-quick up "$WG_INTERFACE"
}

log_error() {
  printf "[$(date +%s)] [$1]\n" >> "$LOG_FILE"
  print_error "$2"
}

print_error() {
  >&2 printf "$BASENAME: $1\n"
  [ -z "$2" ] || exit "$2"
}

if [ -s $WORKDIR/privatekey ]
then
  WG_PRIVATE_KEY=$(cat "$WORKDIR/privatekey")
else
  print_error "$WORKDIR/privatekey does not exist or is empty" 1
fi
[ -s $WG_CONFIG ] || : > $WG_CONFIG

which wg-quick 1>/dev/null || print_error "wg-quick is not installed" 1

which curl 1>/dev/null || print_error "curl is not installed" 1

main $@
exit $?
