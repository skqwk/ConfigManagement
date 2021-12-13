all: hello

hello: main.o factorial.o hello.o
 g++ main.o factorial.o hello.o -o hello
 echo "Компоновка исполняемого файла"

main.o: main.cpp
 g++ -c main.cpp
 echo "Компиляция main.cpp"

factorial.o: factorial.cpp
 g++ -c factorial.cpp
 echo "Компиляция factorial.cpp"

hello.o: hello.cpp
 g++ -c hello.cpp
 echo "Компиляция hello.cpp"