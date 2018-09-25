"""
	.. sectionauthor:: Joseph Scannell <joseph_scannell@student.uml.edu><joe0400@gmail.com>
	
	cDocGenerator
	cDocGenerator is ran through the terminal/Command Line, and is provided the workingfolder of all the files. Then the file will find all files with extensions .c, .cpp, .h
	Then using the docSyntax, will create htmlsites for all
	
	Provided DocString format
	/*
		@Author:Name
		@Date:Date
		@Method:Name
		@Param:parameter
		@Returns:return
		@Class:Name
		;Text goes here descriving the method, new lines are included,
		Also \t, and \n are ignored so it autofits the text.Use semicolon to end the statement;
	
	*/
	
	a Example DocString for a method named
	int nextFib(int a, int b);
	of Class Fibonacci is provided
	
	/*
		@Class:Fibonacci
		@Method:nextFib
		@Param:a, State n-2
		@Param:b, State n-1
		@Returns:int of the next fib
	*/

	It will then generate a folder named Docs, with all the HTML Doc Sites
	Also include all text you want to keep
"""
#!/usr/bin/python3

import sys
import re
from os import walk
import os

class getFiles:
	
	def __init__(self,path):
		self.files = []
		self.path = path
		for(_,_,fil) in walk(path):
			self.files = fil
			break
	def getCfiles(self):
		fil = [self.files[i] for i in range(len(self.files)) if ((len(self.files[i]) > 4 and self.files[i][-4:] ==".cpp") or (len(self.files[i]) > 2 and self.files[i][-2:] == ".h"))]
		return fil
	def removeCandHfromFiles(self):
		fil = self.getCfiles()
		for i in range(0,len(fil)):
			if(fil[i][-2:] == ".h"):
				fil[i] = fil[i][:-2]
			else:
				fil[i] = fil[i][:-4]
		return fil
	def getHeader(self):
		header = "\n\t\t\t\t<header class=\"mdl-layout__header\">\n\t\t\t\t\t<div class=\"mdl-layout__tab-bar mdl-js-ripple-effect\">\n\t\t\t\t\t\t"
		fil = self.removeCandHfromFiles()
		for i in range(0,len(fil)):
			header += "\t\t\t\t\t\t<a href=\"#"+fil[i]+"\" class=\"mdl-layout__tab"
			if(i == 0):
				header += " is-active"
			header += "\">" + fil[i] + "</a>\n"
		header += "\t\t\t\t\t</div>\n\t\t\t\t</header>\n"
		return header
	def genHTML(self):
		html = "<html><style>\n.card-wide.mdl-card{\nwidth:512px;}\n.card-wide > .mdl-card__title{\ncolor:#fff;\nbackground-color:#7777FF;\n}\n</style><head><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"><link rel=\"stylesheet\" href=\"https://code.getmdl.io/1.3.0/material.indigo-pink.min.css\"><script defer src=\"https://code.getmdl.io/1.3.0/material.min.js\"></script></head>\n\t<body>\n\t\t<div class=\"mdl-layout mdl-js-layout mdl-layout--fixed-header mdl-layout--fixed-tabs\">"+self.getHeader()
		files = self.getCfiles()
		filec = self.removeCandHfromFiles()
		html += "\t\t\t\t<main class=\"mdl-layout__content\">\n"
		for i in range(0,len(files)):
			html += "\t\t\t\t\t<section class=\"mdl-layout__tab-panel "
			if(i == 0):
				html += " is-active"
			html += "\" id=\"" + filec[i] + "\">"
			a = file(self.path+"/"+files[i])
			a.makeDocStringList()
			l = a.genDiscUnions()
			print(l)
			for la in l:
				print(la)
				print(la.__dict__)
				html += la.genCard()
			html += "\t\t\t\t\t</section>\n"
		html += "\t\t\t\t</main>\n\t\t\t</div>\n\t\t</body>\n</html>"
		return html
		
class file:
	def getLineParam(text,param):
		ret = None
		if(text.find(param)!=-1):
			ret = text[text.find(param)+len(param):]
			if(ret.find("\n")!=-1 and (ret.find("*/") > ret.find("\n") or ret.find("*/") == -1)):
				ret = ret[:ret.find("\n")]
			else:
				ret = ret[:ret.find("*/")]
		return ret
	
	def __init__(self,FileLocation):
		self.file = FileLocation
		self.readFile = open(self.file,'r')
		self.text = self.readFile.read()
	def makeDocStringList(self):
		self.list =[]
		while(self.text.find("/*")!= -1):
			self.list.append(self.text[self.text.find("/*"):self.text.find("*/")])
			self.text = self.text[self.text.find("*/")+1:]

	def genDiscUnions(self):
		
		self.discUnions = []
		param = ["@Method",None,"@Returns","@Date","@Author","@Class",None]
		
		for element in self.list:
			params = [None for i in range(7)]
			for i in range(7):
				if(type(param[i]) == str):
					params[i] = [file.getLineParam(element,param[i])]
			if(element.find(";") != -1):
				txt = element[element.find(";")+1:]
				txt = txt[:txt.find(";")].replace('\n',' ').replace('\t','')
				params[6] = txt
			parameter = []
			while(element.find("@Param") != -1):
				parameter.append(getLineParam(element,"@Param"))
				element = element[element.find("@Param"):]
				if(element.find("\n")!=-1 and (element.find("*/") > element.find("\n") or element.find("*/") == -1)):
					element = element[:element.find("\n")]
				else:
					element = element[:element.find("*/")]
			if(len(parameter)== 0):
				parameter = None
			params[1] = parameter
			print(type(params[0]))
			self.discUnions.append(discriminatedUnionDoc(params[0],params[1],params[2],params[3],params[4],params[5],params[6]))
		return self.discUnions
				
		
		
		

