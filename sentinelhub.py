# -*- coding: utf-8 -*-
"""
/***************************************************************************
 sentinelhub
                                 A QGIS plugin
 sentinelhub
                              -------------------
        begin                : 2016-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2016 by geodrinx
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from sentinelhub_dialog import sentinelhubDialog
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from qgis.core import *
from qgis.gui import *
import qgis


class sentinelhub:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'sentinelhub_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = sentinelhubDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&sentinelhub')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'sentinelhub')
        self.toolbar.setObjectName(u'sentinelhub')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('sentinelhub', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/sentinelhub/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'sentinelhub'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&sentinelhub'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
#------------------------------------------------------------------------
#        """Run method that performs all the real work"""
#        # show the dialog
#        self.dlg.show()
#        # Run the dialog event loop
#        result = self.dlg.exec_()
#        # See if OK was pressed
#        if result:
#            # Do something useful here - delete the line containing pass and
#            # substitute with your code.
#            pass
#------------------------------------------------------------------------

				mapCanvas = self.iface.mapCanvas()
				boundBox = mapCanvas.extent()

				xMin = float(boundBox.xMinimum())
				yMin = float(boundBox.yMinimum())

				xMax = float(boundBox.xMaximum())                
				yMax = float(boundBox.yMaximum())

				xc = (xMin + xMax) / 2.
				yc = (yMin + yMax) / 2.

				crs2     = mapCanvas.mapRenderer().destinationCrs()
				crsSrc2  = QgsCoordinateReferenceSystem(crs2.authid())   
				crsDest2 = QgsCoordinateReferenceSystem(4326)  # Wgs84LLH   
				xform2   = QgsCoordinateTransform(crsSrc2, crsDest2)

				pt5 = xform2.transform(QgsPoint(xc, yc))

				xc = pt5.x()
				yc = pt5.y()

				stringa1 = "http://apps.sentinel-hub.com/sentinel-playground/#x="
				stringa2 = ("%s") %(xc)
				stringa3 = "%2By="
				stringa4 = ("%s") %(yc)
				stringa5 = "%2Bs=14%2Bpreset=1_NATURAL_COLOR%2Blayers=1_NATURAL_COLOR%2Bmaxcc=0%2Bgain=2.1%2Btime=2015-01-01/2016-09-03%2Bpriority=mostRecent"

				sentinel2 = stringa1 + stringa2 + stringa3 + stringa4 + stringa5

				print sentinel2

				QApplication.clipboard().setText(sentinel2)
				msg = "Sentinel URL copied in the clipboard ! "
				if len(msg) > 30:
				  msg = msg + "... ("+str(len(sentinel2))+" chars)"
				self.iface.mainWindow().statusBar().showMessage(msg)
        
#           os.startfile('sentinel2')
