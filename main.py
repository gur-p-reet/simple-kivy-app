import kivy
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import json,glob, random
from datetime import datetime
from pathlib import Path


Builder.load_file('my.kv')

class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction='left'
        self.manager.current="sign_up_screen"
    def login(self, uname, pword):
        self.manager.transition.direction='left'
        with open('users.json', 'r') as file:
            users=json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current='login_screen_success'
        else:
            self.ids.wrong_login.text="Wrong username or password"

class RootWidget(ScreenManager):
    
    pass

class SignUpScreen(Screen):
    
    def add_user(self, uname,pword):
        self.manager.transition.direction='left'
        with open("users.json") as file:
            users=json.load(file)
        
        users[uname]={'username':uname, 'password':pword,
                  'created':datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}
        with open('users.json','w') as file:
            json.dump(users,file)
        self.manager.current='sign_up_screen_success'

class SignUpScreenSucess(Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"


    
class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"      
        
    def get_quote(self,feel):
        feel=feel.lower()
        available_fellings=glob.glob("quotes/*.txt")
        
        available_fellings=[Path(filename).stem for filename in available_fellings]
        
        if feel in available_fellings:
            with open(f"quotes/{feel}.txt", encoding='UTF-8') as file:
                quotes=file.readlines()
            self.ids.quotes.text=random.choice(quotes)
        else:
            self.ids.quotes.text="Try another feeling"
                


class MyApp(App):
    def build(self):
               
        return RootWidget()

if __name__=="__main__":
    MyApp().run()
