#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines Application nodes classes related to Database objects.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import sibl_gui.components.core.database.operations
import sibl_gui.ui.common
import sibl_gui.ui.nodes
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
            "get_template_user_name",
            "AbstractDatabaseNode",
            "IblSetNode",
            "TemplateNode",
            "CollectionNode"]

LOGGER = foundations.verbose.install_logger()

def get_template_user_name(title, software):
    """
    Returns the Template user name.

    :param title: Template title.
    :type title: unicode
    :param software: Template software.
    :type software: unicode
    :return: Template user name.
    :rtype: unicode
    """

    return foundations.strings.remove_strip(title, software)

class AbstractDatabaseNode(sibl_gui.ui.nodes.GraphModelNode):
    """
    Defines Application Database abstract base class used by concrete Database Node classes.
    """

    __family = "AbstractDatabaseNode"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self,
                database_item,
                name=None,
                parent=None,
                children=None,
                roles=None,
                node_flags=None,
                attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled),
                icon_size=None,
                icon_placeholder=None,
                **kwargs):
        """
        Initializes the class.

        :param database_item: Database object.
        :type database_item: object
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
        self.__database_item = database_item
        self.__tool_tip_text = ""

        AbstractDatabaseNode.__initialize_node(self, attributes_flags)

    @property
    def database_item(self):
        """
        Property for **self.__database_item** attribute.

        :return: self.__database_item.
        :rtype: object
        """

        return self.__database_item

    @database_item.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_item(self, value):
        """
        Setter for **self.__database_item** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "database_item"))

    @database_item.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def database_item(self):
        """
        Deleter for **self.__database_item** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "database_item"))

    @property
    def tool_tip_text(self):
        """
        Property for **self.__tool_tip_text** attribute.

        :return: self.__tool_tip_text.
        :rtype: unicode
        """

        return self.__tool_tip_text

    @tool_tip_text.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def tool_tip_text(self, value):
        """
        Setter for **self.__tool_tip_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "tool_tip_text", value)
        self.__tool_tip_text = value

    @tool_tip_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tool_tip_text(self):
        """
        Deleter for **self.__tool_tip_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tool_tip_text"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        for column in self.__database_item.__table__.columns:
            attribute = column.key
            if attribute == "name":
                continue

            value = getattr(self.__database_item, attribute)
            roles = {Qt.DisplayRole : value,
                    Qt.EditRole : value}
            self[attribute] = sibl_gui.ui.nodes.GraphModelAttribute(attribute, value, roles, attributes_flags)

    def update_node(self):
        """
        Updates the Node from the database item.

        :return: Method success.
        :rtype: bool
        """

        raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
        self.__class__.__name__, self.update_node.__name__, self.__class__.__name__))

    def update_node_attributes(self):
        """
        Updates the Node attributes from the database item attributes.

        :return: Method success.
        :rtype: bool
        """

        for column in self.__database_item.__table__.columns:
            attribute = column.key
            if not attribute in self:
                continue

            if issubclass(self[attribute].__class__, sibl_gui.ui.nodes.GraphModelAttribute):
                self[attribute].value = self[attribute].roles[Qt.DisplayRole] = self[attribute].roles[Qt.EditRole] = \
                getattr(self.__database_item, attribute)
        return True

    def update_database_item(self):
        """
        Updates the database item from the node.

        :return: Method success.
        :rtype: bool
        """

        raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
        self.__class__.__name__, self.update_database_item.__name__, self.__class__.__name__))

    def update_database_itemAttributes(self):
        """
        Updates the database item attributes from the Node attributes.

        :return: Method success.
        :rtype: bool
        """

        for column in self.__database_item.__table__.columns:
            attribute = column.key
            if not attribute in self:
                continue

            if issubclass(self[attribute].__class__, sibl_gui.ui.nodes.GraphModelAttribute):
                setattr(self.__database_item, attribute, self[attribute].value)
        return True

    @foundations.exceptions.handle_exceptions(NotImplementedError)
    def update_tool_tip(self):
        """
        Updates the Node tooltip.

        :return: Method success.
        :rtype: bool
        """

        raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(
        self.__class__.__name__, self.update_tool_tip.__name__, self.__class__.__name__))

class IblSetNode(AbstractDatabaseNode):
    """
    Defines Ibl Sets nodes.
    """

    __family = "IblSet"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self,
                database_item,
                name=None,
                parent=None,
                children=None,
                roles=None,
                node_flags=None,
                attributes_flags=None,
                icon_path=None,
                icon_size=None,
                icon_placeholder=None,
                **kwargs):
        """
        Initializes the class.

        :param database_item: Database object.
        :type database_item: object
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
        :param icon_path: Icon path.
        :type icon_path: unicode
        :param icon_size: Icon size.
        :type icon_size: unicode
        :param icon_placeholder: Icon placeholder.
        :type icon_placeholder: QIcon
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        AbstractDatabaseNode.__init__(self,
                                    database_item,
                                    name,
                                    parent,
                                    children,
                                    roles,
                                    node_flags,
                                    attributes_flags,
                                    icon_size,
                                    icon_placeholder,
                                    **kwargs)

        # --- Setting class attributes. ---
        self.__icon_path = icon_path
        self.tool_tip_text = """
                <p><b>{0}</b></p>
                <p><b>Author: </b>{1}<br>
                <b>Location: </b>{2}<br>
                <b>Shot Date: </b>{3}<br>
                <b>Comment: </b>{4}</p>
                """

        IblSetNode.__initialize_node(self)

    @property
    def icon_path(self):
        """
        Property for **self.__icon_path** attribute.

        :return: self.__icon_path.
        :rtype: unicode
        """

        return self.__icon_path

    @icon_path.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def icon_path(self, value):
        """
        Setter for **self.__icon_path** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "icon_path"))

    @icon_path.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def icon_path(self):
        """
        Deleter for **self.__icon_path** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "icon_path"))

    def __initialize_node(self):
        """
        Initializes the node.
        """

        self.roles.update({Qt.DisplayRole : self.database_item.title,
                            Qt.DecorationRole : foundations.common.filter_path(self.__icon_path),
                            Qt.EditRole : self.database_item.title})
        self.update_tool_tip()

    def update_node(self):
        """
        Updates the node from the database item.

        :return: Method success.
        :rtype: bool
        """

        self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.__database_item.title
        return self.update_node_attributes()

    def update_node_attributes(self):
        """
        Updates the node attributes from the database item attributes.

        :return: Method success.
        :rtype: bool
        """

        return AbstractDatabaseNode.update_node_attributes(self)

    def update_database_item(self):
        """
        Updates the database item from the node.

        :return: Method success.
        :rtype: bool
        """

        self.title = self.database_item.title = self.name
        return self.update_database_itemAttributes()

    def update_tool_tip(self):
        """
        Updates the node tooltip.

        :return: Method success.
        :rtype: bool
        """

        self.roles[Qt.ToolTipRole] = self.tool_tip_text.format(self.database_item.title,
                                                            self.database_item.author or Constants.null_object,
                                                            self.database_item.location or Constants.null_object,
                                                            sibl_gui.ui.common.get_formatted_shot_date(self.database_item.date,
                                                                            self.database_item.time) or Constants.null_object,
                                                            self.database_item.comment or Constants.null_object)
        return True

