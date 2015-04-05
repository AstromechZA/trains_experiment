
import os
import re
import json
import time
from bs4 import BeautifulSoup
from collections import Counter

from constants import data_dir


def read_content(p):
    with open(p, 'r') as f:
        return re.sub(r'&nbsp;', '', f.read())


def identify_mode_width(lens):
    data = Counter(lens)
    return list(*data.most_common(1))[0]


def filter_matches(rows, mode_width):
    return filter(lambda r: len(r) == mode_width, rows)


def find_trainnum_column(first_row):
    i = 0
    for r in first_row:
        if r.upper().strip() == 'TRAIN NO.':
            return i
        i += 1
    raise RuntimeError("Couldn't find train number.")


def form_station_maps(first_column, nc):
    relrows = list([''] * (nc+1)) + list(first_column[nc+1:])

    m = {}
    i = 0
    for r in relrows:
        if len(r.strip()) > 0:
            m[i] = r.strip().upper()
        i += 1

    return m


def is_train_column(column):
    time_rows = 0
    for row in column:
        if re.match(r'\d\d:\d\d', row.strip()) is not None:
            time_rows += 1
    return time_rows > 2


def get_time(cell):
    cell = cell.lower().strip()
    if re.match(r'\d\d:\d\d', cell) is not None:
        return cell
    return None


def dostuff(content):
    output = []

    soup = BeautifulSoup(content)
    rows = [list(r.select('td')) for r in soup.select('tbody tr')]
    mode_width = identify_mode_width([len(r) for r in rows])

    rows = filter_matches(rows, mode_width)
    text_rows = [[r.text for r in col] for col in rows]
    transposed_rows = zip(*text_rows)

    trainnum_col = find_trainnum_column(transposed_rows[0])

    station_map = form_station_maps(transposed_rows[0], trainnum_col)

    for column in transposed_rows:
        if is_train_column(column):
            train_number = column[trainnum_col]
            stops = []

            for k, v in station_map.iteritems():
                t = get_time(column[k])
                if t is not None:
                    stops += [[v, t]]

            output.append({
                'train_number': train_number,
                'stops': stops
            })

    return output


def collect_htmls(d):
    return map(lambda f: os.path.join(d, f), filter(lambda f: f.endswith('.htm.stripped'), os.listdir(d)))


def main():
    all_data = {'weekdays': [], 'saturdays': [], 'sundays': []}

    for f in collect_htmls(data_dir):
        content = read_content(f)
        trains = dostuff(content)

        fn = os.path.basename(f).lower()
        if '_monfri_' in fn:
            all_data['weekdays'] += trains
        elif '_sat_' in fn:
            all_data['saturdays'] += trains
        elif '_sun_' in fn:
            all_data['sundays'] += trains
        else:
            raise RuntimeError('Could not extract weekday from filename ' + fn)

    with open(os.path.join(data_dir, 'train_times.json'.format()), 'w') as f:
        f.write(json.dumps(all_data))

if __name__ == "__main__":
    main()