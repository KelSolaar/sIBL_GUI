#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 - 2011 - Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs:
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - thomas.mansencal@gmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	testsParser.py
***
***	Platform:
***		Windows, Linux, Mac Os X
***
***	Description:
***		Parser Tests Module.
***
***	Others:
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os
import unittest
from collections import OrderedDict

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import foundations.parser
from foundations.parser import Parser

#***********************************************************************************************
#***	Overall Variables
#***********************************************************************************************
RESOURCES_DIRECTORY = os.path.join(os.path.dirname(__file__), "resources")
COMPONENT_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.rc")
IBL_SET_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.ibl")
TEMPLATE_FILE = os.path.join(RESOURCES_DIRECTORY, "standard.sIBLT")
FILES = {"component":COMPONENT_FILE,
		"iblSet":IBL_SET_FILE,
		"template":TEMPLATE_FILE}
SECTIONS_AND_ATTRIBUTES = {"component":OrderedDict([("Component", {"stripped":["Name", "Module", "Object", "Rank", "Version"],
																"namespaced":["Component|Name", "Component|Module", "Component|Object", "Component|Rank", "Component|Version"]}),
													("Informations", {"stripped":["Author", "Email", "Url", "Description"],
																"namespaced":["Informations|Author", "Informations|Email", "Informations|Url", "Informations|Description"]})]),
							"iblSet":OrderedDict([("Header", {"stripped":["ICOfile", "Name", "Author", "Location", "Comment", "GEOlat", "GEOlong", "Link", "Date", "Time", "Height", "North"],
															"namespaced":["Header|ICOfile", "Header|Name", "Header|Author", "Header|Location", "Header|Comment", "Header|GEOlat", "Header|GEOlong", "Header|Link", "Header|Date", "Header|Time", "Header|Height", "Header|North"]}),
												("Background", {"stripped":["BGfile", "BGmap", "BGu", "BGv", "BGheight"],
															"namespaced":["Background|BGfile", "Background|BGmap", "Background|BGu", "Background|BGv", "Background|BGheight"]}),
												("Enviroment", {"stripped":["EVfile", "EVmap", "EVu", "EVv", "EVheight", "EVmulti", "EVgamma"],
															"namespaced":["Enviroment|EVfile", "Enviroment|EVmap", "Enviroment|EVu", "Enviroment|EVv", "Enviroment|EVheight", "Enviroment|EVmulti", "Enviroment|EVgamma"]}),
												("Reflection", {"stripped":["REFfile", "REFmap", "REFu", "REFv", "REFheight", "REFmulti", "REFgamma"],
															"namespaced":["Reflection|REFfile", "Reflection|REFmap", "Reflection|REFu", "Reflection|REFv", "Reflection|REFheight", "Reflection|REFmulti", "Reflection|REFgamma"]}),
												("Sun", {"stripped":["SUNcolor", "SUNmulti", "SUNu", "SUNv"],
															"namespaced":["Sun|SUNcolor", "Sun|SUNmulti", "Sun|SUNu", "Sun|SUNv"]}),
												("Light1", {"stripped":["LIGHTname", "LIGHTcolor", "LIGHTmulti", "LIGHTu", "LIGHTv"],
															"namespaced":["Light1|LIGHTname", "Light1|LIGHTcolor", "Light1|LIGHTmulti", "Light1|LIGHTu", "Light1|LIGHTv"]})]),
							"template":OrderedDict([("Template", {"stripped":["Name", "Path", "HelpFile", "Release", "Date", "Author", "Email", "Url", "Software", "Version", "Renderer", "OutputScript", "Comment"],
																"namespaced":["Template|Name", "Template|Path", "Template|HelpFile", "Template|Release", "Template|Date", "Template|Author", "Template|Email", "Template|Url", "Template|Software", "Template|Version", "Template|Renderer", "Template|OutputScript", "Template|Comment"]}),
													("sIBL File Attributes", {"stripped":["BGfile", "BGheight", "EVfile", "EVmulti", "EVgamma", "REFfile", "REFmulti", "REFgamma", "SUNu", "SUNv", "SUNcolor", "SUNmulti", "Height", "North", "DynamicLights"],
																"namespaced":["sIBL File Attributes|Background|BGfile", "sIBL File Attributes|Background|BGheight", "sIBL File Attributes|Enviroment|EVfile", "sIBL File Attributes|Enviroment|EVmulti", "sIBL File Attributes|Enviroment|EVgamma", "sIBL File Attributes|Reflection|REFfile", "sIBL File Attributes|Reflection|REFmulti", "sIBL File Attributes|Reflection|REFgamma", "sIBL File Attributes|Sun|SUNu", "sIBL File Attributes|Sun|SUNv", "sIBL File Attributes|Sun|SUNcolor", "sIBL File Attributes|Sun|SUNmulti", "sIBL File Attributes|Header|Height", "sIBL File Attributes|Header|North", "sIBL File Attributes|Lights|DynamicLights"]}),
													("Common Attributes", {"stripped":["createBackground", "createLighting", "createReflection", "createSun", "createLights"],
																"namespaced":["Common Attributes|createBackground", "Common Attributes|createLighting", "Common Attributes|createReflection", "Common Attributes|createSun", "Common Attributes|createLights"]}),
													("Additional Attributes", {"stripped":["preserveSessionSettings", "createFeedBack", "createGround", "shadowCatcher", "hideLights", "physicalSun", "activateFinalGather", "activateLinearWorkflow", "framebufferGamma", "photographicTonemapper", "showCamerasDialog"],
																"namespaced":["Additional Attributes|preserveSessionSettings", "Additional Attributes|createFeedBack", "Additional Attributes|createGround", "Additional Attributes|shadowCatcher", "Additional Attributes|hideLights", "Additional Attributes|physicalSun", "Additional Attributes|activateFinalGather", "Additional Attributes|activateLinearWorkflow", "Additional Attributes|framebufferGamma", "Additional Attributes|photographicTonemapper", "Additional Attributes|showCamerasDialog"]}),
													("Remote Connection", {"stripped":["ConnectionType", "ExecutionCommand", "DefaultAddress", "DefaultPort"],
																"namespaced":["Remote Connection|ConnectionType", "Remote Connection|ExecutionCommand", "Remote Connection|DefaultAddress", "Remote Connection|DefaultPort"]}),
													("Script", None)])}

