import lxml.etree as etree
from lxml.etree import XSLT,fromstring
import os, sys, string, stat
from os.path import exists, join
from os import pathsep
from string import split
import shutil
from datetime import datetime
import getopt

try:
    from qa import mafPath
except ImportError:
    import mafPath

currentPathScript = os.path.split(os.path.realpath(__file__))[0]

class PluginsRenderer:
    def __init__(self):
        pass
        
    def generateLinks(self):
        check for external scripting
        pos = 0
        pos = headString.find("@@@_EXTERNAL_TOOLS_REPORT_@@@")-1
        if(param['coverage']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir, "ExternalScripts", "lcov")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "coveragePublish.py"))
      
        li = "<li><a href=\"../externalCoverage/index.html\">Coverage</a></li>";
        headString = headString[:pos] + li + headString[pos:]
        pos = pos + len(li)
        #os.chdir(scriptsDir)

        if(param['cppcheck']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir,"ExternalScripts", "cppcheck")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory,"cppcheckPublish.py"))
            li = "<li><a href=\"../externalcppcheck/index.html\">Static Analysis</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
   
        if(param['cccc']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir,"ExternalScripts", "cccc")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "ccccPublish.py"))
            li = "<li><a href=\"../externalcccc/index.html\">Code Complexity</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
    
        #remove placeholder for external scripting
        headString = headString.replace("@@@_EXTERNAL_TOOLS_REPORT_@@@", "")

    
        
    def run(param):   
        # PluginsRenderer
        self.PluginsRenderer.generateLinks()   
        #check for external scripting
        pos = 0
        pos = headString.find("@@@_EXTERNAL_TOOLS_REPORT_@@@")-1
        if(param['coverage']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir, "ExternalScripts", "lcov")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "coveragePublish.py"))
      
        li = "<li><a href=\"../externalCoverage/index.html\">Coverage</a></li>";
        headString = headString[:pos] + li + headString[pos:]
        pos = pos + len(li)
        #os.chdir(scriptsDir)

        if(param['cppcheck']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir,"ExternalScripts", "cppcheck")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory,"cppcheckPublish.py"))
            li = "<li><a href=\"../externalcppcheck/index.html\">Static Analysis</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
   
        if(param['cccc']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(scriptsDir,"ExternalScripts", "cccc")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "ccccPublish.py"))
            li = "<li><a href=\"../externalcccc/index.html\">Code Complexity</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
    
        #remove placeholder for external scripting
        headString = headString.replace("@@@_EXTERNAL_TOOLS_REPORT_@@@", "")

def usage():
    print "Usage: python ScriptLauncher.py [-h] [-l] [-c] [-M]"
    print "-h, --help                     show help (this)"
    print "-l, --enable-coverage          enable coverage"
    print "-c, --enable-cppcheck          enable cppcheck tool"
    print "-C, --enable-cccc              enable cccc tool: conditional complexity"
    print "-M, --enable-memory-profiling   enable memory profiler tool"

def main():
    pass

if __name__ == "__main__":
  main()


