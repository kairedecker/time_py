import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation
from models import EnumDayType, Workday


class TimesGUI(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20,10))
        self.pack(fill=BOTH, expand=YES)
        print("Starting...")
        #self.name = ttk.StringVar(value="")
        #self.student_id = ttk.StringVar(value="")
        #self.course_name = ttk.StringVar(value="")
        #self.final_score = ttk.DoubleVar(value=0)
        self.start_time = ttk.StringVar(value="")
        self.stop_time = ttk.StringVar(value="")
        self.pause = ttk.StringVar(value="")
        self.date = ttk.StringVar(value="")
        #self.day_type = EnumDayType.OPEN
        self.data = []
        self.colors = master_window.style.colors

        instruction_text = "Please enter your contact information: " 
        instruction = ttk.Label(self, text=instruction_text, width=50)
        instruction.pack(fill=X, pady=10)

        self.start_time_input = self.create_form_entry("Start Zeit: ", self.start_time, type='time')
        self.stop_time_input = self.create_form_entry("Stop Zeit: ", self.stop_time, type='time')
        self.pause_input =  self.create_form_entry("Pause: ", self.pause, type='time')
        self.date_input = self.create_form_entry("Datum: ", type='date')
        self.day_type_input = self.create_form_entry("Typ: ", type='day_type')
        #self.final_score_input = self.create_form_entry("Final Score: ", self.final_score)
        #self.create_meter()
        self.create_buttonbox()

        self.table = self.create_table()

    
    def create_form_entry(self, label, variable=None, type=None):
        form_field_container = ttk.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)
        form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
        form_field_label.pack(side=LEFT, padx=12)
        form_input = ''
        print(form_input)
        match type:
            case 'time':
                form_input = ttk.Entry(master=form_field_container, textvariable=variable)
                form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)
                add_regex_validation(form_input, r'^(?:([01]?\d|2[0-3]):([0-5]?\d))?$')
            case 'date':
                form_input = ttk.DateEntry(master=form_field_container)
                form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)
            case 'day_type':
                form_input = ttk.Combobox(master=form_field_container, textvariable=variable)
                form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)
                day_type_list = []
                for day_type in EnumDayType:
                    day_type_list.append(day_type.value)
                    form_input['values'] = tuple(day_type_list)
            case _:
                form_input = ttk.Entry(master=form_field_container, textvariable=variable)
                form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)
                add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')

        return form_input
    
    def create_buttonbox(self):
        button_container = ttk.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        cancel_btn = ttk.Button(
            master=button_container,
            text="Exit",
            command=self.on_cancel,
            bootstyle=DANGER,
            width=8,
        )

        cancel_btn.pack(side=RIGHT, padx=5)

        submit_btn = ttk.Button(
            master=button_container,
            text="Speichern",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width=8,
        )

        submit_btn.pack(side=RIGHT, padx=5)
    '''
    def create_meter(self):
        meter = ttk.Meter(
            master=self,
            metersize=150,
            padding=5,
            amounttotal=100,
            amountused=50,
            metertype="full",
            subtext="Final Score",
            interactive=True,
        )

        meter.pack()

        self.final_score.set(meter.amountusedvar)
        self.final_score_input.configure(textvariable=meter.amountusedvar)
    
    '''
    
    
    def create_table(self):
        coldata = [
            {"text": "Datum"},
            {"text": "Start-Zeit", "stretch": False},
            {"text": "End-Zeit"},
            {"text": "Pause", "stretch": False},
            {"text": "Arbeitszeit", "stretch": False},
            {"text": "Fiori Eintrag"},
            {"text": "Typ"}
        ]

        print(self.data)

        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None),
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

    def on_submit(self):
        """Print the contents to console and return the values."""

        validator = self.start_time_input.validate() and self.stop_time_input.validate() and self.pause_input.validate()
        if(not validator):
            toast = ToastNotification(
                title="Submission failed!",
                message="Please provide data in correct format",
                duration=3000,
            )
            toast.show_toast()
            return None

        start_time = self.start_time.get()
        stop_time = self.stop_time.get()
        pause = self.pause.get()
        date = self.date_input.entry.get()
        day_type = self.day_type_input.get()

        toast = ToastNotification(
            title="Submission successful!",
            message="Your data has been successfully submitted.",
            duration=3000,
        )

        toast.show_toast()
        print(day_type)

        # Refresh table
        self.data.append((date, start_time, stop_time, pause, 'No', day_type))
        self.table.destroy()
        self.table = self.create_table()

    def on_cancel(self):
        """Cancel and close the application."""
        self.quit()


if __name__ == "__main__":

    app = ttk.Window("Manager of times", "superhero", resizable=(False, False))
    TimesGUI(app)
    app.mainloop()