RANDOM_ATTRIBUTES = {"component":{"Component|Name":"core.db", "Component|Module":"db", "Informations|Author":"Thomas Mansencal", "Informations|Email":"thomas.mansencal@gmail.com"},
					"iblSet":{"Header|ICOfile":"Icon.jpg", "Header|Name":"Standard", "Background|BGfile":"Standard_Background.jpg", "Background|BGmap":"1", "Enviroment|EVfile":"Standard_Lighting.jpg", "Enviroment|EVmap":"1", "Reflection|REFfile":"Standard_Reflection.jpg", "Reflection|REFmap":"1", "Sun|SUNcolor":"240,250,255", "Sun|SUNmulti":"1.0", "Light1|LIGHTcolor":"250,220,190", "Light1|LIGHTmulti":"0.75"},
					"template":{"Template|Name":"@Name | Standard | String | Template Name", "Template|Path":"@Path | | String | Template Path", "sIBL File Attributes|Background|BGfile":"@BGfile", "sIBL File Attributes|Background|BGheight":"@BGheight", "Common Attributes|createBackground":"@createBackground | 1 | Boolean | Create Background", "Common Attributes|createLighting":"@createLighting | 1 | Boolean | Create Lighting", "Additional Attributes|preserveSessionSettings":"@preserveSessionSettings | 1 | Boolean | Preserve Session Settings", "Additional Attributes|createFeedBack":"@createFeedBack | 1 | Boolean | Create Feedback", "Remote Connection|ConnectionType":"@ConnectionType | Socket | String | Connection Type", "Remote Connection|ExecutionCommand":"@ExecutionCommand | source \"$loaderScriptPath\"; | String | ExecutionCommand"}}

