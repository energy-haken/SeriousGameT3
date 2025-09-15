define super_sexy_santa = Character("Super Sexy Santa")
define bob = Character("Bob")
define weedo = Character("Weedo")
label start:
    scene room
    show super sexy santa
    super_sexy_santa " MERRY CHRISTMAS! " 
    menu:
        "What will you ask santa?"
        "test_banana3704133587496290141":
            "You chose : test_banana3704133587496290141"
            jump jump_to_8930583773802351095
        "test_banana6602855303062700121":
            "You chose : test_banana6602855303062700121"
            jump jump_to_11680770448837265811
label jump_to_8930583773802351095:
    scene room
    show bob
    bob " Hi, I'm your gift! " 
    return
label jump_to_11680770448837265811:
    scene room
    show super sexy santa
    super_sexy_santa " Really? What kind of naughty? " 
    menu:
        "What kind of naughty?"
        "test_banana929272510723083167":
            "You chose : test_banana929272510723083167"
            jump jump_to_12889468267835703911
        "test_banana6654791296107692856":
            "You chose : test_banana6654791296107692856"
            jump jump_to_1693671719669220802
label jump_to_12889468267835703911:
    scene room
    show super sexy santa
    super_sexy_santa " Coal for you! " 
    hide super sexy santa
    show weedo
    weedo " I love weed. " 
    return
label jump_to_1693671719669220802:
    scene room
    show super sexy santa
    super_sexy_santa " Pink coal for you! " 
    return
