terminal_id="$(tty)"
tty_number=$(basename "$terminal_id")
root_directory=~/.oslui
log_directory="$root_directory/command_log"
log_file="$log_directory/$tty_number.log"
last_recorded_command=""

# Make sure the path and file exists
if [ ! -d "$root_directory" ]; then
  mkdir -p "$root_directory"
fi

if [ ! -d "$log_directory" ]; then
  mkdir -p "$log_directory"
fi

if [ ! -f "$log_file" ]; then
  touch "$log_file"
fi

record_command() {
  # Get the last command in history
  local last_command
  if [ "${ZSH_VERSION}" ]; then
    last_command=$(history -1 | sed -e "s/^[ ]*[0-9]*[ ]*//")
  elif [ "${BASH_VERSION}" ]; then
    last_command=$(history 1 | sed -e "s/^[ ]*[0-9]*[ ]*//" | sed -E "s/^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} //")
  fi

  # Log if the new command is different from the last logged command
  if [ "$last_command" != "$last_recorded_command" ]; then
    # Append records to log file
    echo "$last_command" >> "$log_file"
    last_recorded_command="$last_command"
  fi
}

[ "${BASH_VERSION}" ] && PROMPT_COMMAND="record_command"
[ "${ZSH_VERSION}" ] && precmd() { record_command; }

# When the terminal session ends, cancel the DEBUG trap
cleanup() {
  rm -f "$log_file"
  trap - DEBUG
}

# Register a cleanup function when the terminal is closed
trap 'cleanup' EXIT
