import sys
import csv

from collections import defaultdict
from heapq import *

import io


def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))

    q, seen = [(0, f, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2, path))

    return float("inf"), []


def flatten(container):
    for i in container:
        if isinstance(i, (list, tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


if __name__ == '__main__':
    edges = []
    verkey = []
    with open('e.csv', 'r') as data_file:
        reader1 = csv.reader(data_file, delimiter=',')
        for i in reader1:
            edges.append([i[0], i[1], float(i[2])])
    with open('vkey.csv', 'r') as data_file1:
        reader2 = csv.reader(data_file1, delimiter=',')
        for i in reader2:
            verkey.append(int(i[0]))
    with io.open('result_pl3.csv', 'wb') as csvfile:
        fieldnames = ['cost', 'path']
        writer1 = csv.writer(csvfile, delimiter=',')
        writer1.writerow([u'start', u'end', u'cost', u'path sequence'])
        for i in verkey:
            if 20000 < i <= 30000:
                for j in verkey:
                    if j > i:
                        row_lines = []
                        cost, path = dijkstra(edges, str(i), str(j))
                        row_lines.append(str(i))
                        row_lines.append(str(j))
                        flattened_path = list(flatten(path))
                        flattened_path.reverse()
                        print("i: {} j:{}".format(str(i), str(j)))
                        row_lines.append(cost)
                        for item in flattened_path:
                            row_lines.append(item)
                        writer1.writerow(row_lines)
