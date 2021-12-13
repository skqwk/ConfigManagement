import zipfile
import archive
import sys

def main():
    name = sys.argv[1]
    with zipfile.ZipFile(name, 'r') as zip:
        arch = archive.Archive(zip)
        while True:
            print(f"[User]:{arch.currentDir}", end=": ")
            commands = input().split()
            if len(commands) < 1:
                continue
            elif commands[0] == "pwd":
                print(arch.currentDir)

            elif commands[0] == "ls":
                try: 
                    arch.getData(commands)
                except Exception as e:
                    print(e)

            elif commands[0] == "cd":
                try:
                    arch.comeDirectory(commands[1])
                except Exception as e:
                    arch.comeDirectory("/"+arch.rootDir)

            elif commands[0] == "cat":
                try:
                    arch.catenate(commands[1])
                except Exception as e:
                    print()

            elif commands[0] == "exit":
                break
            else:
                print("Command is not recognized")
        
main()
