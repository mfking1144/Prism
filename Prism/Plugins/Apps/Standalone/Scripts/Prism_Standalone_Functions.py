# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2020 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import platform
import shutil

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

if platform.system() != "Windows":
    import pwd

from PrismUtils.Decorators import err_catcher as err_catcher


class Prism_Standalone_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

    @err_catcher(name=__name__)
    def startup(self, origin):
        if "loadProject" not in self.core.prismArgs:
            return False

    @err_catcher(name=__name__)
    def onProjectChanged(self, origin):
        pass

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        return ""

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.loadOiio()

        origin.closeParm = "closeafterloadsa"
        origin.actionStateManager.setEnabled(False)

    @err_catcher(name=__name__)
    def projectBrowserLoadLayout(self, origin):
        pass

    @err_catcher(name=__name__)
    def setRCStyle(self, origin, rcmenu):
        pass

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        return False

    @err_catcher(name=__name__)
    def correctExt(self, origin, lfilepath):
        return lfilepath

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}, underscore=True):
        return

    @err_catcher(name=__name__)
    def setSaveColor(self, origin, btn):
        btn.setPalette(origin.savedPalette)

    @err_catcher(name=__name__)
    def clearSaveColor(self, origin, btn):
        btn.setPalette(origin.oldPalette)

    @err_catcher(name=__name__)
    def setProject_loading(self, origin):
        pass

    @err_catcher(name=__name__)
    def onPrismSettingsOpen(self, origin):
        pass

    @err_catcher(name=__name__)
    def createProject_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def editShot_startup(self, origin):
        origin.loadOiio()

    @err_catcher(name=__name__)
    def shotgunPublish_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def createWinStartMenu(self, origin):
        if os.environ.get("prism_skip_root_install"):
            print "skipped creating Prism startmenu because of missing permissions."
            return

        if platform.system() == "Windows":
            startMenuPath = os.path.join(
                os.environ["AppData"], "Microsoft", "Windows", "Start Menu", "Programs"
            )
            trayStartup = os.path.join(startMenuPath, "Startup", "PrismTray.lnk")
            trayStartMenu = os.path.join(startMenuPath, "Prism", "PrismTray.lnk")
            pbStartMenu = os.path.join(
                startMenuPath, "Prism", "PrismProjectBrowser.lnk"
            )
            settingsStartMenu = os.path.join(
                startMenuPath, "Prism", "PrismSettings.lnk"
            )

            trayLnk = os.path.join(self.core.prismRoot, "Tools", "PrismTray.lnk")
            pbLnk = os.path.join(
                self.core.prismRoot, "Tools", "PrismProjectBrowser.lnk"
            )
            settingsLnk = os.path.join(
                self.core.prismRoot, "Tools", "PrismSettings.lnk"
            )

            cbPath = trayStartup

            toolList = [
                [trayLnk, "PrismTray.exe", "PrismTray.py"],
                [pbLnk, "PrismProjectBrowser.exe", "PrismCore.py"],
                [settingsLnk, "PrismSettings.exe", "PrismSettings.py"],
            ]

            for i in toolList:
                if not os.path.exists(os.path.dirname(i[0])):
                    os.makedirs(os.path.dirname(i[0]))

                self.core.createShortcut(
                    i[0],
                    vTarget=("%s\Python27\%s" % (self.core.prismRoot, i[1])),
                    args=('"%s\Scripts\%s" standalone' % (self.core.prismRoot, i[2])),
                )

        elif platform.system() == "Linux":
            if os.getuid() != 0:
                QMessageBox.warning(
                    QWidget(),
                    "Prism start menu",
                    "Please run this tool as root to continue.",
                )
                return

            if os.path.exists(self.core.integration.installLocPath):
                os.chmod(self.core.integration.installLocPath, 0o777)

            trayStartup = "/etc/xdg/autostart/PrismTray.desktop"
            trayStartMenu = "/usr/share/applications/PrismTray.desktop"
            pbStartMenu = "/usr/share/applications/PrismProjectBrowser.desktop"
            settingsStartMenu = "/usr/share/applications/PrismSettings.desktop"

            trayLnk = os.path.join(self.core.prismRoot, "Tools", "PrismTray.desktop")
            pbLnk = os.path.join(
                self.core.prismRoot, "Tools", "PrismProjectBrowser.desktop"
            )
            settingsLnk = os.path.join(
                self.core.prismRoot, "Tools", "PrismSettings.desktop"
            )
            spbPath = os.path.join(
                self.core.prismRoot, "Tools", "PrismProjectBrowser.sh"
            )
            ssPath = os.path.join(self.core.prismRoot, "Tools", "PrismSettings.sh")
            cbPath = os.path.join(self.core.prismRoot, "Tools", "PrismTray.sh")
            pMenuSource = os.path.join(self.core.prismRoot, "Tools", "Prism.menu")

            for i in [
                trayLnk,
                pbLnk,
                settingsLnk,
                spbPath,
                ssPath,
                cbPath,
                pMenuSource,
            ]:
                if not os.path.exists(i):
                    continue

                with open(i, "r") as f:
                    content = f.read()

                content = content.replace("PRISMROOT", self.core.prismRoot)

                with open(i, "w") as f:
                    f.write(content)

            pMenuTarget = "/etc/xdg/menus/applications-merged/Prism.menu"

            for i in [trayLnk, pbLnk, settingsLnk, pMenuSource]:
                if os.path.exists(i):
                    with open(i, "r") as init:
                        initStr = init.read()

                    with open(i, "w") as init:
                        initStr = initStr.replace(
                            "PRISMROOT", self.core.prismRoot.replace("\\", "/")
                        )
                        init.write(initStr)

            if not os.path.exists(os.path.dirname(pMenuTarget)):
                try:
                    os.makedirs(os.path.dirname(pMenuTarget))
                except:
                    pass

            if os.path.exists(pMenuTarget):
                os.remove(pMenuTarget)

            if os.path.exists(pMenuSource) and os.path.exists(
                os.path.dirname(pMenuTarget)
            ):
                shutil.copy2(pMenuSource, pMenuTarget)
                os.chmod(pMenuTarget, 0o777)
            else:
                print("could not create Prism startmenu entry")

            if os.path.exists(pbLnk):
                userName = (
                    os.environ["SUDO_USER"]
                    if "SUDO_USER" in os.environ
                    else os.environ["USER"]
                )
                desktopPath = "/home/%s/Desktop/%s" % (
                    userName,
                    os.path.basename(pbLnk),
                )
                if os.path.exists(desktopPath):
                    try:
                        os.remove(desktopPath)
                    except:
                        pass

                if os.path.exists(os.path.dirname(desktopPath)):
                    shutil.copy2(pbLnk, desktopPath)
                    uid = pwd.getpwnam(userName).pw_uid
                    os.chown(desktopPath, uid, -1)

            # subprocess.Popen(['bash', "/usr/local/Prism/Tools/PrismTray.sh"])

        elif platform.system() == "Darwin":
            if os.path.exists(self.core.integration.installLocPath):
                os.chmod(self.core.integration.installLocPath, 0o777)

            userName = (
                os.environ["SUDO_USER"]
                if "SUDO_USER" in os.environ
                else os.environ["USER"]
            )
            trayStartup = (
                "/Users/%s/Library/LaunchAgents/com.user.PrismTray.plist" % userName
            )
            trayStartMenu = "/Applications/Prism/Prism Tray.command"
            pbStartMenu = "/Applications/Prism/Prism Project Browser.command"
            settingsStartMenu = "/Applications/Prism/Prism Settings.command"

            trayStartupSrc = os.path.join(
                self.core.prismRoot, "Tools", "Templates", "com.user.PrismTray.plist"
            )
            trayLnk = os.path.join(
                self.core.prismRoot, "Tools", "Templates", "Prism Tray.command"
            )
            pbLnk = os.path.join(
                self.core.prismRoot, "Tools", "Templates", "Prism Project Browser.command"
            )
            settingsLnk = os.path.join(
                self.core.prismRoot, "Tools", "Templates", "Prism Settings.command"
            )

            if os.path.exists(trayStartupSrc):
                with open(trayStartupSrc, "r") as init:
                    initStr = init.read()

                try:
                    tmpPath = os.path.join(self.core.prismRoot, "Tools", "tmp.txt")
                    open(tmpPath, "w").close()
                    os.remove(tmpPath)
                except IOError:
                    QMessageBox.warning(
                        QWidget(),
                        "Prism start menu",
                        "Please copy the Prism folder to any location on your harddrive before you execute the Prism setup.",
                    )
                    return False

            if os.path.exists(pbLnk):
                desktopPath = "/Users/%s/Desktop/%s" % (
                    userName,
                    os.path.splitext(os.path.basename(pbLnk))[0],
                )
                if os.path.exists(desktopPath):
                    try:
                        os.remove(desktopPath)
                    except:
                        pass

                if os.path.lexists(desktopPath):
                    os.unlink(desktopPath)

                os.symlink(pbLnk, desktopPath)

            # subprocess.Popen(['bash', "/usr/local/Prism/Tools/PrismTray.sh"])

        if trayStartMenu != "" and not os.path.exists(os.path.dirname(trayStartMenu)):
            try:
                os.makedirs(os.path.dirname(trayStartMenu))
            except:
                pass

        if not os.path.exists(os.path.dirname(trayStartup)):
            try:
                os.makedirs(os.path.dirname(trayStartup))
                if platform.system() in ["Linux", "Darwin"]:
                    os.chmod(os.path.dirname(trayStartup), 0o777)
            except:
                pass

        if os.path.exists(trayStartup):
            os.remove(trayStartup)

        if os.path.exists(trayLnk):
            if os.path.exists(os.path.dirname(trayStartup)):
                if platform.system() == "Darwin":
                    os.system("cp \"%s\" \"%s\"" % (trayLnk, trayStartup))
                else:
                    shutil.copy2(trayLnk, trayStartup)
                os.chmod(trayStartup, 0o777)
            else:
                print("could not create PrismTray autostart entry")

            if trayStartMenu != "":
                if os.path.exists(os.path.dirname(trayStartMenu)):
                    if platform.system() == "Darwin":
                        os.system("cp \"%s\" \"%s\"" % (trayLnk, trayStartMenu))
                    else:
                        shutil.copy2(trayLnk, trayStartMenu)
                    os.chmod(trayStartMenu, 0o777)
                else:
                    print("could not create PrismTray startmenu entry")

        if pbStartMenu != "":
            if os.path.exists(pbLnk) and os.path.exists(os.path.dirname(pbStartMenu)):
                if platform.system() == "Darwin":
                    os.system("cp \"%s\" \"%s\"" % (pbLnk, pbStartMenu))
                else:
                    shutil.copy2(pbLnk, pbStartMenu)
                os.chmod(pbStartMenu, 0o777)
            else:
                print("could not create PrismProjectBrowser startmenu entry")

        if settingsStartMenu != "":
            if os.path.exists(settingsLnk) and os.path.exists(
                os.path.dirname(settingsStartMenu)
            ):
                if platform.system() == "Darwin":
                    os.system("cp \"%s\" \"%s\"" % (settingsLnk, settingsStartMenu))
                else:
                    shutil.copy2(settingsLnk, settingsStartMenu)
                os.chmod(settingsStartMenu, 0o777)
            else:
                print("could not create PrismSettings startmenu entry")

        if platform.system() == "Darwin":
            templateTools = [
                trayLnk,
                pbLnk,
                settingsLnk,
            ]

            shortCuts = [trayStartup, trayStartMenu, pbStartMenu, settingsStartMenu]
            uid = pwd.getpwnam(userName).pw_uid

            for i in templateTools:
                if not os.path.exists(i):
                    continue

                targetPath = os.path.join(
                    os.path.dirname(os.path.dirname(i)), os.path.basename(i)
                )

                os.system("cp \"%s\" \"%s\"" % (i, targetPath))
                os.chmod(targetPath, 0o777)
                filepath = targetPath
                shortCuts.append(filepath)

            for i in shortCuts:
                if not os.path.exists(i):
                    continue

                with open(i, "r") as init:
                    scriptStr = init.read()

                with open(i, "w") as init:
                    scriptStr = scriptStr.replace(
                        "PRISMROOT", self.core.prismRoot.replace("\\", "/")
                    )
                    init.write(scriptStr)

                os.chown(i, uid, -1)

        return True
