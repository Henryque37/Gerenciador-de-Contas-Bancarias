from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.animation import Animation
import json
import os

os.environ["KIVY_GL_BACKEND"] = "gl"
os.environ["KIVY_WINDOW"] = "sdl2"


class Gerenciador(ScreenManager):
	pass

class Menu(Screen):
	def on_pre_enter(self):
		Window.bind(on_request_close=self.confirmacao)

	def confirmacao(self,*args,**kargs):
		box = BoxLayout(orientation='vertical', padding='10sp',spacing='10sp')
		botoes = BoxLayout(padding='10sp',spacing='10sp')
		
		pop = Popup(title='Deseja mesmo sair?', content=box,size_hint=(0.1,0.1))

		sim = Botao(text='Sim', on_release=App.get_running_app().stop)
		nao = Botao(text='Não', on_release=pop.dismiss)

		botoes.add_widget(sim)
		botoes.add_widget(nao)

		atencao = Image(source='atencao.png')

		box.add_widget(atencao)
		box.add_widget(botoes)


		animText = Animation(color=(0,0,0,1)) + Animation(color=(1,1,1,1))
		animText.repeat = True
		animText.start(sim)
		anim = Animation(size_hint=(0.5,0.3), duration=0.3, t='out_back')
		anim.start(pop)
		pop.open()
		return True

class Botao(ButtonBehavior,Label):
	cor = ListProperty([0.1,0.5,0.7,1])
	cor2 = ListProperty([0.1,0.1,0.1,0.1])


	def __init__(self,**kwargs):
		super(Botao,self).__init__(**kwargs)

	def on_pos(self,*args):
		self.atualizar()

	def on_size(self,*args):
		self.atualizar()

	def on_press(self,*args):
		self.cor, self.cor2 = self.cor2, self.cor

	def on_release(self,*args):
		self.cor, self.cor2 = self.cor2, self.cor

	def on_cor(self,*args):
		self.atualizar()

	def atualizar(self,*args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(rgba=self.cor)
			Ellipse(size=(self.height,self.height),
					pos=(self.pos))
			Ellipse(size=(self.height,self.height),
					pos=(self.x+self.width-self.height,self.y))
			Rectangle(size=(self.width-self.height,self.height),
					pos=(self.x+self.height/2.0,self.y))

class Tarefas(Screen):
	tarefas = []
	path = ''
	leitura_concluida = False
	
	def on_pre_enter(self):
		Window.softinput_mode = 'pan'
		self.path = App.get_running_app().user_data_dir+'/'
		self.loadData()
		Window.bind(on_keyboard=self.voltar)
		if Tarefas.leitura_concluida == 0:
			for tarefa in self.tarefas:
				self.ids.box.add_widget(Tarefa(text=tarefa))
				Tarefas.leitura_concluida = True

	def voltar(self,window,key,*args):
		if key == 27:
			App.get_running_app().root.current = 'menu'
			return True

	def on_pre_leave(self):
		Window.softinput_mode = ''
		Window.unbind(on_keyboard=self.voltar)

	def loadData(self,*args):
		try:
			with open(self.path+'data.json','r') as data:
				self.tarefas = json.load(data)
		except FileNotFoundError:
			pass

	def saveData(self,*args):
		with open(self.path+'data.json', 'w') as data:
			json.dump(self.tarefas,data)

	def removeWidget(self,tarefa):
		texto = tarefa.ids.label.text
		self.ids.box.remove_widget(tarefa)
		self.tarefas.remove(texto)
		self.saveData()

	def addWidget(self):
		texto = self.ids.texto.text
		self.ids.box.add_widget(Tarefa(text=texto))
		self.ids.texto.text=''
		self.tarefas.append(texto)
		self.saveData()

class Tarefa(BoxLayout):
	def __init__(self, text='', **kwargs):
		super(Tarefa,self).__init__(**kwargs)
		self.ids.label.text = text

class aplic(App):
	def build(self):
		return Gerenciador()

aplic().run()
