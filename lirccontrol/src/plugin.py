from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from enigma import eTimer
from Components.ConfigList import ConfigListScreen
from Components.config import config, getConfigListEntry, ConfigText, ConfigSelection, ConfigSubsection, ConfigYesNo

global sessions

sessions = []

config.plugins.lirc = ConfigSubsection()
config.plugins.lirc.enable_lircd = ConfigYesNo(default=false)

class LIRCControlMain(ConfigListScreen,Screen):
    skin = """
<screen position="100,100" size="550,400" title="LIRC-Control" >
</screen>"""
    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.list.append(getConfigListEntry(_("enable LIRCd"), config.plugins.lirc.enable_lircd))
        ConfigListScreen.__init__(self, self.list)
        self["buttonred"] = Label(_("cancel"))
        self["buttongreen"] = Label(_("ok"))
        self["setupActions"] = ActionMap(["SetupActions"],
        {
            "green": self.save,
            "red": self.cancel,
            "save": self.save,
            "cancel": self.cancel,
            "ok": self.save,
        }, -2)


    def save(self):
        print "[LIRC-Control] saving config"
        for x in self["config"].list:
            x[1].save()
        self.close(True)

    def cancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close(False)

class LIRCd:
	enabled = False
	sessions = []
	lastip = ""

	def __init__(self):
		self.timer = eTimer()
		
	def enable(self):
		if config.plugins.lirc.enable_lircd.value:
			self.enabled = True
			
	def disable(self):
		if self.enabled:
			self.enabled = False

	def addSession(self,session):
		self.sessions.append(session)

	def onPluginStart(session, **kwargs):
		session.openWithCallback(onPluginStartCB,LIRCControlMain)

	def onPluginStartCB(changed):
		print "[LIRC-Control] config changed=",changed
		global dyndnsservice
		if changed:
			lircd.disable()
			lircd.enable()

global lircd
lircd = LIRCd()

def onSessionStart(reason, **kwargs):
	global lircd
	if config.plugins.lirc.enable_lircd.value is not False:
		if "session" in kwargs:
			lircd.addSession(kwargs["session"])
		if reason == 0:
			lircd.enable()
		elif reason == 1:
			lircd.disable()

def Plugins(path,**kwargs):
return [PluginDescriptor(where = [PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc = onSessionStart),
PluginDescriptor(name=_("LIRC-Control"), description=_("change LIRC settings & add custom remotes"),where = [PluginDescriptor.WHERE_PLUGINMENU], fnc = onPluginStart, icon="lirc.png")]
