define chirac = Character("Chirac")
define zimao = Character("zimao")
label start:
    scene room
    show chirac
    chirac " I love apples " 
    menu:
        "And you?"
        "Yes.":
            "You chose : Yes."
            jump jump_to_16099613458293605482
        "No.":
            "You chose : No."
            jump jump_to_14998962236388558443
label jump_to_16099613458293605482:
    scene room
    show chirac
    chirac " Good, me too. " 
    return
label jump_to_14998962236388558443:
    scene room
    show zimao
    zimao " You will be purged by the great Moulinette " 
    return
