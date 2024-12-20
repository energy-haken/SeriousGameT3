define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
label start:
    scene room
    show willy wonka
    willy_wonka " I hate cappuccino " 
    menu:
        "Menu name here"
        "1":
            "You chose : 1"
            jump jump_to_13427881501997157959
        "2":
            "You chose : 2"
            jump jump_to_6147279365444420962
        "3":
            "You chose : 3"
            jump jump_to_18386308928814661794
label jump_to_13427881501997157959:
    scene room
    show bob
    bob " 1 " 
    return
label jump_to_6147279365444420962:
    scene room
    show bob
    bob " 2 " 
    return
label jump_to_18386308928814661794:
    scene room
    show bob
    bob " 3 " 
    return
