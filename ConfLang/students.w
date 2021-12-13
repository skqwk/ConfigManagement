{
    # это блок кода
    # здесь можно создать переменные
    subject = "Конфигурационное управление";
    groups = for(1 25 1 "ИКБО-&-20"); 
    student1 = 
    (
        age(19)
        group("ИКБО-4-20")
        name("Иванов И.И.")
    );
    student2 =
    (
        age(18)
        group("ИКБО-4-20")
        name("Петров П.П.")
    );
    student3 =
    (
        age(18)
        group("ИКБО-5-20")
        name("Сидоров С.С.")
    );
}

(
    groups(
            &groups
          )
    students(
            &student1 
            &student2 
            &student3
        (
            age(20) group("ИКБО-6-20") name("Козлов К.К.")
        )
    ) 
subject(&subject)
)