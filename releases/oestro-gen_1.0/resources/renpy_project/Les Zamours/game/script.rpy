define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
label start:
    scene room
    show willy wonka
    willy_wonka " I hate cappuccino " 
    menu:
        "Does it work?"
        "test_banana2667253770613835830":
            "You chose : test_banana2667253770613835830"
            jump jump_to_12288968059842937238
        "test_banana17390290513079323662":
            "You chose : test_banana17390290513079323662"
            jump jump_to_12827071470462911879
label jump_to_12288968059842937238:
    scene room
    show bob
    bob " Hi, I'm Bob " 
    return
label jump_to_12827071470462911879:
    scene room
    show bob
    bob " Hi, I'm Bob " 
    return
