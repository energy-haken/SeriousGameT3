define z = Character("Z")
define a = Character("A")
define student = Character("Student")
label start:
    scene room
    show z
    z " You need to work on this project " 
    hide z
    show a
    a " And you must find a Stage !! " 
    hide a
    show student
    student " What should i do " 
    menu:
        "What will you do"
        "Work":
            "You chose : Work"
            jump jump_to_4848701439648416416
        "Find a stage":
            "You chose : Find a stage"
            jump jump_to_1579036270752386664
label jump_to_4848701439648416416:
    scene room
    show z
    z " Good work ! " 
    return
label jump_to_1579036270752386664:
    scene room
    show a
    a " I'm proud of you " 
    return
