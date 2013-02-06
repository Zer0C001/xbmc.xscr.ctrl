'''
    XScreenSaver control service for XBMC
    Copyright (C) 2011 Team XBMC
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmc
import subprocess,os
import dbus


powerManagementCookie = None
screenSaverCookie = None

bus = dbus.SessionBus()
ssProxy = bus.get_object('org.freedesktop.ScreenSaver', '/ScreenSaver')
pmProxy = bus.get_object('org.freedesktop.PowerManagement.Inhibit','/org/freedesktop/PowerManagement/Inhibit')
sson=1

xbmc.log("starting xctrl script",xbmc.LOGERROR)
while (not xbmc.abortRequested):
  idle=xbmc.getGlobalIdleTime()
  if(idle>10):
     if(xbmc.Player().isPlayingVideo()):
       if(sson==1):
         powerManagementCookie = pmProxy.Inhibit("XBMC","XBMC playback running")
         screenSaverCookie = ssProxy.Inhibit("XBMC","XBMC playback running")
         os.system("xset -dpms")
         os.system("xset s off")
         xbmc.log("disabled screensaver and dpms",xbmc.LOGERROR)
         sson=0
     else:
       if(sson==0):
         if screenSaverCookie != None:
              ssProxy.UnInhibit(screenSaverCookie)
         if powerManagementCookie != None:
              pmProxy.UnInhibit(powerManagementCookie)
         os.system("xset +dpms")
         os.system("xset s on")
         xbmc.log("enabled scr saver and dpms",xbmc.LOGERROR)
         sson=1
  xbmc.sleep(1000)

if screenSaverCookie != None:
     ssProxy.UnInhibit(screenSaverCookie)
if powerManagementCookie != None:
     pmProxy.UnInhibit(powerManagementCookie)
os.system("xset +dpms")
os.system("xset s on")


xbmc.log("enabled scrs and dpms;exit",xbmc.LOGERROR)

