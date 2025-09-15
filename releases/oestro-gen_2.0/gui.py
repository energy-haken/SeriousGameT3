import os
import typing
from pathlib import Path
import pathlib
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from customtkinter import *
from tkinter import *
from PIL import ImageTk
from idlelib.tooltip import Hovertip
import random
import torch

from dialog_object_observer import DialogObjectObserver
from dialog_object_ui import on_click_change_dialog_object, destroy_choices, update_dialog_object_name, \
    destroy_dialog_object
from model_object.character_object import Character
from dialog_object import DialogObject
from generation_type import GenerationType
from model_observer import ModelObserver
from idlelib.tooltip import Hovertip 
from utils import error_handler, change_validate, resize_image
from dialog_object import DialogObject
from generation_type import GenerationType
from model_observer import ModelObserver
from file_writer import HomeMadeFileWriter
from renpy_converter.object_to_script_converter import ObjToScriptConverter
from renpy_project_creator import RenpyProjectCreator
from bindings import test_is_num, test_is_float, test_is_alpha, is_num, is_float, is_alpha, float_delete_dots, delete_last_character

class Gui(ModelObserver, DialogObjectObserver):
        logo_image = None
        prompt = None
        output = None
        button_generate = None
        user_input_global = None
        model_label = None
        parameters = None
        parameters_entry_list = None
        image_label = None
        generation_type = GenerationType.TEXT
        context = None
        window = None
        canvas = None
        first_object = None
        project_name = None
        model_controller = None
        prompt_label_global = None
        gen_type_label = None
        processing_type_button = None
        image_cache = None # stored image if the user want to save it
        first_obj = None
        resize_ratio = 1.0
        combobox_project = None
        nb_opened_window = 0
        canvas_visualiser = None
        choosed_character = None
        frame_character1 = None
        frame_character2 = None
        frame_character3 = None
        frame_character4 = None
        canva_visualiser = None
        frame_parameters_state = None
        frame_character_creation_state = None
        frame_picture_state = None
        outer_frame_left_state = None
        outer_frame_left = None
        inner_frame_left = None
        frame_character = None
        frame_pictures = None
        outer_frame_right = None
        outer_frame_right_state = None
        selected_dialog_object: int = None
        dialog_object_tag_list: typing.List[int] = []
        character_combobox = None

        def create_character(self):
            name = self.entry_name.get()
            if name:
                self.character_instance = Character(name)
                change_validate(self.window, f"Character '{name}' created.")
                
                # Save character to file
                file_writer = HomeMadeFileWriter()
                file_writer.set_file(f"resources/characters/{name}.json")
                file_writer.set_mode("w")
                file_writer.write(file_writer.dump_json(self.character_instance))
                self.populate_character_combobox()  # Refresh the character list in the combobox

        def add_expression(self):
            if self.character_instance:
                expr = self.entry_expr.get()
                if expr:
                    self.character_instance.add_expression(expr)
                    current_values = list(self.combobox_expressions["values"])
                    if expr not in current_values:
                        current_values.append(expr)
                        self.combobox_expressions["values"] = current_values
                       # auto-select newly added
                    change_validate(self.window, f"Expression '{expr}' added.")
                    
                    # Save updated character to file
                    file_writer = HomeMadeFileWriter()
                    file_writer.set_file(f"resources/characters/{self.character_instance.get_name()}.json")
                    file_writer.set_mode("w")
                    file_writer.write(file_writer.dump_json(self.character_instance))
            else:
                error_handler(self.window, "Create a character first.")

        def add_expression_to_character(self):
            """Add an expression to the selected character."""
            if self.character_instance:
                expr = self.text_expression.get()
                if expr:
                    self.character_instance.add_expression(expr)
                    current_values = list(self.combobox_expressions["values"])
                    if expr not in current_values:
                        current_values.append(expr)
                        self.combobox_expressions["values"] = current_values
                    
                    change_validate(self.window, f"Expression '{expr}' added to character '{self.character_instance.get_name()}'.")
                    
                    # Save updated character to file
                    file_writer = HomeMadeFileWriter()
                    file_writer.set_file(f"resources/characters/{self.character_instance.get_name()}.json")
                    file_writer.set_mode("w")
                    file_writer.write(file_writer.dump_json(self.character_instance))
                else:
                    error_handler(self.window, "Expression cannot be empty.")
            else:
                error_handler(self.window, "No character selected. Please select or create a character.")

        def populate_character_combobox(self):
            """Populate the character selection combobox with JSON files from the resources/characters folder."""
            character_folder = pathlib.Path("resources/characters")
            if character_folder.is_dir():
                character_files = [file.stem for file in character_folder.glob("*.json")]
                if character_files:
                    self.character_combobox["values"] = character_files
                    print(f"Characters loaded: {character_files}")  # Debug: Print loaded characters
                else:
                    print("No character files found in the folder.")  # Debug: No files found
            else:
                error_handler(self.window, f"Character folder not found: {character_folder}")

        def select_character(self, event):
            """Load the selected character from the JSON file."""
            selected_character_name = self.character_combobox.get()
            if selected_character_name:
                # Load character from file
                file_writer = HomeMadeFileWriter()
                file_writer.set_file(f"resources/characters/{selected_character_name}.json")
                character_data = file_writer.load_json()
                self.character_instance = file_writer.convert_dict_to_object(character_data)
                
                # Update UI with loaded character data
                current_values = self.character_instance.get_expressions()
                self.combobox_expressions["values"] = current_values
                if current_values:
                    self.expression_var.set(current_values[0])  # auto-select the first expression
                change_validate(self.window, f"Character '{selected_character_name}' loaded.")
            else:
                error_handler(self.window, "No character selected.")

        def __init__(self, window, model_controller):
                self.prompt = "Steve le...POAAAAAA"
                self.output = "Le poisson Steve"
                self.prompt_label_global = None
                self.user_input_global = None
                self.parameters = {}
                self.model_controller = model_controller
                self.model_controller.add_observer(self)
                self.button_generate = None
                self.context = None
                self.window = window
                self.window.configure(background="#0D0B0B")
                self.window.state('zoomed') #Full screen zoomed
                self.frame_character_creation_state = False
                self.frame_picture_state = False
                self.frame_parameters_state = False
                self.outer_frame_left_state = False
                self.outer_frame_right_state = False


                self.logo_image = resize_image("images/LogoApp.png", 400, 160)  # Make sure this returns a PhotoImage


                 # Set the geometry to full screen size
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()
                window.geometry(f"{screen_width}x{screen_height}")



                outer_frame_left = CTkFrame(self.window, corner_radius=50, width=410, height=screen_height-50, bg_color="#1D1B1B")
                outer_frame_left.pack(side=LEFT , fill=X, padx=30)
                self.outer_frame_left = outer_frame_left
                self.outer_frame_left_state = True

                outer_frame_right = CTkFrame(self.window, corner_radius=50, width=410, height=screen_height-50, bg_color="#1D1B1B")
                outer_frame_right.pack(side=RIGHT , fill=X, padx=30)
                self.outer_frame_right = outer_frame_right
                self.outer_frame_right_state = True

                # Inner frame to provide the background color behind the rounded corners
                inner_frame_left = CTkFrame(outer_frame_left, corner_radius=50, width=410, height=screen_height-50, bg_color="#0D0B0B", fg_color="#1D1B1B")
                inner_frame_left.place(relx=0, rely=0, relwidth=1, relheight=1)
                self.inner_frame_left = inner_frame_left

                inner_frame_right = CTkFrame(outer_frame_right, corner_radius=50, width=410, height=screen_height-50, bg_color="#0D0B0B")
                inner_frame_right.place(x=0, y=0)
                self.frame_pictures = inner_frame_right
                self.frame_picture_state = True

                self.frame_parameters_state = True

               


                # Frame for the character creation

                frame_character = CTkFrame(outer_frame_left, corner_radius=50, width=410, height=screen_height-50, bg_color="#0D0B0B", fg_color="#1D1B1B")
                self.frame_character = frame_character

                logo_label2 = CTkLabel(frame_character, image=self.logo_image, text="")  # Use CTkLabel for consistency
                logo_label2.pack(side=TOP ,pady=25)

                frame_character_creation = CTkFrame(frame_character, corner_radius=50, width=410, height=screen_height-50, fg_color="#383535")
                frame_character_creation.pack(side=TOP, fill=X, padx=20, pady=10)




                # === Section: Création du personnage ===

                label_name = CTkLabel(frame_character_creation, text="Character Name", text_color="white", font=("Khmer", 16))
                label_name.pack(pady=5)

                self.entry_name = CTkEntry(frame_character_creation, width=200)
                self.entry_name.pack(pady=5)

                # Stocke l'instance du personnage créé
                self.character_instance = None

                button_create = CTkButton(frame_character_creation, text="Create Character", command=self.create_character)
                button_create.pack(pady=5)

                # === Section: Ajouter une expression ===
                label_expr = CTkLabel(frame_character_creation, text="Add Expression", text_color="white", font=("Khmer", 16))
                label_expr.pack(pady=5)

                self.entry_expr = CTkEntry(frame_character_creation, width=200)
                self.entry_expr.pack(pady=5)

                button_expr = CTkButton(frame_character_creation, text="Add Expression", command=self.add_expression)
                button_expr.pack(pady=5)

                # === Section: Liste des expressions ajoutées ===
                label_expr_list = CTkLabel(frame_character_creation, text="Available Expressions", text_color="white", font=("Khmer", 16))
                label_expr_list.pack(pady=5)

                self.expression_var = StringVar()
                self.combobox_expressions = ttk.Combobox(frame_character_creation, textvariable=self.expression_var, state="readonly", width=27)
                self.combobox_expressions.pack(pady=5)
                self.combobox_expressions["values"] = []  # start empty

                # Select a character from those creater (JSON)

                frame_character_selection = CTkFrame(frame_character, corner_radius=50, width=410, height=screen_height-50, fg_color="#383535")
                frame_character_selection.pack(side=TOP, fill=X, padx=20, pady=10)

                label_new_section = CTkLabel(frame_character_selection, text="Select Character", text_color="white", font=("Khmer", 16))
                label_new_section.pack(pady=5)

                combo_character = ttk.Combobox(frame_character_selection, state="readonly", width=27)
                combo_character.pack(pady=5)
                combo_character["values"] = []  # start empty

                combo_character.bind("<<ComboboxSelected>>", self.select_character)

                self.character_combobox = combo_character  # Store the combobox for later use

                 # fill the combo box of characters

                self.populate_character_combobox()

                text_expression = CTkEntry(frame_character_selection, width=200)
                text_expression.pack(pady=5)

                button_add_expression = CTkButton(frame_character_selection, text="Add Expression", command=lambda:self.add_expression_to_character)
                button_add_expression.pack(pady=5)

                frame_image = CTkFrame(frame_character_selection, width=200, height=200, corner_radius=20, fg_color="#1D1B1B")
                frame_image.pack(side=TOP, fill=X, padx=20, pady=10)

                label_image = CTkLabel(frame_image, text="Image", text_color="white", font=("Khmer", 16))
                label_image.pack(side=TOP, padx=10)

                button_add_image = CTkButton(frame_image, text="Add Image", command=lambda: self.add_image_to_character())
                button_add_image.pack(side=TOP, padx=10, pady=10)

                button_delete_character = CTkButton(frame_character_selection, text="Delete Character", command=lambda: self.delete_character())
                button_delete_character.pack(pady=5)





                # NavBar at the top of the screen

                frame_navbar = CTkFrame(self.window, width=screen_width-820, height=100, fg_color="#383535")
                frame_navbar.pack(side=TOP, fill=Y, pady=20)

                label_navbar = CTkLabel(frame_navbar, text="Navigation", text_color="white", font=("Khmer", 20))
                label_navbar.pack(side=TOP, padx=20)

                button_frame_parameters = CTkButton(frame_navbar, text="Parameters", width=200, height=50, fg_color="#0e471e" ,hover_color="#1D1B1B", text_color="white", command=lambda: self.set_state_left(self.inner_frame_left))
                button_frame_parameters.pack(side=LEFT, padx=20, pady=10)

                button_frame_character_creation = CTkButton(frame_navbar, text="Character Creation", width=200, height=50, fg_color="#0e471e" ,hover_color="#1D1B1B", text_color="white", command=lambda: self.set_state_left(self.frame_character))
                button_frame_character_creation.pack(side=LEFT, padx=20, pady=10)

                button_frame_picture = CTkButton(frame_navbar, text="Picture", width=200, height=50, fg_color="#0e471e" ,hover_color="#1D1B1B", text_color="white", command=lambda: self.set_state_right(self.frame_pictures))
                button_frame_picture.pack(side=LEFT, padx=20, pady=10)
                # All the buttons below the screen

                frame_buttons = CTkFrame(self.window, width=screen_width-820, height=100, fg_color="#0D0B0B")
                frame_buttons.pack(side=BOTTOM, fill=Y, pady=20)

                self.button_generate = CTkButton(frame_buttons, text="Generate", width=200, height=50, fg_color="green" ,hover_color="#1D1B1B", text_color="white", command=lambda: self.generate())
                self.button_generate.pack(side=LEFT, padx=20)

                button_generate_script = CTkButton(frame_buttons, text="Generate script", width=200, height=50, fg_color="#0e471e" ,hover_color="#1D1B1B", text_color="white", command=lambda: self.generate_text())
                button_generate_script.pack(side=LEFT, padx=20)



                # The user input fields

                frame_inputs = CTkFrame(self.window, width=screen_width-820, height=200, fg_color="#0D0B0B")
                frame_inputs.pack(side=TOP, fill=Y, pady=20)

                frame_contexto = CTkFrame(frame_inputs, width=450, height=300, corner_radius=20, fg_color="#383535")
                frame_contexto.pack(side=LEFT, fill=X, padx=20, pady=10)

                frame_prompt = CTkFrame(frame_inputs, width=450, height=300, corner_radius=20, fg_color="#383535")
                frame_prompt.pack(side=RIGHT, fill=X, padx=20, pady=10)

                label_context = Label(frame_contexto, text="Context :", background="#383535", foreground="white", font=("Khmer", 15))
                label_context.pack(side=TOP, padx=10, pady=3)

                text_context = Entry(frame_contexto, width=30, font=("Khmer", 15))
                text_context.pack(side=TOP, padx=10)

                list_context = ttk.Combobox(frame_contexto, width=28, font=("Khmer", 15), foreground="white", state="readonly")
                list_context.pack(side=TOP, padx=10, pady=3)
                list_context["values"] = ["Premade Context", "Medieval", "School", "Sci-fi", "Fantasy", "Modern"]

                label_prompt = Label(frame_prompt, text="Prompt :", background="#383535", foreground="white", font=("Khmer", 15))
                label_prompt.pack(side=TOP, padx=10, pady=10)

                text_prompt = Entry(frame_prompt, width=30, font=("Khmer", 15), text="This is a prompt")
                text_prompt.pack(side=TOP, padx=10, pady=10)

                self.user_input_global = text_prompt # store the user input to use it later

                # Initialize prompt_label_global
                self.prompt_label_global = Label(frame_prompt, text=self.prompt, background="#383535", foreground="white", font=("Khmer", 15))


                # RESULT

                # DialogObject Tree + Scrollbar
                frame_canvas = Frame(self.window, bg="#1D1B1B", width=800, height=200)
                frame_canvas.pack(pady=10, fill=BOTH, expand=True)

                canvas_output = Canvas(frame_canvas, width=900, height=200, background="#383535", highlightthickness=0)
                canvas_output.grid(row=0, column=0, sticky="nsew")

                self.canvas = canvas_output

                vbar = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas_output.yview)
                vbar.grid(row=0, column=1, sticky="ns")

                hbar = Scrollbar(frame_canvas, orient=HORIZONTAL, command=canvas_output.xview)
                hbar.grid(row=1, column=0, sticky="ew")

                canvas_output.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

                # Configure the frame to expand properly
                frame_canvas.grid_rowconfigure(0, weight=1)
                frame_canvas.grid_columnconfigure(0, weight=1)

                # Enable mouse wheel scrolling
                def on_mouse_wheel(event):
                    canvas_output.yview_scroll(-1 * int(event.delta / 120), "units")

                canvas_output.bind("<MouseWheel>", on_mouse_wheel)  # For Windows and MacOS
                canvas_output.bind("<Button-4>", lambda event: canvas_output.yview_scroll(-1, "units"))  # For Linux (scroll up)
                canvas_output.bind("<Button-5>", lambda event: canvas_output.yview_scroll(1, "units"))  # For Linux (scroll down)


                # Visualiser to see what it will look like in Ren'py
                canva_visualiser = Canvas(self.window, width=900, height=450, background="#1D1B1B")
                canva_visualiser.pack(side=TOP , pady=30)
                self.canvas_visualiser = canva_visualiser

                # Adding the component in the left frame


                logo_label = CTkLabel(inner_frame_left, image=self.logo_image, text="")  # Use CTkLabel for consistency
                logo_label.pack(side=TOP ,pady=25)

                # Frame for the project creator


                def open_project_creator_window():
                    project_window = Toplevel(self.window)
                    project_window.title("Create New Project")
                    project_window.geometry("400x300")
                    project_window.configure(bg="#1D1B1B")

                    Label(project_window, text="Project Name:", bg="#1D1B1B", fg="white", font=("Khmer", 12)).pack(pady=10)
                    project_name_var = StringVar(value="Project Name")
                    Entry(project_window, textvariable=project_name_var, font=("Khmer", 12), width=30).pack(pady=5)

                    Label(project_window, text="Resolution:", bg="#1D1B1B", fg="white", font=("Khmer", 12)).pack(pady=10)
                    combo_project_resolution = ttk.Combobox(project_window, font=("Khmer", 12), state="readonly", width=25,  foreground="white")
                    combo_project_resolution["values"] = ["1280x720", "1920x1080", "2560x1440", "3840x2160"]
                    combo_project_resolution.set("1920x1080")
                    combo_project_resolution.pack(pady=5)

                    Label(project_window, text="Theme Color:", bg="#1D1B1B", fg="white", font=("Khmer", 12)).pack(pady=10)
                    combo_project_color = ttk.Combobox(project_window, font=("Khmer", 12), state="readonly", width=25,  foreground="white")
                    combo_project_color["values"] = ["pink", "blue", "green", "red", "yellow"]
                    combo_project_color.set("pink")
                    combo_project_color.pack(pady=5)

                    def create_project():
                        name = project_name_var.get()
                        resolution = combo_project_resolution.get()
                        color = combo_project_color.get()
                        if name:
                            project_creator = RenpyProjectCreator(name, resolution, color)
                            project_creator.create_project()
                            change_validate(self.window, f"Project '{name}' created.")
                            self.combobox_project["values"] = os.listdir(path_folder)  # Update the combobox with the new project
                            project_window.destroy()
                        else:
                            error_handler(project_window, "Please enter a project name.")

                    Button(project_window, text="Create Project", bg="#383535", fg="white", font=("Khmer", 12), command=create_project).pack(pady=20)

                    def create_project(name, resolution, color):
                        if name:
                            project_creator = RenpyProjectCreator(name, resolution, color)
                            project_creator.create_project()
                            change_validate(self.window, f"Project '{name}' created.")
                            self.combobox_project["values"] = os.listdir(path_folder)  # Update the combobox with the new project
                        else:
                            error_handler(self.window, "Please enter a project name.")


                button_create_project = Button(inner_frame_left, background="#383535", fg="white", text="Create Project", font=("Khmer", 15), command=open_project_creator_window)
                button_create_project.pack(side=TOP)




                ## Frame to select the Ren'py project to use
                frame_project = Frame(inner_frame_left, width=366, height=54, bg="#1D1B1B")
                frame_project.pack(side=TOP)

                label_project = Label(frame_project, text="Project :", background="#1D1B1B", foreground="white", font=("Khmer", 15))
                label_project.pack(side=LEFT, padx=5, pady=5)

                path_folder = pathlib.Path(__file__).parent ## to get the path of the current file
                path_folder = pathlib.Path.joinpath(path_folder, "resources/renpy_project") ## add the renpy_project folder to the path

                files = os.listdir(path_folder) ## to get all the files/folder in the directory

                value_project = StringVar()
                value_project.set(path_folder)

                first_project_base = "Project : "
                first_project_base += str(path_folder) ## add the path of the project to the label


                style = ttk.Style()

                style.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox':
                                            {'configure':
                                            {'selectbackground': 'blue',
                                            'fieldbackground': '#383535',
                                            'background': 'white'
                                            }}} ## change the style of the combobox
                                )
                style.theme_use('combostyle') ## use the style for ALL the combobox

                ## Combobox to select the project
                combo_project = ttk.Combobox(frame_project, background="#383535", font=("Khmer", 15), foreground="white", values=files, state="readonly")
                combo_project.pack(fill=X, padx=5, pady=5)
                combo_project.bind("<<ComboboxSelected>>", self.update_project_name)
                self.combobox_project = combo_project # store the combobox to update the project name

                 ## Frame for the button to change the processing mode (between CPU and GPU)
                frame_processing_mode = Frame(inner_frame_left, width=366, height=54, bg="#383535")
                frame_processing_mode.pack(side=TOP, pady=10)

                ## Button to change the processing mode
                button_processing_type = Button(frame_processing_mode, background="#383535", fg="white", text="Processing-Mode : CPU", font=("Khmer", 24), command=lambda: self.change_processing_type())
                button_processing_type.pack()
                self.processing_type_button = button_processing_type




                ## Frame for the button to change the generation mode (between text and image)
                frame_generation_mode = Frame(inner_frame_left, width=366, height=54, bg="#383535")
                frame_generation_mode.pack(side=TOP, pady=10)

                button_generation_mode = Button(frame_generation_mode, background="#383535", fg="white", text="Generation-Mode : Text", font=("Khmer", 22), command=lambda: self.update_gen_type())
                button_generation_mode.pack(fill=BOTH)
                self.gen_type_label = button_generation_mode

                ## Frame for the combobox to select the model
                frame_list_model = Frame(inner_frame_left, background="#383535", width=366, height=53)
                frame_list_model.pack(side=TOP, pady=10)

                ## Combobox to select the model (yes it's a combobox, not a listbox)
                list_model = ttk.Combobox(frame_list_model, background="#383535", font=("Khmer", 23), foreground="white", state="readonly")
                list_model.place(x=0, y=0)


                ## All the parameters of the model

                ## Frame for the parameters
                frame_parameter_model = Frame(inner_frame_left, width=311, height=400, background="#383535")
                frame_parameter_model.pack(side=TOP, pady=10)

                ## Labels for the parameters
                label_parameters = Label(frame_parameter_model, text="PARAMETERS", background="#383535", foreground="white", font=("Khmer", 25))
                label_parameters.place(x=40, y=5)

                ## Parameters : max_length

                label_max_length = Label(frame_parameter_model, text="Max length", background="#383535", foreground="white", font=("Khmer", 20))
                label_max_length.place(x=5, y=55)
                tip_max_length = Hovertip(label_max_length,'taille de la réponse en caractère')

                value1 = StringVar()
                value1.set(self.get_specific_param("max_length"))
                text_max_length = Entry(frame_parameter_model, textvariable=value1, width=10)
                text_max_length.place(x=240, y=70)

                ## Parameters : num_return_sequences

                label_returned_sequence = Label(frame_parameter_model, text="Number of returned \n sequences",justify="left", background="#383535", foreground="white", font=("Khmer", 20))
                label_returned_sequence.place(x=5, y=110)
                tip_returned_sequence = Hovertip(label_returned_sequence,' self explicit')

                value2 = StringVar()
                value2.set(self.get_specific_param("num_return_sequences"))
                text_returned_sequence = Entry(frame_parameter_model, textvariable=value2, width=10)
                text_returned_sequence.place(x=240, y=150)

                ## Parameters : repetition_penalty

                label_repetition_penalty = Label(frame_parameter_model, text="Repetition penalty",justify="left", background="#383535", foreground="white", font=("Khmer", 20))
                label_repetition_penalty.place(x=5, y=190)
                tip_repetition_penalty = Hovertip(label_repetition_penalty,'pénalité lorsque le model se répète \n (favorise un vocabulaire plus diversifié )')

                value3 = StringVar()
                value3.set(self.get_specific_param("repetition_penalty"))
                text_repetition_penalty = Entry(frame_parameter_model, textvariable=value3, width=10)
                text_repetition_penalty.place(x=240, y=200)

                ## Parameters : temperature

                label_temperature = Label(frame_parameter_model, text="Temperature",justify="left", background="#383535", foreground="white", font=("Khmer", 20))
                label_temperature.place(x=5, y=240)
                tip_temperature = Hovertip(label_temperature,' affecte le caractère aléatoire du model \n (plus c\'est petit, plus c\'est prévisible, plus c\'est grand, plus c\'est imprévisible)')

                ## Parameters : temperature

                value4 = StringVar()
                value4.set(self.get_specific_param("temperature"))
                text_temperature = Entry(frame_parameter_model, textvariable=value4, width=10)
                text_temperature.place(x=240, y=250)

                ## Parameters : top_k

                label_top_k = Label(frame_parameter_model, text="Top K",justify="left", background="#383535", foreground="white", font=("Khmer", 20))
                label_top_k.place(x=5, y=285)
                tip_top_k = Hovertip(label_top_k,'nombre de mots à considérer pour la génération')

                value5 = StringVar()
                value5.set(self.get_specific_param("top_k"))
                text_top_k = Entry(frame_parameter_model, textvariable=value5, width=10)
                text_top_k.place(x=240, y=295)

                ## Parameters : num_beams

                label_number_of_beam = Label(frame_parameter_model, text="Number of Beam",justify="left", background="#383535", foreground="white", font=("Khmer", 20))
                label_number_of_beam.place(x=5, y=330)
                tip_number_of_beam = Hovertip(label_number_of_beam,'nombre de beam pour la génération')

                value6 = StringVar()
                value6.set(self.get_specific_param("num_beams"))
                text_number_of_beam = Entry(frame_parameter_model, textvariable=value6, width=10)
                text_number_of_beam.place(x=240, y=340)

                text_context.bind("<KeyRelease>", test_is_alpha)
                self.user_input_global.bind("<KeyRelease>", test_is_alpha)
                text_temperature.bind("<KeyRelease>", test_is_float)
                text_top_k.bind("<KeyRelease>", test_is_num)
                text_max_length.bind("<KeyRelease>", test_is_num)
                text_number_of_beam.bind("<KeyRelease>", test_is_num)
                text_repetition_penalty.bind("<KeyRelease>", test_is_float)
                text_returned_sequence.bind("<KeyRelease>", test_is_num)

                ## Button to apply the parameters
                button_apply_parameters = Button(inner_frame_left, background="#383535", foreground="white", text="Apply Parameters & model", font=("Khmer", 15), command=lambda: self.update_parameters())
                button_apply_parameters.pack(side=TOP, pady=20)

                ## Dictionary with the initial parameters
                self.parameters_entry_list = {"selected_model":list_model,
                                            "temperature":text_temperature,
                                            "num_beams":text_number_of_beam,
                                            "repetition_penalty":text_repetition_penalty,
                                            "num_return_sequences":text_returned_sequence,
                                            "top_k":text_top_k,
                                            "max_length":text_max_length}


                # Add a semi-transparent black frame for the future dialog
                canva_visualiser.create_rectangle(
                    0, canva_visualiser.winfo_height() - 30, canva_visualiser.winfo_width(), canva_visualiser.winfo_height(),
                    fill="black", stipple="gray75", outline="", tags="dialog_frame"
                )
                canva_visualiser.tag_lower("dialog_frame")  # Ensure it stays at the bottom layer
                canva_visualiser.bind("<Configure>", lambda _: canva_visualiser.coords(
                    "dialog_frame", 0, 350, canva_visualiser.winfo_width(), 430))  # Dynamically adjust width on resize
                canva_visualiser.tag_raise("dialog_frame")  # Ensure it stays on top of everything

                # Function to ensure the dialog frame always stays on top
                def ensure_dialog_frame_on_top():
                    self.canvas_visualiser.tag_raise("dialog_frame")

                ## Create the first object of the tree
                first_obj = DialogObject()
                first_obj.set_observer(self)
                first_obj.set_character(Character("Willy Wonka"))
                first_obj.set_img("Willy Beans")
                first_obj.set_text("I hate cappuccino")
                first_obj.set_model_controller(self.model_controller)

                first_obj.build_tree(self.canvas)
                self.first_obj = first_obj
                self.model_controller.set_current_window(window) # set the current window to the model controller

                ## Button to generate with the model (and create the tree)
                buttonGenerate = Button(self.window , text="Generate" , background="#383535" , foreground="white" , font=("Khmer" , 15) , command=lambda: self.generate())
                buttonGenerate.pack(side=BOTTOM)

                self.button_generate = buttonGenerate

                nb_obj = 10
                self.canvas.configure(scrollregion=(0, 0, 120*nb_obj, 2000))


                # Fill the frame_image

                label_charachters = Label(inner_frame_right, text="Characters", background="#383535", foreground="white", font=("Khmer", 25))
                label_charachters.pack(pady=10)

                frame_characters = Frame(inner_frame_right, bg="#383535")
                frame_characters.pack(pady=10)

                label_backgrounds = Label(inner_frame_right, text="Backgrounds", background="#383535", foreground="white", font=("Khmer", 25))
                label_backgrounds.pack(pady=10)

                frame_backgrounds = Frame(inner_frame_right, bg="#383535")
                frame_backgrounds.pack(pady=10)

                # Initialize character frames



                if self.project_name is None:
                    # Resize images
                    image_character1 = resize_image("images/moi.jpg", 199, 199)
                    image_character2 = resize_image("images/H4K3N.png", 199, 199)
                    image_character3 = resize_image("images/LGBTeam-Rebirth-v1.png", 199, 199)
                    image_character4 = resize_image("images/haken.png", 199, 199)

                    image_background = resize_image("images/background/town.jpg", 199, 199)
                    image_background2 = resize_image("images/background/forest.jpg", 199, 199)
                    image_background3 = resize_image("images/background/dark_street.jpg", 199, 199)
                    image_background4 = resize_image("images/background/bedroom.jpg", 199, 199)

                    # Character Buttons (inside frames)
                    self.character_wrappers = []
                    character_data = [
                        ("images/moi.jpg", image_character1),
                        ("images/H4K3N.png", image_character2),
                        ("images/LGBTeam-Rebirth-v1.png", image_character3),
                        ("images/haken.png", image_character4),
                    ]

                    for i, (img_path, img) in enumerate(character_data):
                        wrapper = Frame(frame_characters, bg="#383535", padx=2, pady=2)
                        wrapper.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                        self.frame_character1 = wrapper if i == 0 else self.frame_character1
                        self.frame_character2 = wrapper if i == 1 else self.frame_character2
                        self.frame_character3 = wrapper if i == 2 else self.frame_character3
                        self.frame_character4 = wrapper if i == 3 else self.frame_character4

                        btn = Button(wrapper, image=img, bg="#383535", width=199, height=199,
                                    command=lambda w=wrapper, p=img_path: self.character_image_clicked(w, p, self.first_obj))
                        btn.image = img
                        btn.pack()
                        self.character_wrappers.append(wrapper)

                    # Background Buttons (inside frames)
                    # Background Buttons (inside frames)
                self.background_wrappers = []

                background_data = [
                    ("images/background/town.jpg", image_background),
                    ("images/background/forest.jpg", image_background2),
                    ("images/background/dark_street.jpg", image_background3),
                    ("images/background/bedroom.jpg", image_background4),
                ]

                for i, (img_path, img) in enumerate(background_data):
                    wrapper = Frame(frame_backgrounds, bg="#383535", padx=2, pady=2)
                    wrapper.grid(row=i // 2, column=i % 2, padx=5, pady=5)

                    btn = Button(wrapper, image=img, bg="#383535", width=199, height=199,
                                command=lambda w=wrapper, p=img_path: self.background_image_clicked(w, p))
                    btn.image = img
                    btn.pack()
                    self.background_wrappers.append(wrapper)


                if not torch.cuda.is_available():
                    error_handler(self.window , "CUDA not available, expect unhandled bugs")

                 # close the window properly
                self.window.protocol("WM_DELETE_WINDOW", lambda: self.quit_window())

                self.model_controller.update_reload()


        def set_state_left(self, frame_to_show):
            print("set_state called for:", "inner_frame_left" if frame_to_show == self.inner_frame_left else "character_creation")

            # Si on veut masquer une frame déjà affichée
            if (frame_to_show == self.inner_frame_left and self.frame_parameters_state) or \
            (frame_to_show == self.frame_character and self.frame_character_creation_state):

                frame_to_show.place_forget()
                if frame_to_show == self.inner_frame_left:
                    self.frame_parameters_state = False
                else:
                    self.frame_character_creation_state = False

                # Si aucune frame n’est affichée, on cache outer_frame_right visuellement (mais on ne fait pas pack_forget)
                if not self.frame_parameters_state and not self.frame_character_creation_state:
                    self.outer_frame_left.configure(width=0)
                    self.outer_frame_left_state = False
                return

            # Si outer_frame_left était caché (width=0), on le réaffiche
            if not self.outer_frame_left_state:
                print("Reactivating outer_frame_left")
                self.outer_frame_left.configure(width=410)
                self.outer_frame_left_state = True

            # Masquer toutes les frames enfants
            self.inner_frame_left.place_forget()
            self.frame_character.place_forget()
            self.frame_parameters_state = False
            self.frame_character_creation_state = False

            # Afficher la bonne
            frame_to_show.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame_to_show.update_idletasks()

            # Mettre à jour l’état
            if frame_to_show == self.inner_frame_left:
                self.frame_parameters_state = True
            else:
                self.frame_character_creation_state = True

            print("Frame visibility -> parameters:", self.inner_frame_left.winfo_ismapped(),
                "| character_creation:", self.frame_character.winfo_ismapped(),
                "| outer_frame_left:", self.outer_frame_left.winfo_ismapped())


        def set_state_right(self, frame_to_show):
           if (self.frame_picture_state and self.outer_frame_right_state):
                self.frame_pictures.place_forget()
                self.outer_frame_right.configure(width=0)
                self.frame_picture_state = False
                self.outer_frame_right_state = False
                return
           else :
                self.frame_picture_state = True
                self.outer_frame_right_state = True
                self.outer_frame_right.pack(side=RIGHT, fill=Y, padx=20)
                self.outer_frame_right.configure(width=410)
                self.frame_pictures.place(relx=0, rely=0, relwidth=1, relheight=1)





        def update_buttons_image(self):
            if self.project_name:
                project_path = pathlib.Path("resources/renpy_project") / self.project_name / "game/images"
                if project_path.is_dir():
                    character_images = list(project_path.glob("*.png"))
                    if character_images:
                        for frame in [self.frame_character1, self.frame_character2, self.frame_character3, self.frame_character4]:
                            if frame:  # Ensure the frame is not None
                                for widget in frame.winfo_children():
                                    widget.destroy()
                                random_image_path = random.choice(character_images)
                                resized_image = resize_image(random_image_path, 199, 199)  # Use resize_image for resizing
                                button_image = Button(
                                    frame,
                                    image=resized_image,
                                    background="#383535",
                                    height=199,
                                    width=199,
                                    command=lambda f=frame, path=random_image_path: self.character_image_clicked(f, path, self.first_obj)  # Bind path
                                )
                                button_image.image = resized_image  # Prevent garbage collection
                                button_image.pack(side=LEFT)

        def update_project_name(self, event=None):
            if self.combobox_project:
                if self.combobox_project.get():
                    self.combobox_project.update()
                    self.project_name = self.combobox_project.get()
                    self.model_controller.set_current_project(self.project_name)
                    self.update_buttons_image()  # Update buttons image when project is updated
                else:
                    error_handler(self.window,"No project name")

        def quit_window(self):
            self.model_controller.flush_observers() # just in case
            quit()

        def generate_tree_with_ai(self):
            self.canvas.delete("all")  # Clean up the canvas before generating anything with AI
            count = self.output.count('\n')
            dialogue = self.output.split('\n')
            self.first_obj.destroy_self(self.canvas)
            obj_p = self.first_obj
            obj_p.set_character(Character("Character0"))
            if dialogue[0] != '' and dialogue[0] != "." and dialogue[0] != '."':
                obj_p.set_text(dialogue[0])
            else:
                obj_p.set_text(dialogue[1])

            for i in range(count):
                if i > 0:
                    if dialogue[i] != '' and dialogue[i] != "." and dialogue[i] != ".\"" and dialogue[i] != obj_p.get_text():  # If the line is not empty
                        obj = DialogObject()
                        obj.set_character("Character" + str(i))
                        obj.set_text(dialogue[i])
                        obj.set_parent(obj_p)
                        obj.build_tree(self.canvas)  # Add the DialogObject to the canvas
                        obj_p = obj
                        # Bind click event to the DialogObject widget
                        if obj.widget:
                            obj.widget.bind("<Button-1>", lambda _: self.dialog_object_clicked(obj))
                            print(f"Event bound to DialogObject: {obj}")  # Debug print to confirm event binding
            obj_p.build_tree(self.canvas)

        def change_processing_type(self):
            self.model_controller.change_processing_method()
        def obs_update_processing_type(self,processing_type):
            if self.processing_type_button is not None:
                self.processing_type_button.config(text="Processing-Mode  :" +processing_type+"")
        def update_gen_type(self):
            if self.generation_type == GenerationType.TEXT:
                self.model_controller.set_generation_type(GenerationType.IMAGE)
                self.generation_type = GenerationType.IMAGE
                self.gen_type_label.config(text="Generation-Mode : Image  ")
            else:
                self.model_controller.set_generation_type(GenerationType.TEXT)
                self.generation_type = GenerationType.TEXT
                self.gen_type_label.config(text="Generation-Mode : Text     ")

        def obs_update_models_list(self, model_list):
            self.parameters_entry_list["selected_model"].configure(values=model_list)


        def generate(self):
            self.update_prompt()
            self.prompt = str(self.context) + " \n " + str(self.prompt)
            print(self.prompt)
            self.model_controller.generate(self.prompt)
            self.button_generate.configure(text="Regenerate") # change the button text to regenerate


        def save_image(self):
            base_path = "resources/images/"
            file_name = "generated_img"
            if not self.image_cache is None:
                img = ImageTk.getimage(self.image_cache) # get the actual image
                nb = 1
                if Path(base_path).is_dir():    # if the directory exist, do
                    while Path(base_path + file_name + str(nb) + ".png").is_file():
                        nb+=1
                    img.save(base_path + file_name + str(nb) + ".png", "PNG")
                    showinfo("Saved", "Image saved at : "+base_path)
            else:
                error_handler(self.window ,"No image to save")

        def unload_model(self):
            self.model_controller.turn_off_model()


        def update_output(self,message):
            if 'error' in message[0]:
                error_handler(self.window , message[0]['error'])
            else:
                self.output = message[0]['generated_text']
                if self.nb_opened_window==1: # if only the main window is opened
                    self.generate_tree_with_ai()


        def update_prompt(self):
            self.prompt = self.user_input_global.get()
            self.prompt_label_global.config(text=self.prompt)

        def update_parameters(self):
            for index in self.parameters_entry_list.keys():
                if index == "selected_model":
                    selected_model = self.parameters_entry_list.get(index).get()
                    if selected_model:
                        self.parameters.update({"selected_model": selected_model})
                        change_validate(self.window, "Model " + selected_model + " selected")
                    if selected_model == "":
                        error_handler(self.window, "No model selected")
                        return
                    else:
                        self.parameters.update({"selected_model": self.get_specific_param("selected_model")})
                else:
                    try:
                        value = float(self.parameters_entry_list.get(index).get())
                        self.parameters.update({index: value})
                    except ValueError:
                        error_handler(self.window, f"Parameter {index} is not a valid number")
                        return

            self.model_controller.update_parameters(self.parameters)
        def obs_update_parameters(self,data):
            self.parameters = data

        def obs_update_current_model(self, current_model):
            if self.model_label is not None:
                self.model_label.config(text=current_model)

        def get_specific_param(self,param):
            return self.parameters[param]
        def switch(self):
            if self.button_generate["state"] == "normal":
                self.button_generate["state"] = "disabled"
            else:
                self.button_generate["state"] = "normal"

        def generate_text(self):
            self.canvas_visualiser.delete("dialog_frame")  # Clear dialog
            base_path = "resources/renpy_project/"+self.project_name+"/game/" # TODO : With the project selection combobox
            # Init fileWriter
            file_writer = HomeMadeFileWriter()
            file_writer.set_mode("w")
            file_writer.set_file(base_path+"script.rpy")

            # Gather information on tree
            tree_information = self.first_obj.get_tree_information()

            # Init ObjConverter
            obj_converter = ObjToScriptConverter()
            obj_converter.set_label_list(tree_information["labels"])
            obj_converter.set_characters_list(tree_information["characters"])

            # Convert and write to file
            file_writer.write(obj_converter.convert())
            change_validate(self.window,"Script generated at : "+base_path)

        def character_image_clicked(self, wrapper, image_path, dialog_object):
            # Reset previous selection
            self.canvas_visualiser.delete("dialog_frame")  # Clear dialog
            if hasattr(self, 'choosed_character') and self.choosed_character:
                self.choosed_character.configure(bg="#383535")

            # Highlight new selection
            self.choosed_character = wrapper
            wrapper.configure(bg="yellow")

            # Show character on top of the background
            resized_image = resize_image(image_path, 300, 450)  # Resize character image to a bigger size
            self.canvas_visualiser.delete("character")  # Clear previous character
            self.canvas_visualiser.create_image(450, 450, image=resized_image, anchor=S, tags="character")  # Add character at the bottom center
            self.canvas_visualiser.character_image = resized_image  # Prevent garbage collection
            self.canvas_visualiser.character_image_path = image_path

            # Update DialogObject with the selected image
            dialog_object.set_img(image_path)

            # Ensure dialog frame stays on top
            self.canvas_visualiser.tag_raise("dialog_frame")

            print(f"Character image clicked: {image_path}")
        def display_show_obj(self, obj_name : str, data_type : str):
            # in case there's an error, init with existing images


            tag_type = "background"
            image_path = "images/LGBTeam-Rebirth-v1.png"
            base_path = ""
            if self.project_name:
                base_path = "resources/renpy_project/"+self.project_name+"/game/"
            if data_type.__eq__("character"):
                tag_type = "character"
                image_path = base_path + "images/" + obj_name + ".png"
            elif data_type.__eq__("background"):
                image_path = base_path + "images/background/" + obj_name + ".jpg"

            if not os.path.isfile(image_path):
                print("ERROR IN display_show_obj : no such "+data_type+" image : "+image_path)
                if data_type.__eq__("character"):
                    image_path = "resources/images/angry.png"
                else:
                    image_path = "images/background/forest.jpg"

            # Show character on top of the background

            self.canvas_visualiser.delete(tag_type)  # Clear previous image
            if data_type.__eq__("character"):
                resized_image = resize_image(image_path, 300, 450)  # Resize character image to a bigger size

                self.canvas_visualiser.create_image(450, 450, image=resized_image, anchor=S,tags="character")  # Add character at the bottom center
                self.canvas_visualiser.character_image = resized_image  # Prevent garbage collection
                self.canvas_visualiser.character_image_path = image_path
            else:
                resized_image = resize_image(image_path, 900, 450)  # Resize character image to a bigger size
                self.canvas_visualiser.create_image(0, 0, image=resized_image, anchor=NW,tags="background")  # Add background
                self.canvas_visualiser.image = resized_image  # Prevent garbage collection
                self.canvas_visualiser.image_path = image_path

            # Ensure dialog frame stays on top
            self.canvas_visualiser.tag_raise("dialog_frame")
            # self.canvas_visualiser.tag_raise("character")
        def display_show_dialog(self, dialog : str):
            ratio = 1.2*len(dialog)/17 # shitty ratio
            print("RATIO : "+str(ratio))
            if ratio < 0.9:
                ratio = 1.0
            self.canvas_visualiser.delete("dialog_frame")  # Clear previous image
            self.canvas_visualiser.create_rectangle(0,250,900,350,outline="black",fill="white")
            self.canvas_visualiser.create_text(450, 285, tags="dialog_frame", text=dialog, fill="black",font=("Khmer", 20), justify="center")
            #self.canvas_visualiser.tag_raise("dialog_frame")

        def background_image_clicked(self, wrapper, image_path):
            # Reset previous selection
            if hasattr(self, 'choosed_character') and self.choosed_character:
                self.choosed_character.configure(bg="#383535")

            # Highlight new selection
            self.choosed_character = wrapper
            wrapper.configure(bg="yellow")

            # Show background on canvas
            self.canvas_visualiser.delete("background")  # Clear previous background
            resized_image = resize_image(image_path, 900, 450)  # Resize to fit canvas dimensions
            self.canvas_visualiser.create_image(0, 0, image=resized_image, anchor=NW, tags="background")  # Add background
            self.canvas_visualiser.image = resized_image  # Prevent garbage collection
            self.canvas_visualiser.image_path = image_path

            # Ensure dialog frame stays on top
            self.canvas_visualiser.tag_raise("dialog_frame")

            print(f"Background image clicked: {image_path}")

        def dialog_object_clicked(self, dialog_object):
            """Handle click on a DialogObject."""
            print(f"DialogObject clicked: {dialog_object}")  # Debug print to check if the event is called
            if self.choosed_character:
                self.choosed_character.configure(highlightbackground="#383535", highlightthickness=0)
            self.choosed_character = dialog_object.widget  # Use the widget for highlighting
            self.choosed_character.configure(highlightbackground="yellow", highlightthickness=2)

            # Display the corresponding dialog in the canvas
            self.canvas_visualiser.delete("all")  # Clear previous content
            dialog_text = dialog_object.get_text()  # Get the dialog text
            self.canvas_visualiser.create_text(450, 225, text=dialog_text, fill="white", font=("Khmer", 15), justify="center")

            print(f"Dialog text displayed: {dialog_text}")

        def update(self,subject,data_type,data) -> None:
            """
            Receive update from subject.
            """

            # Determine the type of update given
            match data_type:
                case "output":
                    self.update_output(data)
                case "model_list":
                    self.obs_update_models_list(data)
                case "current_model":
                    self.obs_update_current_model(data)
                case "parameters":
                    self.obs_update_parameters(data)
                case "reload":
                    self.obs_update_models_list(data["model_list"])
                    self.obs_update_current_model(data["current_model"])
                    self.obs_update_processing_type(data["processing_type"])
                    self.obs_update_parameters(data["parameters"])
                case "can_generate":
                    self.nb_opened_window = data
                case "broadcast":
                    if data["type"]=="error":
                        error_handler(self.window,data["message"])
                    else:
                        change_validate(self.window,data["message"])
                case _:
                    print("ERROR : COULDN'T READ SUBJECT DATA")
            pass
        def update_doo(self,subject,data_type,data) -> None:
            """
            Receive update from subject.
            """
            match data_type:
                case "kill_dialog_object":
                    # remove dialog_object from the tag list
                    if data in self.dialog_object_tag_list:
                        self.dialog_object_tag_list.remove(data)
                        destroy_dialog_object(self.canvas,data)
                        if data is self.selected_dialog_object:
                            self.selected_dialog_object = None
                    else:
                        print("ERROR : WHAT IS DEAD MAY NEVER DIE IN update_doo")
                case "delete_choices":
                    # remove all choices
                    destroy_choices(self.canvas,data)
                case "update_dialog_object_character_name":
                    if data[0] in self.dialog_object_tag_list: # if the dialog_object is already drawn or not
                        update_dialog_object_name(self.canvas,data[0],data[1])
                case "add_dialog_object":
                    # add dialog_object to the tag list
                    self.dialog_object_tag_list.append(data)
                case "click_on_dialog_object":
                    # check if current dialog object is selected or not
                    if self.selected_dialog_object != data:
                        # change last dialog object
                        if self.selected_dialog_object and self.selected_dialog_object in self.dialog_object_tag_list:
                            on_click_change_dialog_object(self.canvas,self.selected_dialog_object, "black")
                        self.selected_dialog_object = data
                        on_click_change_dialog_object(self.canvas,self.selected_dialog_object,"yellow")
                case "flush_all_dialog_objects":
                    # get rid of the dialog_object tag list
                    self.dialog_object_tag_list.clear()
                    self.selected_dialog_object = None
                case "display_dialog":
                    # 0 : character name
                    # 1 : dialog
                    # 2 : background
                    print(data[0] + "|"+data[1]+"|"+data[2])
                    self.display_show_obj(data[2], "background")
                    self.display_show_obj(data[0],"character")
                    self.display_show_dialog(data[1])


                case _:
                    print("ERROR : COULDN'T READ SUBJECT DATA IN update_doo")
            pass

        def add_image_to_character(self):
            """Add an image to the selected character and expression."""
            if self.character_instance:
                selected_expression = self.expression_var.get()
                if not selected_expression:
                    selected_expression = ""  # Default to an empty expression if none is selected

                # Open file dialog to select an image
                from tkinter.filedialog import askopenfilename
                image_path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                if not image_path:
                    error_handler(self.window, "No image selected.")
                    return

                # Ensure a project is selected
                if not self.project_name:
                    error_handler(self.window, "No project selected. Please select a project.")
                    return

                # Define the target path
                project_path = pathlib.Path(f"resources/renpy_project/{self.project_name}/game/images")
                project_path.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
                target_filename = ""
                if selected_expression.__eq__(""):
                    target_filename = f"{self.character_instance.get_name()}.png"
                else:
                    target_filename = f"{self.character_instance.get_name()} {selected_expression}.png"
                target_path = project_path / target_filename

                # Save the image to the target path
                from shutil import copyfile
                copyfile(image_path, target_path)

                # Update the character's expression image mapping
                change_validate(self.window, f"Image saved for character '{self.character_instance.get_name()}' with expression '{selected_expression}'.")
            else:
                error_handler(self.window, "No character selected. Please select or create a character.")