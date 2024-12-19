define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
label start:
    scene room
    show willy wonka
    willy_wonka " I hate cappuccino " 
    menu:
        "Do you like capucionionio?"
        "Ye":
            "You chose : Ye"
            jump jump_to_15945050526914265431
        "Ney":
            "You chose : Ney"
            jump jump_to_6366640239748270595
label jump_to_15945050526914265431:
    scene room
    show bob
    bob " You're a horrible person " 
    return
label jump_to_6366640239748270595:
    scene room
    show bob
    bob " Ye, fuck capucini " 
    return
