define willy_wonka = Character("Willy Wonka")
define bob = Character("Bob")
define zdo = Character("zdo")
define zdo_intrigued = Character("zdo intrigued")
label start:
    scene bg room
    show willy wonka
    willy_wonka " HEKLP! " 
    hide willy wonka
    show bob
    bob " Hi, I'm Bob " 
    hide bob
    show willy wonka
    willy_wonka " HELP ME BOB! " 
    hide willy wonka
    show bob
    bob " No " 
    hide bob
    show zdo
    zdo " Time to die " 
    hide zdo
    show zdo intrigued
    zdo_intrigued " Exterminatus " 
    return
