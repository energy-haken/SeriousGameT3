define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
label start:
    scene room
    show willy wonka
    willy_wonka " Does it Worek? " 
    menu:
        "Does it Worek?"
        "Yes :D":
            "You chose : Yes :D"
            jump jump_to_3611109038596376885
        "No >:(":
            "You chose : No >:("
            jump jump_to_8276925201764139426
label jump_to_3611109038596376885:
    scene room
    show bob
    bob " Hi, Yes it Worek! " 
    return
label jump_to_8276925201764139426:
    scene room
    show bob
    bob " Sorry, it doesn't Worek. " 
    return