RANDOM_COMMENTS = {"component":{"Component|#0":{'content': ' Component Comment For Tests Purpose.', 'id': 0}, "Informations|#1":{'content': ' Informations Comment For Tests Purpose.', 'id': 1}},
					"iblSet":{"Header|#0":{'content': ' Header Comment For Tests Purpose.', 'id': 0}, "Header|#1":{'content': ' Additional Header Comment For Tests Purpose.', 'id': 1}},
					"template":{"Template|#0":{'content': ' Template Comment For Tests Purpose.', 'id': 0}, "sIBL File Attributes|#1":{'content': ' sIBL File Attributes Comment For Tests Purpose.', 'id': 1}}}

SCRIPT_RAW_SECTION = [ "// @OutputScript - @Release For @Software @Version\n",
						"// Author : @Author\n",
						"// EMail : @Email\n",
						"// Homepage : @Url\n",
						"// Template Path : @Path\n",
						"// Template Last Modified : @Date\n",
						"// sIBL_GUI\n",
						"string $backgroundFilePath = \"@BGfile\";\n",
						"int $backgroundWidth = @BGheight*2;\n",
						"string $lightingFilePath = \"@EVfile\";\n" ]

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class ParserTestCase(unittest.TestCase):
	'''
	This Class Is The ParserTestCase Class.
	'''

	def testRequiredAttributes(self):
		'''
		This Method Tests Presence Of Required Attributes.
		'''

		parser = Parser(IBL_SET_FILE)
		requiredAttributes = ("_file",
								"_content",
								"_splitter",
								"_namespaceSplitter",
								"_commentLimiter",
								"_commentMarker",
								"_rawSectionContentIdentifier",
								"_sections",
								"_comments")

		for attribute in requiredAttributes:
			self.assertIn(attribute, parser.__dict__)

	def testRequiredMethods(self):
		'''
		This Method Tests Presence Of Required Methods.
		'''

		parser = Parser(IBL_SET_FILE)
		requiredMethods = ("parse",
							"sectionsExists",
							"attributeExists",
							"getAttributes",
							"getValue")

		for method in requiredMethods:
			self.assertIn(method, dir(parser))

	def testParse(self):
		'''
		This Method Tests The "Parser" Class "parse" Method.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parseSuccess = parser.parse()
			self.assertTrue(parseSuccess)

			self.assertIsInstance(parser.sections, OrderedDict)
			self.assertIsInstance(parser.comments, OrderedDict)
			parser.parse(orderedDictionary=False)
			self.assertIsInstance(parser.sections, dict)
			self.assertIsInstance(parser.comments, dict)

	def testSections(self):
		'''
		This Method Tests The "Parser" Class Sections.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse()
			self.assertListEqual(parser.sections.keys(), SECTIONS_AND_ATTRIBUTES[type].keys())
			parser.parse(orderedDictionary=False)
			for section in SECTIONS_AND_ATTRIBUTES[type]:
				self.assertIn(section, parser.sections.keys())

	def testRawSections(self):
		'''
		This Method Tests The "Parser" Class Raw Sections.
		'''

		parser = Parser(TEMPLATE_FILE)
		parser.read()
		parser.parse(rawSections=("Script"))
		self.assertListEqual(parser.sections["Script"]["Script|_rawSectionContent"][0:10], SCRIPT_RAW_SECTION)

	def testComments(self):
		'''
		This Method Tests The "Parser" Class Comments.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse()
			self.assertEqual(parser.comments, OrderedDict())
			parser.parse(stripComments=False)
			for comment, value in RANDOM_COMMENTS[type].items():
				self.assertIn(comment, parser.comments)
				self.assertEqual(value["id"], parser.comments[comment]["id"])

	def testSectionExists(self):
		'''
		This Method Tests The "Parser" Class "sectionsExists" Method.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse()

			self.assertTrue(parser.sectionsExists(SECTIONS_AND_ATTRIBUTES[type].keys()[0]))
			self.assertFalse(parser.sectionsExists("Unknown"))

	def testAttributeExists(self):
		'''
		This Method Tests The "Parser" Class "attributeExists" Method.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(False)
			for attribute in RANDOM_ATTRIBUTES[type].keys():
				self.assertTrue(parser.attributeExists(attribute, foundations.parser.getNamespace(attribute)[0]))
				self.assertFalse(parser.attributeExists("Unknown", foundations.parser.getNamespace(attribute)[0]))

	def testGetAttributes(self):
		'''
		This Method Tests The "Parser" Class "getAttributes" Method.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse()
			for section in SECTIONS_AND_ATTRIBUTES[type]:
				if SECTIONS_AND_ATTRIBUTES[type][section]:
					self.assertListEqual(parser.getAttributes(section, True, False).keys(), SECTIONS_AND_ATTRIBUTES[type][section]["stripped"])
					self.assertListEqual(parser.getAttributes(section).keys(), SECTIONS_AND_ATTRIBUTES[type][section]["namespaced"])

	def testGetValue(self):
		'''
		This Method Tests The "Parser" Class "getValue" Method.
		'''

		for type, file in FILES.items():
			parser = Parser(file)
			parser.read()
			parser.parse(False)
			for attribute, value in RANDOM_ATTRIBUTES[type].items():
				self.assertIsInstance(parser.getValue(attribute, foundations.parser.getNamespace(attribute)[0]), str)
				self.assertIsInstance(parser.getValue(attribute, foundations.parser.getNamespace(attribute)[0], encode=True), unicode)
				self.assertEqual(parser.getValue(attribute, foundations.parser.getNamespace(attribute)[0]), value)

