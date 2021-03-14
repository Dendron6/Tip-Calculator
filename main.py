from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def main():
    root = Tk()
    gui = Calc(root)
    gui.root.mainloop()
    return None


class Calc:
    def __init__(self, root):
        self.root = root
        self.root.title("Tip Calculator")
        self.root.geometry("790x620")
        self.root.iconbitmap("pizzaico.ico")
        #self.img = Tk.Image("photo", file="pizzaico.ico")
        # values
        self.tips = 0
        self.avg_deliveries = 0
        self.hourly_pay = 0
        self.mileage_pay = 0
        self.miles_driven = 0
        self.delivery_pay = 0
        self.days_work = 1
        self.hours_work = 1

        # Frame_fields to hold elements in places
        entry_field = LabelFrame(self.root, padx=5, pady=5)
        entry_field.grid(row=1, column=1, padx=10, pady=10)
        self.button_field = LabelFrame(self.root, padx=5, pady=5)
        self.button_field.grid(row=2, column=1, padx=10, pady=10)
        self.plot_year_field = LabelFrame(self.root, padx=5, pady=5)
        self.plot_year_field.grid(row=1, column=2, padx=10, pady=10)

        # tips
        Label(entry_field, text="Average Tip").grid(row=1, column=0)
        self.tips_entry = Entry(entry_field)
        self.tips_entry.grid(row=2, column=0)

        # Avg deliveries
        Label(entry_field, text="Average Deliveries per Day").grid(row=3, column=0)
        self.avg_deliveries_entry = Entry(entry_field)
        self.avg_deliveries_entry.grid(row=4, column=0)

        # Mileage driven
        Label(entry_field, text="Average Miles Driven per Day").grid(row=5, column=0)
        self.miles_driven_entry = Entry(entry_field)
        self.miles_driven_entry.grid(row=6, column=0)

        # Mileage Pay
        Label(entry_field, text="Pay per Mile driven").grid(row=7, column=0)
        self.mileage_pay_entry = Entry(entry_field)
        self.mileage_pay_entry.grid(row=8, column=0)

        # Hourly Pay
        Label(entry_field, text="Your Hourly Pay Rate").grid(row=9, column=0)
        self.hourly_pay_entry = Entry(entry_field)
        self.hourly_pay_entry.grid(row=10, column=0)

        # Days at work
        Label(entry_field, text="How many days per Week do you work?").grid(row=11, column=0)
        self.days_work_entry = Scale(entry_field, from_=1, to=7, orient=HORIZONTAL)
        self.days_work_entry.grid(row=12, column=0)

        # Hours per Day
        Label(entry_field, text="How many hours per day do you work?").grid(row=13, column=0)
        self.hours_work_entry = Scale(entry_field, from_=1, to=24, orient=HORIZONTAL)
        self.hours_work_entry.grid(row=14, column=0)

        # Delivery pay
        Label(entry_field, text="Payment per Single Delivery\n\t*if applicable").grid(row=15, column=0)
        self.delivery_pay_entry = Entry(entry_field)
        self.delivery_pay_entry.grid(row=16, column=0)

        # buttons
        yearly = Button(self.button_field, text="Calculate Income", command=self.Total, width=30)
        yearly.grid(row=1, column=1, columnspan=2)
        self.root.bind("<Return>", self.Total)
        clear = Button(self.button_field, text="Clear", command=self.Clear, width=30)
        clear.grid(row=7, column=1, columnspan=2)
        self.root.bind("<Return>", self.calcInc)

    # so this could be a pre calculation function, that makes new variables
    # and that in later funcitons we multiply these variable by 30 and by 365 for days
    def Total(self):
        self.calcInc()
        self.yearly_label = Label(self.button_field,
                                  text=f"This is Yearly Income: {round(self.total_income * self.days_work * 52, 2)}$")
        self.yearly_label.grid(row=2, column=1)

        self.monthly_label = Label(self.button_field,
                                   text=f"This is Monthly Income: {round(self.total_income * self.days_work * 4.2, 2)}$")
        self.monthly_label.grid(row=3, column=1)

        self.weekly_label = Label(self.button_field,
                                  text=f"This is Weekly Income: {round(self.total_income * self.days_work, 2)}$")
        self.weekly_label.grid(row=4, column=1)
        self.plot_pie()

    def calcInc(self, event=None):
        # tips
        if len(self.tips_entry.get()) == 0:
            self.tips = 0
        else:
            self.tips = float(self.tips_entry.get())
        # amount of deliveries
        if len(self.avg_deliveries_entry.get()) == 0:
            self.avg_deliveries = 0
        else:
            self.avg_deliveries = float(self.avg_deliveries_entry.get())

        # avg miles driven
        if len(self.miles_driven_entry.get()) == 0:
            self.miles_driven = 0
        else:
            self.miles_driven = float(self.miles_driven_entry.get())
        # mileage pay
        if len(self.mileage_pay_entry.get()) == 0:
            self.mileage_pay = 0
        else:
            self.mileage_pay = float(self.mileage_pay_entry.get())

        # hourly rate
        if len(self.hourly_pay_entry.get()) == 0:
            self.hourly_pay = 0
        else:
            self.hourly_pay = float(self.hourly_pay_entry.get())
        # days work
        self.days_work = int(self.days_work_entry.get())
        # hours work
        self.hours_work = int(self.hours_work_entry.get())

        # delivery pay
        if len(self.delivery_pay_entry.get()) == 0:
            self.delivery_pay = 0
        else:
            self.delivery_pay = float(self.delivery_pay_entry.get())

        # count totals to plot 4
        self.tip_per_day = self.tips * self.avg_deliveries
        self.miles_per_day = self.mileage_pay * self.miles_driven
        self.daily_wage = self.hourly_pay * self.hours_work
        self.delivery_pay_daily = self.delivery_pay * self.avg_deliveries

        # total income and individual percentage
        self.total_income = self.tip_per_day + self.miles_per_day + self.daily_wage + self.delivery_pay_daily
        if self.tip_per_day == 0:
            self.tips_interest = 0
        else:
            self.tips_interest = round((self.tip_per_day / self.total_income) * 100, 1)
        if self.miles_per_day == 0:
            self.miles_interest = 0
        else:
            self.miles_interest = round((self.miles_per_day / self.total_income * 100), 1)
        if self.daily_wage == 0:
            self.wage_interest = 0
        else:
            self.wage_interest = round((self.daily_wage / self.total_income) * 100, 1)
        if self.delivery_pay_daily == 0:
            self.delivery_interest = 0
        else:
            self.delivery_interest = round((self.delivery_pay_daily / self.total_income) * 100, 1)

    def plot_pie(self):
        # fig1, ax1 = plt.subplots()
        # sizes = [(self.tips_interest), (self.miles_interest), (self.wage_interest), (self.delivery_interest)]
        # explode = (0.1, 0, 0, 0)
        # ax1.pie(sizes, explode=explode, shadow=True, startangle=85, autopct='%1.1f%%')
        # ax1.axis("equal")
        # plt.title(f"Tips - {self.tips_interest}%, Mileage Pay - {self.miles_interest}%\nHourly Pay - {self.wage_interest}%, Delivery Pay - {self.delivery_interest}%")
        # plt.show()
        figure = Figure(figsize=(5, 4), dpi=100)
        subplot2 = figure.add_subplot(111)
        labels2 = 'Tips', 'Mileage Pay', 'Hourly Pay', 'Pay per Delivery'
        pieSizes = [(self.tips_interest), (self.miles_interest), (self.wage_interest), (self.delivery_interest)]
        my_colors2 = ['lightgreen', 'lightblue', 'silver', 'lightsteelblue']
        explode2 = (0.1, 0, 0, 0)
        subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=True,
                     startangle=90)
        subplot2.axis('equal')
        self.pie = FigureCanvasTkAgg(figure, self.root)
        self.pie.get_tk_widget().grid(row=1, column=2)

    # button that resets the values
    def Clear(self):
        self.tips_entry.delete(0, END)
        self.avg_deliveries_entry.delete(0, END)
        self.hourly_pay_entry.delete(0, END)
        self.mileage_pay_entry.delete(0, END)
        self.miles_driven_entry.delete(0, END)
        self.delivery_pay_entry.delete(0, END)
        self.days_work_entry.set(0)
        self.hours_work_entry.set(0)
        self.pie.get_tk_widget().grid_forget()


main()
