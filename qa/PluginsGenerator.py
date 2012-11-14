import os
try:
    from qa import mafPath
except ImportError:
    import mafPath

currentPathScript = os.path.split(os.path.realpath(__file__))[0]

#read all files and directories , for every rule directory, generate a python file
allPlugins = []

def CheckPluginsDirectories(arg, directory, files):
    if(arg == directory): return
    if os.path.isdir(directory):
        allPlugins.append(os.path.basename(directory))
      
def GeneratePythonQAScripts():
    testList = open("PluginsList.txt", 'w')
    for plugin in allPlugins:
      f = open(plugin + "QA.py", 'w')
      f.write("import os\n")
      f.write("import sys\n")
      f.write("import re\n")
      
      f.write("\n")
      f.write("from Plugins."+ plugin + " import " + plugin + "Script\n")

	  #costant
      f.write("\n")
      f.write(plugin + "Script.execute()")

      testList.write(plugin + "QA.py" + "\n")

      
	  #for
      
      f.close()

    testList.close()

if __name__ == '__main__':
  scriptsDir = os.getcwd()
  os.path.walk(os.path.join(scriptsDir, "Plugins"), CheckPluginsDirectories, os.path.join(scriptsDir, "Plugins"))
  GeneratePythonQAScripts()
  print "GENERATION SUCCESSFUL"
#in each directory check .ini, for every ini generate rule
