import random
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class HomeScreen(Screen):
    pass

class AkunScreen(Screen):
    pass

class ModeSelectionScreen(Screen):
    pass

class PengenalanBentukScreen(Screen):
    question_text = StringProperty("Ini Bentuk Apa:")
    choices = ListProperty(["Lingkaran", "Segitiga", "Persegi", "Persegi Panjang"])
    question_image = StringProperty() 
    current_level = 1  
    correct_answers = 0  
    level_data = {
        1: ["Persegi", "Lingkaran"], 
        2: ["Persegi", "Lingkaran", "Segitiga", "Persegi Panjang"],
        3: ["Persegi", "Lingkaran", "Segitiga", "Persegi Panjang", "Kubus", "Balok", "Prisma"]
    }
    
    all_shapes = ["Persegi", "Lingkaran", "Segitiga", "Persegi Panjang", "Kubus", "Balok", "Prisma"]

    def on_pre_enter(self):
        self.set_new_question()

    def set_new_question(self):
        available_shapes = self.level_data.get(self.current_level, [])

        if available_shapes:
            self.correct_answer = random.choice(available_shapes)
            self.question_image = f'assets/images/{self.correct_answer.lower().replace(" ", "_")}.png'
            self.question_text = f"Ini Bentuk Apa:\n"

        incorrect_choices = [shape for shape in self.all_shapes if shape != self.correct_answer]
        wrong_choices = random.sample(incorrect_choices, 3)

        all_choices = wrong_choices + [self.correct_answer]
        random.shuffle(all_choices)

        self.choices = all_choices  

    def check_answer(self, answer):
        if answer == self.correct_answer:
            self.correct_answers += 1
            self.question_text = "Benar! Ayo coba lagi!"
            self.play_sound('true')

            if self.correct_answers >= 3:
                self.correct_answers = 0  
                if self.current_level < 3: 
                    self.current_level += 1 
                    self.set_new_question() 
        else:
            self.question_text = "Salah! Coba lagi!"
            self.play_sound('false')

        Clock.schedule_once(self.reset_question, 2)

    def reset_question(self, dt):
        self.set_new_question()

    def play_sound(self, sound_name):
        sound = SoundLoader.load(f'assets/sounds/{sound_name}.mp3')
        if sound:
            sound.play()
        else:
            print(f"Sound {sound_name} not found!")

class HitungLuasScreen(Screen):
    selected_shape = StringProperty('')

    def on_shape_selected(self, value):
        self.selected_shape = value

class InputScreen(Screen):
    selected_shape = StringProperty('')  
    result_text = StringProperty('')     
    input_image = StringProperty('')  # Properti untuk menyimpan gambar

    def prepare_inputs(self, selected_shape):
        self.selected_shape = selected_shape
        self.result_text = ''
        self.input_image = f'assets/images/{selected_shape.lower().replace(" ", "_")}.png'  # Set gambar sesuai bentuk
        if selected_shape == 'Persegi':
            self.ids.input_label.text = "Masukkan sisi:"
            self.ids.input_field.hint_text = "Sisi"
        elif selected_shape == 'Lingkaran':
            self.ids.input_label.text = "Masukkan jari-jari:"
            self.ids.input_field.hint_text = "Jari-jari"
        elif selected_shape == 'Segitiga':
            self.ids.input_label.text = "Masukkan alas dan tinggi (pisahkan dengan koma):"
            self.ids.input_field.hint_text = "Alas, Tinggi"
        elif selected_shape == 'Persegi Panjang':
            self.ids.input_label.text = "Masukkan panjang dan lebar (pisahkan dengan koma):"
            self.ids.input_field.hint_text = "Panjang, Lebar"
        elif selected_shape == 'Kubus':
            self.ids.input_label.text = "Masukkan panjang sisi:"
            self.ids.input_field.hint_text = "Sisi"
        elif selected_shape == 'Balok':
            self.ids.input_label.text = "Masukkan panjang, lebar, dan tinggi (pisahkan dengan koma):"
            self.ids.input_field.hint_text = "Panjang, Lebar, Tinggi"
        elif selected_shape == 'Prisma':
            self.ids.input_label.text = "Masukkan alas, tinggi alas, dan tinggi prisma (pisahkan dengan koma):"
            self.ids.input_field.hint_text = "Alas, Tinggi Alas, Tinggi Prisma"


    def calculate_result(self):
        try:
            input_data = self.ids.input_field.text.split(',')
            if self.selected_shape == 'Persegi':
                sisi = float(input_data[0])
                luas = sisi ** 2
                self.result_text = f"Luas Persegi: {luas}"
            elif self.selected_shape == 'Lingkaran':
                jari_jari = float(input_data[0])
                luas = 3.14 * (jari_jari ** 2)
                self.result_text = f"Luas Lingkaran: {luas}"
            elif self.selected_shape == 'Segitiga':
                alas, tinggi = map(float, input_data)
                luas = 0.5 * alas * tinggi
                self.result_text = f"Luas Segitiga: {luas}"
            elif self.selected_shape == 'Persegi Panjang':
                panjang, lebar = map(float, input_data)
                luas = panjang * lebar
                self.result_text = f"Luas Persegi Panjang: {luas}"
            elif self.selected_shape == 'Kubus':
                sisi = float(input_data[0])
                volume = sisi ** 3
                self.result_text = f"Volume Kubus: {volume}"
            elif self.selected_shape == 'Balok':
                panjang, lebar, tinggi = map(float, input_data)
                volume = panjang * lebar * tinggi
                self.result_text = f"Volume Balok: {volume}"
            elif self.selected_shape == 'Prisma':
                alas, tinggi_alas, tinggi_prisma = map(float, input_data)
                volume = (alas * tinggi_alas / 2) * tinggi_prisma
                self.result_text = f"Volume Prisma: {volume}"
            else:
                self.result_text = 'Bangun tidak didukung'
        except Exception as e:
            self.result_text = "Input tidak valid!"



class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ModeSelectionScreen(name='mode_selection'))
        sm.add_widget(PengenalanBentukScreen(name='pengenalan_bentuk'))
        sm.add_widget(HitungLuasScreen(name='hitung_luas'))
        sm.add_widget(InputScreen(name='input_screen'))
        sm.add_widget(AkunScreen(name='akun'))
        return sm

if __name__ == '__main__':
    MainApp().run()
