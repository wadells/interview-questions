# Given an apache log file with lines like the following:
#
# 10.7.181.167 - - [28/Feb/2016:03:51:06 -0800] "GET /queue_info_json/ HTTP/1.1" 200 60 "https://build.west.isilon.com/BR_7_1_1/page3" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0"
# 10.7.166.36 - - [06/Mar/2016:03:29:02 -0800] "GET /register/vmvirtbuild01.west.isilon.com/build-journaled/seattle/ HTTP/1.1" 200 99 "-" "Python-urllib/2.6"
#
# In a language of your choice, write a program that finds all the
# paths that return response code 500, counts them, and displays a list
# sorted by count. For example the ouput should look like:
#
#     314 /launcher/api/1/jobs/
#      83 /queue_info_json/
#      10 /register/qavm-rw21/test/santaclara/
#
# (spacing/padding is unimportant, but each line should include the
# endpoint and the number of times it returned response code 500 in
# the logs).
#
# A compressed ~750M apache log to test on can be found in this directory
# in the file apache.log.gz.

from collections import namedtuple
import gzip
import sys
from typing import IO, Iterable


Clf = namedtuple("clf", ["ip", "timestamp", "method", "path", "protocol", "response", "bytes"])


def parse(line: str) -> Clf:
    section = line.split('"')

    part = section[0].split()
    ip = part[0]
    timestamp = part[3] + " " + part[4]  # TODO: convert to datetime

    part = section[1].split()
    method = part[0]
    path = part[1]
    protocol = part[2]

    part = section[2].split()
    response = int(part[0])
    if part[1] == "-":
        bytes = 0
    else:
        bytes = int(part[1])

    return Clf(ip=ip, timestamp=timestamp, method=method, path=path, protocol=protocol, response=response, bytes=bytes)


def convert(f: IO) -> Iterable[Clf]:
    for line in f:
        yield parse(line)


def head(f: Iterable, n: int = 10) -> Iterable:
    i = 0
    for line in f:
        yield line
        i += 1
        if i >= n:
            break


def rc_filter(f: Iterable[Clf], rc: int) -> Iterable[Clf]:
    for line in f:
        if line.response == rc:
            yield line


def aggregate(f: Iterable[Clf]) -> dict[str, int]:
    count = {}
    for line in f:
        count[line.path] = count.get(line.path, 0) + 1
    return count


if __name__ == "__main__":
    target = sys.argv[1]
    with gzip.open(target, 'rt') as f:
        data = rc_filter(convert(f), 500)
        counts = aggregate(data)
        output = ["{} {}".format(v, k) for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    print("\n".join(output))
