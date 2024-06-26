# -*- coding: utf-8 -*-
"""
/***************************************************************************
 plugin_3Dialog
                                 A QGIS plugin
 plugin16_18
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2024 by NataliaJulia
        email                : qwert
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsMessageLog, Qgis
from qgis.core import QgsProject, QgsPointXY
from qgis.utils import iface


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wtyczka_1_dialog_base.ui'))


class plugin_3Dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(plugin_3Dialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.przycisk_przewyzszenie.clicked.connect(self.przewyzszenie)
        self.przycisk_pole_pow.clicked.connect(self.pole_powierzchni)
    def przewyzszenie(self):
        obiekt = iface.activeLayer()
        obiekt2 = obiekt.selectedFeatures()
        if len(obiekt2) != 2:
            iface.messageBar().pushMessage(
                "Obliczanie przewyższenia", 
                "Jeżeli chcesz obliczyć różnicę wysokości musisz wybrać 2 punkty!", 
                level=Qgis.Warning
            )
            return
        if len(obiekt2) == 2:
            H1 = float(obiekt2[0]['h_plevrf20'])
            H2 = float(obiekt2[1]['h_plevrf20'])
            przewyzszenie = round(H2 - H1, 3)

            self.wynik_przewyzszenie.setText(f"{przewyzszenie}  m")

            QgsMessageLog.logMessage(
                f"Różnica wysokości między wybranymi punktami wynosi: {przewyzszenie} m", 
                level=Qgis.Success
            )
            iface.messageBar().pushMessage(
                "Obliczanie przewyższenia", 
                "Różnica wysokości między wybranymi punktami została policzona.", 
                level=Qgis.Success
            )

    def pole_powierzchni(self):
        warstwa = iface.activeLayer()
        obiekt_pole = iface.activeLayer().selectedFeatures()
        punkty = []
        for o in obiekt_pole:
            x = float(o.geometry().asPoint().x())
            y = float(o.geometry().asPoint().y())
            punkt = QgsPointXY(x, y)
            punkty.append(punkt)
        if len(obiekt_pole)>2:
            pole = 0
            ilosc_punktow = len(punkty)
            for i in range(ilosc_punktow):
                p = (i + 1) % ilosc_punktow
                pole += (punkty[p].x() + punkty[i].x()) * (punkty[p].y() - punkty[i].y())
    
            pole /= 2
            pole = round(abs(pole/10000), 3)
    
            self.wynik_pole_pow.setText(str(pole) + 'ha')

            QgsMessageLog.logMessage(
            f"Pole powierzchni powstałej figury wynosi: {pole} ha.",
            level=Qgis.Success
        )


