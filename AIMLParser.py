import xml.etree.ElementTree as ET
import string

class AIMLParser:
	"""Reads and Writes AIML Files"""

	# ElementTree object used to store data from AIML file
	tree = {}

	# Element object containing root <aiml> object
	root = {}

	# Path of file to load from (used to make saving easier)
	path = None

	def __init__(self, path = None, categoryList = None, author = None, version = "1.0"):
		"""Initialize with either the path to an aiml file or a categoryList"""
		if path:
			self.path = ""
			self.parse(path)
		elif categoryList:
			self.createFromCategoryList(categoryList, author, version)
		else:
			raise TypeError, "path or categoryList required"


	def parse(self, path):
		"""Parse AIML file, saving ElementTree as self.tree"""
		self.tree = ET.parse(path)
		self.root = self.tree.getroot()

	def createFromCategoryList(categoryList, author, version):
		"""Create ElementTree from categoryList"""
		pass

	def save(self, path = None):
		"""Save current ElementTree to file located at `path`"""
		# Case 1: Saving to same location as original file
		if self.path and not path:
			tree.write(self.path)
		# Case 2: Originally loaded from a file, but saving to new file OR
		# Case 3: Saving to file for the first time
		else:
			tree.write(path)

	def getCategory(self, index):
		"""Get category Element by index within the list of Category elements"""
		xpathIndex = index + 1 # convert index to be 1-based, as used by xpath
		xpath = 'category[%d]' % xpathIndex
		return self.root.findall(xpath)[0]

	def createCategory(self, pattern, template):
		"""Create new category, append to root element"""
		categoryElement = ET.SubElement(self.root, "category")
		patternElement = ET.SubElement(categoryElement, "pattern")
		patternElement.text = pattern
		templateElement = ET.SubElement(categoryElement, "template")
		templateElement.text = template

	def editCategory(self, index, pattern = None, template = None):
		"""Update category (with the provided index)'s pattern and template"""
		category = self.getCategory(index)
		patternElement = category.find("pattern")
		templateElement = category.find("template")

		# Update elements' text values (if new value provided)
		if pattern:
			patternElement.text = pattern
		if template:
			templateElement.text = template

	def deleteCategory(self, index):
		"""Delete category with the provided index"""
		category = self.getCategory(index)
		self.root.remove(category)

	def toString(self):
		"""Converts tree to string"""
		return ET.tostring(self.root)

	def toCategoryList(self):
		"""Return rules as a list of (pattern, response) tuples"""
		categories = []
		for rule in self.root.findall("category"):
			pattern = string.strip(rule.find("pattern").text)
			response = string.strip(rule.find("template").text)
			categories.append((pattern, response))
		return categories