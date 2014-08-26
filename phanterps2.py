# -*- coding: utf-8 -*- 
import wx
import os
corrente = os.getcwd()



class meu_splash(wx.App): 
	def OnInit(self):
		
		bmp = wx.Image ( corrente +'\imagens\conexao.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		
		wx.SplashScreen ( bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1200, None, style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP ) 
		wx.Yield() 
		return True


class meu_programa(wx.App):
	def OnInit(self):
		favicon = wx.Icon(corrente +'\imagens\\favicon.png', wx.BITMAP_TYPE_ANY)
		self.title = "PhanterPS2"
		frame = meu_frame(self.title, (-1,-1), (450,340))
		frame.SetIcon(favicon) 
		frame.Show()
		self.SetTopWindow(frame)
		return True

class meu_frame(wx.Frame):
	def __init__ (self, title, pos, size):
		self.title = "PhanterPS2"
		imagem1 = wx.Image ( corrente+'\imagens\\abrir.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem2 = wx.Image ( corrente+'\imagens\salvar.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		imagem3 = wx.Image ( corrente+'\imagens\sobre.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()

		wx.Frame.__init__(self, None, -1, title, pos, size)
		painel = wx.Panel(self)
		barra_de_status = self.CreateStatusBar()
		self.SetStatusText("Bem vindo ao PhanterPS2")
		barra_de_ferramentas = self.CreateToolBar()
		barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem1 , "Abrir", u"Abrir as configurações")
		barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem2 , "Salvar", u"Salvar as configurações")
		barra_de_ferramentas.AddSimpleTool(wx.NewId(), imagem3 , "Sobre", u"Sobre o programa e autor")
		barra_de_ferramentas.Realize()
		Barra_de_menu = wx.MenuBar()
		menu1 = wx.Menu()
		Item_submenu1 = menu1.Append(-1, "A&brir", u"Abrir configurações")
		Item_submenu2 = menu1.Append(-1, "Salvar", u"Salvar configurações")
		Barra_de_menu.Append(menu1, "&Arquivo")

		self.Bind(wx.EVT_MENU, self.AbrirConf, Item_submenu1)
		self.SetMenuBar(Barra_de_menu)
	wildcard = "PhanterFiles (*.pha)|*.phan|All files (*.*)|*.*"
	def AbrirConf (self, event):
		dlg = wx.FileDialog(self, u"Abrindo arquivo de configuração...", corrente, style=wx.OPEN, wildcard=self.wildcard)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetPath()
			print self.filename
			#self.ReadFile()
			self.SetTitle(self.title + ' -- ' + self.filename)
			dlg.Destroy()
	def SalveConf(self, event):
		pass
	def PastaDoJogo (self, event):
		dlg = wx.DirDialog(self, u"Abrindo arquivo de configuração...", corrente, style=wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.dir = dlg.GetPath()
			print self.dir
			self.SetTitle(self.title + ' -- ' + self.filename)
			dlg.Destroy()










if __name__ == '__main__':
	x = meu_splash()
	x.MainLoop()
	y = meu_programa()
	y.MainLoop()
