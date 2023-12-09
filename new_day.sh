#!/usr/bin/sh

# create directory structure with template code for a new
# day of AoC

year=${2:-$(date +%Y)}

if [ ! -d ${year} ]
then
    mkdir ${year}
fi

last_day=$(ls ${year} | tail -n 1)
last_day=${last_day:-day_00}
last_day_num=$((10#${last_day: -2}))
new_day_num=$((${last_day_num}+1))
new_day_num=${1:-${new_day_num}}
printf -v new_day_num "%02d" ${new_day_num}

mkdir ${year}/day_${new_day_num}

cat <<EOP > ${year}/day_${new_day_num}/answer.py
#!/usr/bin/env python

def p1(data, is_sample):
    if not is_sample:
        return 'N/A'
    return 'N/A'


def p2(data, is_sample):
    if not is_sample:
        return 'N/A'
    return 'N/A'
EOP

echo "Added template answer to ${year}/day_${new_day_num}"
