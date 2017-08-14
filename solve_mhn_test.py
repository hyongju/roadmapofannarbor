"""

"""

from collections import defaultdict
import time

def best_paths_from(g, start_node, dest_nodes):
    """

    :param g: {'node': [('dest_node', cost), ...]}
    :param start_node: 'node'
    :param dest_nodes: set(['node_a', 'node_b'])
    :return: [('dest_node', [('edge_src', 'edge_dest'), ...], cost), ...]
    """
    num_nodes = len(g)
    visited = set()
    num_visited = 1
    num_to_find = len(dest_nodes)

    paths = [] # [(node, path, cost)] path to node from start_node
    sol_paths = []
    sols_found = set()

    current_node = start_node
    current_path = []
    current_cost = 0

    while num_visited < num_nodes and num_to_find > 0:
        visited.add(current_node)
        num_visited += 1
        # print("--visited {} out of {}".format(num_visited, num_nodes))
        for dest_node, cost in g.get(current_node, []):
            if dest_node in visited:
                continue
            paths.append((dest_node, current_path + [(current_node, dest_node)], current_cost + cost))
        paths.sort(key=lambda t: -t[2])
        if len(paths) == 0:
            break
        current_node, current_path, current_cost = paths.pop()
        if current_node not in sols_found and current_node in dest_nodes:
            sol_paths.append((current_node, current_path, current_cost))
            sols_found.add(current_node)
            dest_nodes.remove(current_node)
            num_to_find -= 1

    for dest_node, path, cost in reversed(paths):
        if dest_node not in sols_found and dest_node in dest_nodes:
            sol_paths.append((dest_node, path, cost))
            sols_found.add(dest_node)

    return sol_paths


# g = {
#     'a': [('b', 100.), ('c', 1.)],
#     'b': [('d', 1.), ('f', 2.5)],
#     'c': [('e', 1.5)],
#     'd': [('b', 1.), ('e', 1.)],
#     'e': [('d', 1.), ('c', 1.5), ('f', 1)],
#     'f': [('b', 2.5), ('e', 1)]
# }


g = defaultdict(list)
num_read = 0
for line in open('e_simp_mhn.csv'):
    src, dest, cost = line.split(',')
    cost = float(cost)
    num_read += 1
    g[src].append((dest, cost))

print("finished reading graph of size {}".format(len(g)))

# print(g)


node_list = sorted(g.keys(), key = int)
node_list = [node for node in node_list if len(g[node]) > 2]


num_nodes = len(node_list)
print("finding paths for {} intersection nodes".format(num_nodes))
with open('all_paths_mhn_simp.csv', 'w') as f:
    for i in range(0, num_nodes - 1):
        start_node = node_list[i]

        before = time.time()
        paths = best_paths_from(g, start_node, set(node_list[i+1:]))
        after = time.time()
        elapsed = after - before
        print("[{}] found {} paths from {} in {:.3f}s".format(i, len(paths), start_node, elapsed))
        for dest_node, path, cost in sorted(paths, key=lambda p: p[0]):
            f.write(','.join([start_node, dest_node, '{:.3f}'.format(cost)] + [d for (s,d) in path]))
            f.write('\n')
        f.flush()