class discriminatedUnionDoc:
	
	def instanceOf(A,typeA):
		return type(A)==typeA
	
	def _instanceOr(A,typeA,typeB):
		return type(A)==typeA or type(A)==typeB

	def _instanceCheckL(ListA,typeA,typeB):
		for element in ListA:
			if not discriminatedUnionDoc._instanceOr(element,typeA,typeB):
				return False
		return True

	
	def __init__(self,Methods, Params, Returns, Dates, Author, Class,Text):
		if(not discriminatedUnionDoc._instanceCheckL([Methods,Params,Returns,Dates,Author,Class],type(None),list)):
			raise("One of the Parameters dont fall into type list, or None")
	
		self.Methods = Methods
		
		self.Params = Params

		self.Returns = Returns
	
		self.Dates = Dates
		
		self.Author = Author
		self.Class = Class
		
		self.Text = Text
	def getDict(self):
		return self.__dict__
	
	def genCard(self):
		Card = "\t\t\t\t\t<div class=\"mdl-grid\">\n\t\t\t\t\t\t<div class=\"mdl-layout-spacer\"></div>\n\t\t\t\t\t\t<div class=\"page-content\">\n\t\t\t\t\t\t\t<div class=\"card-wide mdl-card mdl-shadow--2dp\">\n"
		
		if(type(self.Methods) != type(None) and self.Methods != [None]):
			Card += "\t\t\t\t\t\t\t\t<div class=\"mdl-card__title\">	\n\t\t\t\t\t\t\t\t\t<h3>"
			if(type(self.Methods) == list):
				Card += self.Methods[0]
			else:
				Card += self.Methods
			Card += "</h3>\n\t\t\t\t\t\t\t\t</div>\n"
		if(type(self.Params) != type(None) and self.Params != [None]):
			Card += "\t\t\t\t\t\t\t\t<div class=\"mdl-card__supporting-text mdl-card--border\">"
			for each in self.Params:
				Card += "\n\t\t\t\t\t\t\t\t" + each + "<br>"
			Card = Card[:-4]
			Card += "\n\t\t\t\t\t\t\t</div>"
		if(type(self.Text) == str):
			Card += "\t\t\t\t\t\t\t\t<div class=\"mdl-card__supporting-text mdl-card--border\">" + self.Text + "\n\t\t\t\t\t\t\t</div>"
			
		if(type(self.Returns) != type(None) and self.Returns != [None]):
			Card += "\n\t\t\t\t\t\t\t<div class=\"mdl-card__supporting-text mdl-card--border\">\n\t\t\t\t\t\t\t\t"
			if(type(self.Returns)== list):
				Card+= self.Returns[0]
			else:
				Card+= self.Returns
			Card += "\n\t\t\t\t\t\t\t</div>"
		if((type(self.Class) != type(None) and self.Class != [None]) or (type(self.Author) != type(None) and self.Author != [None]) or (type(self.Dates) != type(None) and self.Dates != [None])):
			Card += "\n\t\t\t\t\t\t\t<div class=\"mdl-card__menu\">\n"
			if(type(self.Class) != type(None) and self.Class != [None]):
				Card += "\t\t\t\t\t\t\t\t<span class=\"mdl-chip\">\n\t\t\t\t\t\t\t\t\t<span class=\"mdl-chip__text\">"
				if(type(self.Class) == list):
					Card += self.Class[0]
				else:
					Card += self.Class
				Card += "</span>\n\t\t\t\t\t\t\t\t</span>\n"
			if(type(self.Author) != type(None) and self.Author != [None]):

				Card += "\t\t\t\t\t\t\t\t<span class=\"mdl-chip\">\n\t\t\t\t\t\t\t\t\t<span class=\"mdl-chip__text\">"
				if(type(self.Author) == list):
					Card += self.Author[0]
				else:
					Card += self.Author
				Card += "</span>\n\t\t\t\t\t\t\t\t</span>\n"
			if(type(self.Dates) != type(None) and self.Dates != [None]):

				Card += "\t\t\t\t\t\t\t\t<span class=\"mdl-chip\">\n\t\t\t\t\t\t\t\t\t<span class=\"mdl-chip__text\">"
				if(type(self.Dates) == list):
					Card += self.Dates[0]
				else:
					Card += self.Dates
				Card += "</span>\n\t\t\t\t\t\t\t</span>\n"
			Card += "\t\t\t\t\t\t\t</div>\n"
		Card += "\t\t\t\t\t\t</div></div>\n\t\t\t\t\t\t<div class=\"mdl-layout-spacer\"></div>\n\t\t\t\t\t</div>"
		return Card
		
	
def main():
	a = getFiles(os.getcwd())
	f = open("index.html","w")
	f.write(a.genHTML())
	
	

#class TextGenerator:
main()
