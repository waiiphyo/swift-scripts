#!/bin/bash
#by wai.phyo6
container="sbsbackup-01"
nameprefix="$1"
dateprefix="$2-"
start_day=1
end_day=31

red_bold='\033[1;31m'
reset_color='\033[0m'

if [[ -z $nameprefix || -z $dateprefix || -z $start_day || -z $end_day ]]; then
  echo -e "${red_bold}Usage: ./swift_size_check.sh <nameprefix> <dateprefix>${reset_color}"
  echo -e "${red_bold}Usage: ./swift_size_chek.sh <Name> <year>${reset_color}"
  exit 1
fi

total_size=0
start_month=07
end_month=12

for ((month=start_month; month<=end_month; month++));do
  month_formatted=$(printf "%02d" "$month")
  for ((day=start_day; day<=end_day; day++)); do
    day_formatted=$(printf "%02d" "$day")
    object="${nameprefix}/${dateprefix}${month_formatted}-${day_formatted}"
    echo -e "${red_bold}Checking object $object from $container${reset_color}"
    #echo "$object"
  
    # Retrieve the list of objects
    objects_list=$(swift list --prefix "$object" "$container")
  
    # Loop through each object to get its size
    while IFS= read -r obj; do
      obj_size=$(swift stat "$container" "$obj" | awk '/Content Length:/ {print $3}')
      if [ "$obj_size" -gt 0 ]; then
        echo "$obj : $obj_size bytes"
        total_size=$((total_size + obj_size))
      fi
    done <<< "$objects_list"
  done
done

total_size_gb=$(awk "BEGIN {printf \"%.2f\", $total_size / (1024 * 1024 * 1024)}")

echo -e "${red_bold}Total size of objects: $total_size_gb GB${reset_color}"

