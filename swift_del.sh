#!/bin/bash
#by wai.phyo6
container="sbsbackup-01"
nameprefix="$1"
dateprefix="$2-"
start_day="$3"
end_day="$4"

red_bold='\033[1;31m'
reset_color='\033[0m'

if [[ -z $nameprefix || -z $dateprefix || -z $start_day || -z $end_day ]]; then
  echo -e "${red_bold}Usage: ./swift_list.sh <nameprefix> <dateprefix> <start_day> <end_day>${reset_color}"
  echo -e "${red_bold}Usage: ./swift_list.sh <Name> <year-month> <1-31> <1-31>${reset_color}"
  exit 1
fi


for ((day=start_day; day<=end_day; day++)); do
  day_formatted=$(printf "%02d" "$day")
  object="${nameprefix}/${dateprefix}${day_formatted}"
  
  #echo $day_formatted
  #echo $object
  echo -e "${red_bold}Deleting $object from $container${reset_color}"
  swift delete --prefix "$object" "$container"

done

