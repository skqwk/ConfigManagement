
import json
import codecs
import sys

from top_sort import topSort
from analyzer import analyzeData
import os
import hashlib

MEMORY_PATH = 'memory.json'


def createGrapfvizCode(lines):
    dependencies = []
    for line in lines:
        if (isinstance(line, dict)):
            for key in line:
                for node in line[key]:
                    dependencies.append(f'"{key}" -> "{node}";')
    graphvizCode = ""
    for dependency in dependencies:
        graphvizCode += dependency + '\n'
    return graphvizCode

def readMakefile(path):
    f = codecs.open( path, "r", "utf-8" )
    return f.read()

def correspondTasksAndCommands(lines):
    tasksAndCommands = {}
    singleTaskAndCommand = {}
    task = ''
    for line in lines:
        if (isinstance(line, dict)):
            if (singleTaskAndCommand):
                tasksAndCommands.update(singleTaskAndCommand)
            task = list(line.keys())[0]
            singleTaskAndCommand = {task : []}
        else:
            singleTaskAndCommand[task].append(line)
    tasksAndCommands.update(singleTaskAndCommand)

    return tasksAndCommands

def getGraphFromLines(lines):
    graph = {}
    for line in lines:
            if (isinstance(line, dict)):
                graph.update(line)
    return graph

def execute(sortedTasks, tasksAndCommands):
    for task in sortedTasks:
        for command in tasksAndCommands[task]:
            os.system(command)

def excludeOrCreateMemory():
    memory = {}
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'r+', encoding='utf-8') as json_file:
                memory = json.load(json_file)
    return memory

def isNeedMakeFile(file, memory):
    # Если файла по данному пути не существует - задачу нужно выполнить
    if not os.path.exists(file):
        return True

    # Если файл существует - нужно посчитать его хэш 
    hasher = hashlib.md5()
    # Читаем содержимое файла, получаем хэш
    with open(file, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        hash = hasher.hexdigest()
    
    # Если файл уже есть в памяти
    if file in memory:
        # И он был изменен - нужно будет обновить его хэш в памяти и
        # выполнить задачу снова
        if not (hash == memory[file]):
            memory.update({file : hash})
            return True

        # Файл не изменился - не обновляем память, не выполняем задачу
        else:
            return False
    # Если файла не было в памяти - добавляем и выполняем
    else:
        memory.update({file : hash})
        return True
         
# Передаем задачу с ее зависимостями target : dependencies
# Необходимость выполнения цели зависит от того,
# изменились ли ее зависимости и сама цель
def checkIfNeedExecute(graph, memory):
    needExecute = {}
    for branch in graph:
        isNeeded = False
        for node in graph[branch]:
            isNeeded |= isNeedMakeFile(node, memory)
        isNeeded |= isNeedMakeFile(branch, memory)
        if isNeeded:
            needExecute.update({branch: graph[branch]})
    return needExecute

def main():
    # читаем make-файл
    enableGraphviz = False
    if len(sys.argv) > 2:
        path = sys.argv[2]
        enableGraphviz = (sys.argv[1] == '-v')
    else:
        path = sys.argv[1]
    data = readMakefile(path)

    # разбираем его
    lines = analyzeData(data)
    
    if enableGraphviz:        
        graphvizCode = createGrapfvizCode(lines)
        print(graphvizCode)

    # сопоставляем задачу и команды для ее выполнения 
    tasksAndCommands = correspondTasksAndCommands(lines)

    # print('tasksAndCommands: ')
    # print(tasksAndCommands)

    graph = getGraphFromLines(lines)

    # print("graph: ")
    # print(graph)

    # извлекаем или создаем память
    memory = excludeOrCreateMemory()

    # print(memory)

    # выбираем команды для исполнения
    needExecute = checkIfNeedExecute(graph, memory)

    # print("needExecute:")
    # print(needExecute)

    sortedTasks = topSort(needExecute)

    # print("sortedTasks:")
    # print(sortedTasks)

    # выполняем необходимые команды
    execute(sortedTasks, tasksAndCommands)

    # переводим память обратно в json в том случае, если она использовалась
    # print(memory)
    if memory:
        with open(MEMORY_PATH, "w", encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)

main()