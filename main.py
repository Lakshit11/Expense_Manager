import csv
import json
from datetime import datetime

import pandas as pd
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy_garden.graph import Graph, MeshLinePlot

CSV_FILE = "data.csv"


def make_plot(amt):
    x = list(range(1, 8)) 

    graph = Graph(
        xlabel="Date",
        ylabel="Amount",
        x_ticks_minor=5,
        x_ticks_major=1,
        y_ticks_major=100,
        y_grid_label=True,
        x_grid_label=False,
        padding=5,
        x_grid=True,
        y_grid=True,
        xmin=0,
        xmax=8,
        ymin=0,
        ymax=2000,
    )

    plot = MeshLinePlot(color=[1, 0, 0, 1])
    plot.points = [(i, j) for i, j in zip(x, amt)]
    graph.add_plot(plot)

    return graph


def make_dates():
    today = datetime.today()
    return str(today.month) + "/" + str(today.day)


class Home(Screen):
    def signin(self, uname, p1):
        users = self.manager.get_users()

        if uname in users and users[uname]["password"] == p1:
            self.manager.transition.direction = "left"
            self.manager.current = "Submit_Screen"
            self.ids.quote.text = "Enter Your Username And Password to Login OR Create New Account using Sign Up Button"
            self.ids.username.text = ""
            self.ids.password.text = ""
        else:
            self.ids.quote.text = "Please Enter Valid Details"
            self.ids.username.text = ""
            self.ids.password.text = ""

    def next(self):
        self.manager.transition.direction = "left"
        self.manager.current = "SignUp_Screen"
        self.ids.quote.text = "Enter Your Username And Password to Login OR Create New Account using Sign Up Button"

    def fg(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Forgot_Screen"
        self.ids.quote.text = "Enter Your Username And Password to Login OR Create New Account using Sign Up Button"



class SignUpScreen(Screen):
    def adduser(self, uname, p1, p2):
        users = self.manager.get_users()
        if p1 == p2:
            if uname in users:
                self.ids.same.text = "User Already Exists!! Pleaase try different Username"
                self.ids.password1.text=""
                self.ids.password2.text=""
            else:
                users[uname] = {"username": uname, "password": p1, "created": make_dates()}
                self.manager.update_users(users)
                self.manager.transition.direction = "right"
                self.manager.current = "Home_Screen"
                self.ids.same.text = "Enter Username And Password Below"
                self.ids.name.text = ""
                self.ids.password1.text = ""
                self.ids.password2.text = ""
        else:
            
            self.ids.same.text = "Please Enter Same Password"
            self.ids.password1.text = ""
            self.ids.password2.text = ""
    
    def goback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.same.text = "Enter Username And Password Below"
        self.ids.name.text = ""
        self.ids.password1.text = ""
        self.ids.password2.text = ""

class ForgotScreen(Screen):
    def forgot(self, uname, p1, p2):
        if p1 == p2:
            users = self.manager.get_users()
            if uname in users:
                users[uname] = {
                    "username": uname,
                    "password": p1,
                    "Password Updated": make_dates(),
                }
                self.manager.update_users(users)
                self.ids.lbf.text = "Password Updated Successfully"
                self.manager.transition.direction = "left"
                self.manager.current = "Home_Screen"
                self.ids.lbf.text = "Enter Username and New Password"
                self.ids.fgname.text = ""
                self.ids.newp.text = ""
                self.ids.confirm.text = ""
            else:
                self.ids.lbf.text = "User does not Exist!! Please Enter Existing Username"
                self.ids.newp.text = ""
                self.ids.confirm.text = ""
        else:
            self.ids.lbf.text = "Please Enter Same Password"
            self.ids.newp.text = ""
            self.ids.confirm.text = ""

    def goback(self):
        self.ids.lbf.text = "Enter Username and New Password"
        self.manager.transition.direction = "left"
        self.manager.current = "Home_Screen"
        self.ids.fgname.text = ""
        self.ids.newp.text = ""
        self.ids.confirm.text = ""


class AddExpense(Screen):
    def goback(self):
        self.ids.expen.text = "Add your Expense Below"
        self.manager.transition.direction = "right"
        self.manager.current = "Submit_Screen"
        self.ids.comment.text = ""
        self.ids.amount.text = ""

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.expen.text = "Add your Expense Below"
        self.ids.comment.text = ""
        self.ids.amount.text = ""

    def addexpense(self, expense, comm):
        expense = int(expense)
        now = datetime.now().time()
        if (True):
            with open(CSV_FILE, "a+", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([str(make_dates()), expense, comm])
        self.ids.expen.text = "Expense Added Successfully"
        self.ids.comment.text = ""
        self.ids.amount.text = ""


class SubmitScreen(Screen):
    def goback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.submitex.text = "Click to Add Money or View or Contribute"

    def contribute(self):
        self.manager.transition.direction = "left"
        self.manager.current = "Contribute_Screen"

    def addex(self):
        self.manager.transition.direction = "left"
        self.manager.current = "Add_Expense"

    def gra(self):
        self.manager.transition.direction = "left"
        self.manager.current = "View_Screen"
     
    def clearData(self):
        self.manager.transition.direction = "left"
        self.manager.current = "Clear_Screen"

class ContributeScreen(Screen):
    def goback(self):
        self.ids.contri.text = "Enter The Amount And Number of People Below"
        self.manager.transition.direction = "right"
        self.manager.current = "Submit_Screen"
        self.ids.amount.text = ""
        self.ids.people.text = ""

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.contri.text = "Enter The Amount And Number of People Below"
        self.ids.amount.text = ""
        self.ids.people.text = ""

    def calculate(self, amount, people):
        value = int(amount) / int(people)
        self.ids.contri.text = "The contributed Amount for {one} people is {two} rupees\n The expense will automatically be added accordingly".format(one=people, two=int(value))

        with open(CSV_FILE, "a+", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([make_dates(), int(value),"Contribution"])
        self.ids.amount.text = ""
        self.ids.people.text = ""

class ViewScreen(Screen):
    def goback(self):
        self.ids.quote.text = " Select How you want to View Data"
        self.manager.transition.direction = "right"
        self.manager.current = "Submit_Screen"

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.quote.text = "Select How you want to View Data"
    
    def viewdata(self):
        df = pd.read_csv(CSV_FILE)
        df1 = df.groupby("Date").sum()
        var = df1.to_string(index=True)
        self.ids.quote.text = "Your total expense on date is : \n" + "  " + str(var)
    
    def viewgraph(self):
        view = ModalView(size_hint=(0.90, 0.90))
        df = pd.read_csv(CSV_FILE)
        df1 = df.groupby("Date").sum().reset_index().tail(7)
        self.tickers_on_plot = ["Amount"]
        self.amount = df1["Amount"]
        gr = make_plot(self.amount)
        view.add_widget(gr, canvas="Red")
        view.open()

    def viewcomments(self):
        self.ids.quote.text = "Select How you want to View Data"
        self.manager.transition.direction = "left"
        self.manager.current = "Comment_Screen"

class CommentScreen(Screen):
    def goback(self):
        self.ids.quote.text = "Enter Date for which you want Data"
        self.manager.transition.direction = "right"
        self.manager.current = "View_Screen"
        self.ids.date.text = ""

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.quote.text = "Enter Date for which you want Data"
        self.ids.date.text = ""

    def viewcomments(self,date):
        df = pd.read_csv(CSV_FILE)
        if date in list(df['Date']):
            df1 = df[df['Date'] == date]
            var = df1.to_string(index = False)
            self.ids.quote.text = "The Expenses for the date {} is: \n".format(date) + str(var)
            self.ids.date.text = ""
        else:
            self.ids.quote.text = "The Expenses for the date {} does not exist \n Please re-check the date provided".format(date)

class ClearScreen(Screen):
    def goback(self):
        self.ids.cleardata.text = "Are you sure you want to clear data?"
        self.manager.transition.direction = "right"
        self.manager.current = "Submit_Screen"
        self.ids.usid.text = ""
        self.ids.pid.text = ""

    def home(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Home_Screen"
        self.ids.cleardata.text = "Are you sure you want to clear data?"
        self.ids.usid.text = ""
        self.ids.pid.text = ""
    
    def clear(self, uname, pss):
        
        users = self.manager.get_users()

        if uname in users and users[uname]["password"] == pss:
            with open(CSV_FILE,'r+') as file:
                file.readline()
                file.truncate(file.tell())
            self.ids.cleardata.text = "Data Cleared Successfully!!"
            self.ids.usid.text = ""
            self.ids.pid.text = ""
        else:
            self.ids.cleardata.text = "Please Enter Valid Details"
            self.ids.pid.text = ""

class RootWidget(ScreenManager):
    def get_users(self):
        with open("users.json") as file:
            return json.load(file)

    def update_users(self, data):
        with open("users.json", "w") as file:
            json.dump(data, file, indent=4)


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

    def build(self):
        self.icon = 'icon.png'
        self.title = 'Expense Manager'
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
