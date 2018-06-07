#used libraries
import sys
import argparse
import json
from PIL import Image, ImageDraw, ImageColor

#class holding parameters for point figure
class Point:
	
	type = "Point"
	
	#constructor, takes x y coordinates and color of a point
	def __init__(self,xcoord,ycoord,col):
		self.x = xcoord
		self.y = ycoord
		self.color = col
	#end __init__
#end Point

#class holding parameters for polygon figure
class Polygon:
	
	type = "Polygon"
	
	#constructor, takes list of x y coordinates and color of a polygon
	def __init__(self,pts,col):
		self.points = pts
		self.color = col
	#end __init__
#end Polygon

#class holding parameters for rectangle figure
class Rectangle:

	type = "Rectangle"

	#constructor, takes x y coordinates of a starting point,
	#width, height and color of a rectangle
	def __init__(self,xcoord,ycoord,wid,hei,col):
		self.x = xcoord
		self.y = ycoord
		self.width = wid
		self.height = hei
		self.color = col
	#end __init__
#end Rectangle

#class holding parameters for circle figure
class Circle:
	
	type = "Circle"
	
	#constructor, takes x y coordinates of a center,
	#radius and color of a circle
	def __init__(self,xcoord,ycoord,rad,col):
		self.x = xcoord
		self.y = ycoord
		self.radius = rad
		self.color = col
	#end __init__
#end Circle

#class defining drawing object
class Drawer:
	
	#constructor, takes width, height and background color of an image
	def __init__(self, w, h, c):
		self.image = Image.new("RGB",(w,h),c)	#creates Image object with given parameters
		self.drawing = ImageDraw.Draw(self.image)	#crates ImageDraw object
	#end __init__
	
	#draws given figure as parameter using ImageDraw object
	def draw_figure(self, f):
		if f.type == "Point":
			self.drawing.point([f.x,f.y],f.color)
		elif f.type == "Polygon":
			self.drawing.polygon(f.points,f.color,f.color)
		elif f.type == "Rectangle":
			self.drawing.rectangle([f.x,f.y,f.x+f.width,f.y+f.height],f.color,f.color)
		elif f.type == "Circle":
			self.drawing.arc([f.x-f.radius,f.y-f.radius,f.x+f.radius,f.y+f.radius],0,360,f.color)
		else:
			raise ValueError("Wrong figure type")
	#end draw_figure
	
	#displays drawn image
	def show(self):
		self.image.show()
	#end show
	
	#saves image under given filename
	def save(self,name):
		self.image.save(name)
	#end save
#end Drawer

#class defining reader object used to parse json input
#and create figure objects from the data
class Reader:

	#constructor, opens given input json file, parses it
	#and sets number of parameters
	def __init__(self,input):
		with open(input) as f:
			self.data = json.load(f)
		self.palette = self.data["Palette"]
		self.screen_height = self.data["Screen"]["height"]
		self.screen_width = self.data["Screen"]["width"]
		self.screen_bgcolor = self.get_color(self.data["Screen"]["bg_color"])
		self.screen_fgcolor = self.get_color(self.data["Screen"]["fg_color"])
		self.figures = []
		for fig in self.data["Figures"]:
			if "color" in fig:								#if color was given to figure
				fig_color = self.get_color(fig["color"])	#then use it
			else:											#otherwise use foreground screen color
				fig_color = self.screen_fgcolor
			type = fig["type"]
			if type == "point":
				self.figures.append(Point(fig["x"],fig["y"],fig_color))
			elif type == "polygon":
				self.figures.append(Polygon(self.enlist_points(fig["points"]),fig_color))
			elif type == "rectangle":
				self.figures.append(Rectangle(fig["x"],fig["y"],fig["width"],fig["height"],fig_color))
			elif type == "square":
				self.figures.append(Rectangle(fig["x"],fig["y"],fig["size"],fig["size"],fig_color))
			elif type == "circle":
				self.figures.append(Circle(fig["x"],fig["y"],fig["radius"],fig_color))
			else:
				raise ValueError("Wrong figure type")
	#end __init__

	#changes given list of rgb color values to html #rrggbb notation
	def change_to_hex(self, values):
		ret = "#"
		values = list(map(int,values))
		for v in values:
			ret += hex(v).split('x')[-1]
		return ret
	#end change_to_hex
	
	#returns list of points given as list of lists
	def enlist_points(self, points):
		return list(x for l in points for x in l)
	#end enlist_points
	
	#returns color value in html notation
	def get_color(self, col):
		if col in self.palette:			#checks if given color is in palette
			return self.palette[col]
		elif col[0] == '#':				#if color is already in html notation then returns it
			return col
		else:							#else converts tuple of rgb values to html notation
			col = col[1:len(col)-1]
			vals = col.split(',',2)
			col = self.change_to_hex(vals)
			return col
	#end get_color
	
	#creates drawer object, draws figures and returns drawer object
	def draw_figures(self):
		draw = Drawer(self.screen_width,self.screen_height,self.screen_bgcolor)
		for f in self.figures:
			draw.draw_figure(f)
		return draw
	#end draw_figures
#end Reader

def main():
	#ArgumentParser for easy argument handling
	args_parser = argparse.ArgumentParser()
	args_parser.add_argument("input_file", action="store", type=str, help="name of the input json file")
	args_parser.add_argument('-o', action='store', dest='output_file', type=str, help="name of the output image file")
	args = args_parser.parse_args()
	
	print("Reading input...")
	reader = Reader(args.input_file)	#creates reader out of an input
	print("Drawing figures...")
	drawer = reader.draw_figures()		#draws figures
	if args.output_file == None:		#if output is not given then displays image
		print("Displaying image...")
		drawer.show()
	else:								#else saves image under given output filename
		print("Saving image...")
		drawer.save(args.output_file)
#end main()
	
if __name__ == "__main__":
    main()
