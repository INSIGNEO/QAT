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
        self.scriptsDir = ""
        self.param = {'coverage' : None,
                      'cppcheck' : None,
                      'cccc' : None,
                      'memory-profiling' : None,
                     }
        pass
        
    def generateLinks(self, headString):
        #check for external scripting
        self.scriptsDir = os.getcwd()
        pos = 0
        pos = headString.find("@@@_EXTERNAL_TOOLS_REPORT_@@@")-1

        if(self.param['coverage']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(self.scriptsDir, "Plugins", "lcovPlugin")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "lcovPluginPublish.py"))
            li = "<li><a href=\"../externalCoverage/index.html\">Coverage</a></li>";
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)

        if(self.param['cppcheck']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(self.scriptsDir,"Plugins", "cppcheckPlugin")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory,"cppcheckPluginPublish.py"))
            li = "<li><a href=\"../externalcppcheck/index.html\">Static Analysis</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
   
        if(self.param['cccc']):
            #generateExternalLink
            externalScriptDirectory = os.path.join(self.scriptsDir,"Plugins", "ccccPlugin")
            #os.chdir(externalScriptDirectory)
            os.system("python " + os.path.join(externalScriptDirectory, "ccccPluginPublish.py"))
            li = "<li><a href=\"../externalcccc/index.html\">Code Complexity</a></li>"
            headString = headString[:pos] + li + headString[pos:]
            pos = pos + len(li)
            #os.chdir(scriptsDir)
    
        #remove placeholder for external scripting
        headString = headString.replace("@@@_EXTERNAL_TOOLS_REPORT_@@@", "")
        return headString

def usage():
    print "Usage: python ScriptLauncher.py [-h] [-l] [-c] [-M]"
    print "-h, --help                     show help (this)"
    print "-l, --enable-coverage          enable coverage"
    print "-c, --enable-cppcheck          enable cppcheck tool"
    print "-C, --enable-cccc              enable cccc tool: conditional complexity"
    print "-M, --enable-memory-profiling   enable memory profiler tool"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlcCM", ["help","enable-coverage","enable-cppcheck","enable-cccc", "enable-memory-profiling"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    param = {'coverage':False, 'cppcheck':False, 'cccc':False, 'memory-profiling' : False}
    p = PluginsRenderer()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        elif o in ("-l", "--enable-coverage"):
            p.param['coverage'] = True
        elif o in ("-c", "--enable-cppcheck"):
            p.param['cppcheck'] = True
        elif o in ("-C", "--enable-cccc"):
            p.param['cccc'] = True
        elif o in ("-M", "--enable-memory-profiling"):
            p.param['memory-profiling'] = True
        else:
            assert False, "unhandled option"

    p.generateLinks("")


if __name__ == "__main__":
  main()


