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
      f.write("from Plugins."+ plugin + " import " + plugin + "\n")

	  #instantiate
      f.write("plugin = " + plugin + "." + plugin + "() \n")
      
      #set parameters
      """for rule in rules:
        f.write("\n")
        f.write("    " + "def " + rule + "(self, dirPath, file):" + "\n")
        f.write("    " + "    rule = " + rule + "." + rule + "()"  + "\n")
        
        inif = open("./Rules/" + ruleGroup + "/" + rule + ".ini", 'r')
        lines = inif.readlines()
        inif.close()
        parameters = []
        for line in lines:
          if(line[-1] == "\n"):
            parameters.append(line[10:-1]) # remove "parameter="
          else:
            parameters.append(line[10:]) # remove "parameter="
        parameterString = ",".join(parameters)"""
      f.write("plugin.setPluginParameters({test=\"uno\", var=\"due\"})\n")
      
      #execute
      f.write("plugin.execute()")

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
