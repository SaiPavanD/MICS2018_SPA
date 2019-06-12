import ast
import sys
import pygraphviz as pgv

def __get_class(var_name):
    # for key, value in metadata.items():
    #     if search_value in value:
    #         return key
    return type_data[var_name]

def __add_node(from_, to_):
    # to_ = node.func
    try:
        # Function/Class
        if to_.id in metadata:
            graph.add_edge(from_,to_.id + '__' + '__init__')
        else:
            graph.add_edge(from_,to_.id)
    except:
        # Method
        graph.add_edge(from_,__get_class(to_.value.id)+'__'+to_.attr)

if len(sys.argv) != 3:
    print "Usage - python python_callgraph.py <input_program> <output_file>"
    sys.exit(-1)

with open(sys.argv[1], 'r') as fp:
    input_program = fp.read()

# generate the syntax tree
root = ast.parse(input_program)

# generate a metadata for variable, class and methods
metadata = {'main':[]}

type_data = {}

for child in ast.iter_child_nodes(root):
    # check for function definitions in main
    if child.__class__.__name__ == 'FunctionDef':
        metadata['main'] += [child.name]
    # check for class definitions in main
    if child.__class__.__name__ == 'ClassDef':
        metadata[child.name] = []
        # check for corresponding methods
        for node in ast.walk(child):
            if node.__class__.__name__ == 'FunctionDef':
                metadata[child.name] += [node.name]
        # Add __init__ if not already present
        if '__init__' not in metadata[child.name]:
            metadata[child.name] += ['__init__']

for node in ast.walk(root):
    if node.__class__.__name__ == 'Assign':
        try:
            type_data[node.targets[0].id] = node.value.func.id
        except:
            pass

# init the call the graph
graph = pgv.AGraph(strict=False,directed=True)
for class_ in metadata:
    # graph.add_node(class_)
    for method in metadata[class_]:
        graph.add_node(class_ + '__' + method, label = method)
for class_ in metadata:
    graph.add_subgraph([class_ + '__' + method for method in metadata[class_]], name = 'cluster_' + class_, label = class_)

# identify all function and method calls and build the call graph
for child in ast.iter_child_nodes(root):
    # check for calls in main
    if child.__class__.__name__ != 'ClassDef' and child.__class__.__name__ != 'FunctionDef':
        for node in ast.walk(child):
            if node.__class__.__name__ == 'Call':
                __add_node('main', node.func)

    # check for calls in function definitions
    if child.__class__.__name__ == 'FunctionDef':
        for node in ast.walk(child):
            if node.__class__.__name__ == 'Call':
                __add_node('main__'+child.name, node.func)

    # check for calls in class definitions
    if child.__class__.__name__ == 'ClassDef':
        # check for corresponding methods
        for node in ast.walk(child):
            if node.__class__.__name__ == 'FunctionDef':
                for node2 in ast.walk(node):
                    if node2.__class__.__name__ == 'Call':
                        __add_node(child.name+'__'+node.name, node2.func)


graph.layout(prog='dot')
graph.write(sys.argv[2] + '.dot')
graph.draw(sys.argv[2])
