define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
label start:
    scene forest
    show willy wonka
    willy_wonka " I hate cappuccino " 
    hide willy wonka
    show bob
    bob " Hi, I'm Bob " 
    menu:
        "menu"
        "Eat cheese":
            "You chose : Eat cheese"
            jump jump_to_15831068538432865581
        "Eat cheese":
            "You chose : Eat cheese"
            jump jump_to_218285705758852615
label jump_to_15831068538432865581:
    scene forest
    show bob
    bob " Hi, I'm Bob " 
    return
label jump_to_218285705758852615:
    scene forest
    show bob
    bob " Hi, I'm Bob " 
    return
