#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`sibl_gui.components.core.inspector.inspector.Inspector`
    Component Interface class nodes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.verbose
import sibl_gui.ui.nodes

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PlatesNode"]

LOGGER = foundations.verbose.install_logger()

class PlatesNode(sibl_gui.ui.nodes.GraphModelNode):
    """
    Defines :class:`sibl_gui.components.core.inspector.inspector.Inspector`
        Component Interface class Model Plates node.
    """

    __family = "Plate"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self,
                plate,
                name=None,
                parent=None,
                children=None,
                roles=None,
                node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                icon_size=None,
                icon_placeholder=None,
                **kwargs):
        """
        Initializes the class.

        :param plate: Plate object.
        :type plate: Plate
        :param name: Node name.
        :type name: unicode
        :param parent: Node parent.
        :type parent: GraphModelNode
        :param children: Children.
        :type children: list
        :param roles: Roles.
        :type roles: dict
        :param node_flags: Node flags.
        :type node_flags: int
        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        :param icon_size: Icon size.
        :type icon_size: unicode
        :param icon_placeholder: Icon placeholder.
        :type icon_placeholder: QIcon
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        sibl_gui.ui.nodes.GraphModelNode.__init__(self,
                                                name,
                                                parent,
                                                children,
                                                roles,
                                                node_flags,
                                                icon_size,
                                                icon_placeholder,
                                                **kwargs)

        # --- Setting class attributes. ---
        self.__plate = plate

        self.__tool_tip_text = """
                                <p><b>{0}</b></p>
                                """

        PlatesNode.__initialize_node(self, attributes_flags)

    @property
    def plate(self):
        """
        Property for **self.__plate** attribute.

        :return: self.__plate.
        :rtype: Plate
        """

        return self.__plate

    @plate.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def plate(self, value):
        """
        Setter for **self.__plate** attribute.

        :param value: Attribute value.
        :type value: Plate
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "plate"))

    @plate.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def plate(self):
        """
        Deleter for **self.__plate** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "plate"))

    @property
    def tool_tip_text(self):
        """
        Property for **self.__tool_tip_text** attribute.

        :return: self.__tool_tip_text.
        :rtype: unicode
        """

        return self.__tool_tip_text

    @tool_tip_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tool_tip_text(self, value):
        """
        Setter for **self.__tool_tip_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tool_tip_text"))

    @tool_tip_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tool_tip_text(self):
        """
        Deleter for **self.__tool_tip_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "plate"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        self.roles.update({Qt.ToolTipRole : self.__tool_tip_text.format(self.name)})
