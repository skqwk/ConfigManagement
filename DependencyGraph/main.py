import zipfile 
import requests
import io
import sys

def main():
    main_package = main_dir
    deps = getDeps(main_package)
    nested_dicts = formatDepsToNestedDicts(main_package, deps)
    links = convertNestedDictsToLinks(nested_dicts)
    graphvizCode = "digraph G {\n"+links+"}"
    print(graphvizCode)

def getDeps(package_name):
    r = requests.get(f"https://pypi.org/pypi/{package_name}/json").json()
    version = r["info"]["version"]
    releases = r["releases"]
    last_release = releases[version][0]
    url_whl = last_release["url"]
    name = url_whl.split("/")[-1]
    whl_file = requests.get(url_whl)
    z = zipfile.ZipFile(io.BytesIO(whl_file.content))
    for zip_name in z.namelist():
        if zip_name.endswith("METADATA"):
            metadata = (str(z.read(zip_name), 'utf-8')) 
    lines = metadata.split("\n")
    deps = set()
    for line in lines:
        if "Requires-Dist" in str(line):
            dep = str(line).split(" ")
            if "extra" in dep: break
            dep =dep[1]
            dep = dep.split("\\")[0]
            deps.add(dep)
    return deps

def formatDepsToNestedDicts(main_package, deps):
    deps_format = {}
    deps_format[main_package] = []
    if deps is None: 
        return deps_format
    for dep in deps:
        dep = dep.split(" ")
        if dep == main_dir: continue
        if not "extra" in dep:
            package_name = dep[0]
            internal_deps = getDeps(package_name)
            internal_deps_format = formatDepsToNestedDicts(package_name, internal_deps)
            deps_format[main_package].append(internal_deps_format)
    return deps_format

def convertNestedDictsToLinks(nested_dicts):
    graphviz_code = ""
    for key in nested_dicts:
        if nested_dicts[key] == []:
            return f"\"{key}\";\n"
        for dict in nested_dicts[key]:
            graphviz_code+=f"\"{key}\"->{convertNestedDictsToLinks(dict)}"
    return graphviz_code        

main_dir = sys.argv[1]
main() 