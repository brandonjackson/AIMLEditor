import xml.etree.ElementTree as ET
import string

class AIMLParser:
	"""
	Reads and Writes AIML Files

	Note On Naming Conventions
	--------------------------

	Where possible, the names used both internally and in the class's
	public interface reflect the element names in the AIML spec, even
	though those names are not always intuitive. For example, the
	<category> element is actually what one might more easily conceptualize
	as a "rule," but for consistency it is referred to as a category.

	The only notable exception is the `categoryList`, which is a custom
	data structure created to make it easy to pass lists of rules, umm, I mean
	categories, back and forth.

	Initialization
	--------------

	There are two different ways to initialize this class:

	(1) Parse AIML file

		AP = AIMLParser("test.aiml")

	(2) Construct a new AIML file from a categoryList that contains
	(pattern,template) tuples. It can be passed all of the arguments
	that are passed to AIMLParser.createFromCategoryList().
		
		rules = []
		rules.append(("*", "Does not compute."))
		rules.append(("HELLO", "Hi!"))
		AP = AIMLParser(categoryList, author="John Smith")

	Saving Files
	------------

	To save changes to a file called "test.aiml" pass the path like so:

		AP.save("test.aiml")

	If the parser was initialized with an existing file, changes can
	be saved without passing a path to save():

		AP.save()

	Reading a File's Contents
	-------------------------

	To easily access a list of rules containing patterns and responses
	(known internally as a `categoryList`), use the following method:

		AP.toCategoryList()

	For the example file we created in the Initialization section, this
	method returns the following list (formatted here for convenience):

		[("*", "Does not compute"),
		 ("HELLO", "Hi!")]

	"""

	# ElementTree object used to store data from AIML file
	tree = {}

	# Element object containing root <aiml> object
	root = {}

	# Path of file to load from (used to make saving easier)
	path = None

	def __init__(self, path = None, categoryList = None, **keywords):
		"""
		Initialize with either the path to an aiml file or a categoryList

		if categoryList specified, the following keywords should be passed
		directly to self.createFromCategoryList():
			- version
			- author
			- language
		(they aren't listed above so that their defaults aren't defined
		 twice)
		"""
		if path:
			self.path = path
			self.parse(path)
		elif categoryList:
			self.createFromCategoryList(categoryList, **keywords)
		else:
			raise TypeError, "path or categoryList required"


	def parse(self, path):
		"""Parse AIML file, saving ElementTree as self.tree"""
		self.tree = ET.parse(path)
		self.root = self.tree.getroot()

	def createFromCategoryList(self, categoryList, author="aimlEditor", 
								version = "1.0", language = "en"):
		"""Create ElementTree from categoryList"""

		# Create root AIML element
		self.root = ET.Element("aiml")
		self.root.set("version",version)
		self.tree = ET.ElementTree(self.root)

		# Create meta elements
		authorElement = ET.SubElement(self.root, "meta")
		authorElement.set("name", "author")
		authorElement.set("content", author)

		languageElement = ET.SubElement(self.root, "meta")
		languageElement.set("name","language")
		languageElement.set("content", language)

		# Create category elements
		self.setCategories(categoryList)

	def save(self, path = None):
		"""Save current ElementTree to file located at `path`"""
		# Determine which path to save to.
		# Case 1: Saving to same location as original file
		if self.path and not path:
			path = self.path
		# Case 2: Originally loaded from a file, but saving to new file OR
		# Case 3: Saving to file for the first time
		else:
			# use path provided as argument
			pass
		self.tree.write(path, encoding="ISO-8859-1", xml_declaration=True)

	def setCategories(self, categoryList, overwrite = True):
		"""Defines categories based on categoryList"""

		# @todo should this be separated into:
		# 	- setCategories() which overwrites by default
		# 	- updateCategories() which does not?
		#
		# OR 
		#
		# should I move to a more traditional CRUD interface
		# and split the overwrite task into two function calls:
		#	- to overwrite: deleteCategories() and then insertCategories()
		#	- to update: updateCategores()
		#
		# I should consult how rails ActiveRecord handles this problem...

		# By default, overwrites all existing categories
		if overwrite:
			self.deleteCategories()
			for pattern, template in categoryList:
				self.createCategory(pattern, template)
		# If overwrite is false, try to update matching pattern and
		# if no match found then create new category
		else:
			existingCategories = self.root.findall("category")
			for pattern, template in categoryList:
				matchFound = False
				# @todo move some of this code to a new method 
				# editCategoryByPattern() that edits based on pattern string
				# instead of based on index
				for oldCategory in existingCategories:
					if oldCategory.find("pattern").text == pattern:
						matchFound = True
						oldCategory.find("template").text = template
				if not matchFound:
					self.createCategory(pattern, template)


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

		# @todo enable matching based on pattern strings in addition to index
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

	def deleteCategories(self):
		"""Delete all categories"""
		for category in self.root.findall("category"):
			self.root.remove(category)

	def toString(self):
		"""Converts tree to string (note: excludes XML declaration)"""
		return ET.tostring(self.root)

	def toCategoryList(self):
		"""Return rules as a list of (pattern, response) tuples"""
		categories = []
		for rule in self.root.findall("category"):
			pattern = string.strip(rule.find("pattern").text)
			response = string.strip(rule.find("template").text)
			categories.append((pattern, response))
		return categories