class TemplateNode(AbstractDatabaseNode):
    """
    Defines Templates nodes.
    """

    __family = "Template"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self,
                database_item,
                name=None,
                parent=None,
                children=None,
                roles=None,
                node_flags=None,
                attributes_flags=None,
                icon_size=None,
                icon_placeholder=None,
                **kwargs):
        """
        Initializes the class.

        :param database_item: Database object.
        :type database_item: object
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

        AbstractDatabaseNode.__init__(self,
                                    database_item,
                                    name,
                                    parent,
                                    children,
                                    roles,
                                    node_flags,
                                    attributes_flags,
                                    icon_size,
                                    icon_placeholder,
                                    **kwargs)

        # --- Setting class attributes. ---
        self.tool_tip_text = """
                <p><b>{0}</b></p>
                <p><b>Author: </b>{1}<br>
                <b>Release Date: </b>{2}<br>
                <b>Comment: </b>{3}</p></p>
                """

        TemplateNode.__initialize_node(self)

    def __initialize_node(self):
        """
        Initializes the node.
        """

        template_user_name = get_template_user_name(self.database_item.title, self.database_item.software)
        self.roles.update({Qt.DisplayRole : template_user_name,
                            Qt.EditRole : template_user_name})
        self.update_tool_tip()

    def update_node(self):
        """
        Updates the node from the database item.

        :return: Method success.
        :rtype: bool
        """

        self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = get_template_user_name(self.database_item.title,
                                                                                                self.database_item.software)

        return self.update_node_attributes()

    def update_node_attributes(self):
        """
        Updates the node attributes from the database item attributes.

        :return: Method success.
        :rtype: bool
        """

        return AbstractDatabaseNode.update_node_attributes(self)

    def update_database_item(self):
        """
        Updates the database item from the node.

        :return: Method success.
        :rtype: bool
        """

        self.title = self.database_item.title = self.name
        return self.update_database_itemAttributes()

    def update_tool_tip(self):
        """
        Updates the node tooltip.

        :return: Method success.
        :rtype: bool
        """

        self.roles[Qt.ToolTipRole] = self.tool_tip_text.format(get_template_user_name(self.database_item.title,
                                                                                self.database_item.software),
                                                                    self.database_item.author,
                                                                    self.database_item.date,
                                                                    self.database_item.comment)
        return True

class CollectionNode(AbstractDatabaseNode):
    """
    Defines Collections nodes.
    """

    __family = "Collection"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self,
                database_item,
                name=None,
                parent=None,
                children=None,
                roles=None,
                node_flags=None,
                attributes_flags=None,
                icon_size=None,
                icon_placeholder=None,
                **kwargs):
        """
        Initializes the class.

        :param database_item: Database object.
        :type database_item: object
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

        AbstractDatabaseNode.__init__(self,
                                    database_item,
                                    name,
                                    parent,
                                    children,
                                    roles,
                                    node_flags,
                                    attributes_flags,
                                    icon_size,
                                    icon_placeholder,
                                    **kwargs)

        # --- Setting class attributes. ---
        self.tool_tip_text = """
                <p><b>{0}</b></p>
                <p><b>Comment: </b>{1}<br></p>
                """

        CollectionNode.__initialize_node(self)

    def __initialize_node(self):
        """
        Initializes the node.
        """

        self["count"] = sibl_gui.ui.nodes.GraphModelAttribute(
                        name="count",
                        value=sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.database_item),
                        flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

        self.roles.update({Qt.DisplayRole : self.database_item.name, Qt.EditRole : self.database_item.name})
        self.update_tool_tip()

    def update_node(self):
        """
        Updates the node from the database item.

        :return: Method success.
        :rtype: bool
        """

        self.name = self.roles[Qt.DisplayRole] = self.roles[Qt.EditRole] = self.database_item.name
        return self.update_node_attributes()

    def update_node_attributes(self):
        """
        Updates the node attributes from the database item attributes.

        :return: Method success.
        :rtype: bool
        """

        self.count.value = self.count.roles[Qt.DisplayRole] = \
        sibl_gui.components.core.database.operations.getCollectionIblSetsCount(self.database_item)

        return AbstractDatabaseNode.update_node_attributes(self)

    def update_database_item(self):
        """
        Updates the database item from the node.

        :return: Method success.
        :rtype: bool
        """

        self.database_item.name = self.name
        return self.update_database_itemAttributes()

    def update_tool_tip(self):
        """
        Updates the node tooltip.

        :return: Method success.
        :rtype: bool
        """

        self.roles[Qt.ToolTipRole] = self.tool_tip_text.format(self.database_item.name,
                                                                self.database_item.comment)
        return True
