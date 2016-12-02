import copy
import re
import json
import argparse
import pygraphviz as pgv
from networkx.drawing.nx_agraph import from_agraph
from networkx.readwrite import json_graph

RE_DIGIT = re.compile(" \(([0-9.]+)\w*\)")
LINKS = None
NODES = None
PARENT_MARKS = set()


def find_children(index, root_node):
    global LINKS, NODES, PARENT_MARKS
    PARENT_MARKS.add(index)
    children = []
    c_nodes = []
    for node in LINKS:
        if node['target'] in PARENT_MARKS:
            continue
        if index == node['source']:
            children.append(node['target'])
    if len(children) != 0:
        if 'children' not in root_node:
            root_node['children'] = []
        cnt = 0
        for child in children:
            name = NODES[child]['label'].replace('\\n', '\n')
            if 'size' not in NODES[child]:
                # NOTE: ignore to function local buffer
                size = float(NODES[child]['tooltip'])
                continue
            else:
                size = NODES[child]['size']
            root_node['children'].append({'name': name, 'size': size})
            c_nodes.append(find_children(child, root_node['children'][cnt]))
            cnt += 1
        root_node['children'] = copy.copy(c_nodes)
        if len(root_node['children']) == 0:
            del(root_node['children'])
    return copy.copy(root_node)


def main():
    global NODES, LINKS
    parser = argparse.ArgumentParser(description='Render a dot tree as a treemap.')
    parser.add_argument('filepath', help='A dot file')

    args = parser.parse_args()

    graph = pgv.AGraph(args.filepath)
    graph_netx = from_agraph(graph)
    graph_json = json_graph.node_link_data(graph_netx)
    root_node_index = 0
    root = {}
    for cnt, node in enumerate(graph_json['nodes']):
        _id = node['id']
        if _id[:2] != "NN" and _id[0] != "L":
            s = RE_DIGIT.search(node['tooltip'])
            size = float(s.group(1))
            node['size'] = size
        if _id == 'N1':
            root_node_index = cnt
            root = {'name': node['tooltip'], 'size': size}

    LINKS = [n for n in graph_json['links']]
    NODES = [n for n in graph_json['nodes']]
    ret = find_children(root_node_index, root)
    print(json.dumps(ret))

if __name__ == '__main__':
    main()