class SetNamespaceTestCase(unittest.TestCase):
	'''
	This Class Is The SetNamespaceTestCase Class.
	'''

	def testSetNamespace(self):
		'''
		This Method Tests The "setNamespace" Definition.
		'''

		self.assertIsInstance(foundations.parser.setNamespace("Section", "Attribute"), str)
		self.assertEqual(foundations.parser.setNamespace("Section", "Attribute"), "Section|Attribute")
		self.assertEqual(foundations.parser.setNamespace("Section", "Attribute", ":"), "Section:Attribute")

class GetNamespaceTestCase(unittest.TestCase):
	'''
	This Class Is The GetNamespaceTestCase Class.
	'''

	def testGetNamespace(self):
		'''
		This Method Tests The "getNamespace" Definition.
		'''

		self.assertIsInstance(foundations.parser.getNamespace("Section:Attribute", ":"), list)
		self.assertEqual(foundations.parser.getNamespace("Section|Attribute"), ["Section"])
		self.assertEqual(foundations.parser.getNamespace("Section:Attribute", ":"), ["Section"])
		self.assertIsNone(foundations.parser.getNamespace("Section"))

class RemoveNamespaceTestCase(unittest.TestCase):
	'''
	This Class Is The RemoveNamespaceTestCase Class.
	'''

	def testRemoveNamespace(self):
		'''
		This Method Tests The "testRemoveNamespace" Definition.
		'''

		self.assertIsInstance(foundations.parser.removeNamespace("Section|Attribute"), str)
		self.assertEqual(foundations.parser.removeNamespace("Section|Attribute"), "Attribute")
		self.assertEqual(foundations.parser.removeNamespace("Section:Attribute", ":"), "Attribute")
		self.assertEqual(foundations.parser.removeNamespace("Section|Attribute|Value"), "Value")
		self.assertEqual(foundations.parser.removeNamespace("Section|Attribute|Value", rootOnly=True), "Attribute|Value")

class GetAttributeCompoundTestCase(unittest.TestCase):
	'''
	This Class Is The GetAttributeCompoundTestCase Class.
	'''

	def testGetAttributeCompound(self):
		'''
		This Method Tests The "getAttributeCompound" Definition.
		'''

		self.assertIsInstance(foundations.parser.getAttributeCompound("Attribute", "Value"), foundations.parser.AttributeCompound)

		self.assertEqual(None, foundations.parser.getAttributeCompound("Attribute").value)

		compound = foundations.parser.AttributeCompound(name="Attribute", value="Value", link="@Link", type="Boolean", alias="Link Parameter")
		bindingIdentifier = "@Link | Value | Boolean | Link Parameter"
		self.assertEqual(compound.name, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).name)
		self.assertEqual(compound.value, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).value)
		self.assertEqual(compound.link, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).link)
		self.assertEqual(compound.type, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).type)
		self.assertEqual(compound.alias, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).alias)

		bindingIdentifier = "@Link"
		self.assertEqual(compound.link, foundations.parser.getAttributeCompound("Attribute", bindingIdentifier).link)

if __name__ == "__main__":
	import tests.utilities
	unittest.main()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
