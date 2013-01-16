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

class RulesRenderer:
    def __init__(self):
        pass
        
    def generateLinks(self):
        #create HTML dir
        scriptsDir = os.getcwd()
        baseDir = os.getcwd()  
        os.chdir(mafPath.mafQADir)
        baseDir = os.getcwd()
        qaResultsDir = os.path.join(baseDir,"QAResults")

        #take results
        xmlDir = os.path.join(baseDir,"QAResults","xml")

        if not os.path.exists(xmlDir):
            print "Xml Directory not present: ", xmlDir
            sys.exit(1) 

        htmlDir = os.path.join(baseDir,"QAResults","html")

        if not os.path.exists(htmlDir):
            os.makedirs(htmlDir)
        if not os.path.exists(os.path.join(htmlDir,"Styles")):  
            os.makedirs(os.path.join(htmlDir,"Styles"))

        if(os.path.exists(os.path.join(htmlDir,"Styles"))):
            origDir = os.path.join(scriptsDir, "Styles")
            destDir = os.path.join(htmlDir, "Styles")
            files = os.listdir(origDir)
            for item in files:
                if (item != 'CVS' and item != 'SVN' and item != '.cvs' and item != '.svn'):
                    shutil.copyfile(os.path.join(origDir,item), os.path.join(destDir, item))
        
        # list of possible results      
        xmlList=os.listdir(xmlDir)
        htmlList=[file.replace(".xml", ".html") for file in os.listdir(xmlDir)]
        ruleLinksString = ""
        for link in htmlList:
            if(link != "index.html" and link != "Styles"):
                ruleLinksString = ruleLinksString + "<li><a href=\"" + link + "\">" + link[:link.find(".")] + "</a></li>\n"
        return ruleLinksString

            
    def generateBody(self):   
        result = style.apply(xml)
           
def main():
    pass

if __name__ == "__main__":
  main()


