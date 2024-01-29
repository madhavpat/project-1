from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
import requests

class MotorStartApp(App):
    def build(self):
        # Initialize status values
        self.status_values = ["0", "0", "0", "0"]

        # Create the main layout
        layout = BoxLayout(orientation='vertical', spacing=4)

        # Create a search input and button
        search_layout = BoxLayout(orientation='horizontal', spacing=4)
        self.search_input = TextInput(hint_text='Search', multiline=False)
        search_button = Button(text='Search', on_press=self.search_pressed)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_button)
        layout.add_widget(search_layout)

        # Create pump buttons
        pump_buttons_layout = BoxLayout(orientation='horizontal', spacing=10)
        for i in range(4):
            pump_layout = BoxLayout(orientation='vertical', spacing=10)
            pump_layout.add_widget(Image(source='https://upload.wikimedia.org/wikipedia/commons/f/f2/Ac-elektromotor-robuster-asynchronmotor.jpg', size=(150, 100)))
            pump_button = Button(text=f'Start', background_color=(1, 1, 0, 1), on_press=self.toggle_status)
            pump_button.index = i
            pump_layout.add_widget(pump_button)
            pump_layout.add_widget(Label(text=f'Pump No.{4-i}'))
            pump_buttons_layout.add_widget(pump_layout)

        layout.add_widget(pump_buttons_layout)

        # Create response label
        self.response_label = Label(text='')
        layout.add_widget(self.response_label)

        return layout

    def search_pressed(self, instance):
        search_text = self.search_input.text
        # Handle search logic here if needed
        print(f'Search pressed with text: {search_text}')

    def toggle_status(self, instance):
        index = instance.index
        self.status_values[index] = "0" if self.status_values[index] == "1" else "1"

        url = f"https://tpiams.shrotigroup.in/pump_status.php?imei=864180054092049&status={''.join(self.status_values)}"
        print(url)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.response_label.text = f'Response: {response.text}'
            else:
                self.response_label.text = f'Error: {response.status_code}'
        except Exception as e:
            self.response_label.text = f'Request Error: {e}'

if __name__ == '__main__':
    MotorStartApp().run()
