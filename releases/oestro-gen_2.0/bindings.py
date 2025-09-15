from tkinter import END

def test_is_num(e):
    test_char = e.char
    if not is_num(test_char):
        delete_last_character(e.widget, is_num)

def test_is_float(e):
    test_char = e.char
    if not test_char == "\r":
        if not is_float(test_char):
            if not test_char == '.':  # for float
                delete_last_character(e.widget, is_float)
        float_delete_dots(e.widget)

def test_is_alpha(e):
    test_char = e.char
    if not is_alpha(test_char):
        delete_last_character(e.widget, is_alpha)

def is_num(char):
    if not char.isnumeric() and not char == '\b':
        return False
    else:
        return True

def is_float(char):
    try:
        float(char)
        return True
    except ValueError:
        return False

def is_alpha(char):
    if (not char.isalnum() and not char.isspace() and not char == '\b'
            and not char == '.' and not char == ',' and not char == '!' and not char == '?'):  # \b is backspace
        return False
    else:
        return True

def float_delete_dots(widget):
    i = 0
    nb_dots = 0
    new_text = widget.get()
    for char in widget.get():
        if char == '.':
            nb_dots += 1
        if nb_dots > 1:
            temp_list = list(new_text)  # need to convert to list, because string are immutable in python
            temp_list[i] = " "  # can't delete since it's a foreach, so we replace
            new_text = ''.join(temp_list)  # convert back to string
        i += 1
    new_text = new_text.replace(" ", "")  # get rid of the white space previously generated
    widget.delete(0, END)
    widget.insert(0, new_text)

def delete_last_character(widget, test):
    current_widget = widget
    new_text = current_widget.get()
    for char in current_widget.get():
        if not test(char):
            new_text = new_text.replace(char, '')
    current_widget.delete(0, END)
    current_widget.insert(0, new_text)