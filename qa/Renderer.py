import lxml.etree as etree
from lxml.etree import XSLT,fromstring
import os, sys, string, stat
from os.path import exists, join
from os import pathsep
from string import split
import shutil
from datetime import datetime
import getopt

from RulesRenderer import RulesRenderer
from PluginsRenderer import PluginsRenderer

try:
    from qa import mafPath
except ImportError:
    import mafPath

currentPathScript = os.path.split(os.path.realpath(__file__))[0]

class Renderer:
    def __init__(self):
        self.RulesRenderer = RulesRenderer()
        self.PluginsRenderer = PluginsRenderer()
        
    def run(self, param):
        # Base Renderer
        #read xml file
        scriptsDir = os.getcwd()
        os.chdir(mafPath.mafQADir)
        baseDir = os.getcwd()
        qaResultsDir = os.path.join(baseDir,"QAResults")

        #take results
        xmlDir = os.path.join(baseDir,"QAResults","xml")

        if not os.path.exists(xmlDir):
            print "Xml Directory not present: ", xmlDir
            sys.exit(1)

        #create HTML dir    
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

        #Rules links!
        ruleLinksString = self.RulesRenderer.generateLinks()
        xsltH, xsltT = self.generateXSLT()
        
        headString = "".join(open(os.path.join(htmlDir,"Styles" ,"head.temp")))
        headString = headString.replace("@@@_PUBLISH_DATE_@@@", str( datetime.now().date()))
        centerString = "".join(open(os.path.join(htmlDir,"Styles","center.temp")))
        tailString = "".join(open(os.path.join(htmlDir, "Styles","tail.temp")))
   
        # PluginsRenderer
        for d in self.PluginsRenderer.param.keys():
            if(d in param.keys()):
                self.PluginsRenderer.param[d] = param[d]
        
        headString = self.PluginsRenderer.generateLinks(headString)   
        
        # RulesRenderer
        message = { 'xsltHeader' : xsltH ,
                      'header' : headString ,
                      'rulesLink' : ruleLinksString ,
                      'body' : centerString ,
                      'footer' : tailString ,
                      'xsltFooter' : xsltT 
                    } 
        if(self.RulesRenderer.generateBody(xmlDir, message) == True):
            print "PUBLISH SUCCESSFUL"
   
        index = open(os.path.join(htmlDir, "index.html"), 'w')
   
        # Base Renderer
        index.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\" \"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">")
        index.write(headString)
        index.write(ruleLinksString)
        index.write(centerString)
        index.write(self.generateIntroduction())
        index.write(tailString)
        index.close()

        os.chdir(scriptsDir)

    
    def generateXSLT(self):
        xsltH = """<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:output indent="yes"/>
            <xsl:template name="break">
                <xsl:param name="text"/>
                <xsl:choose>
                   <xsl:when test="contains($text, '&#xa;')">
                           <xsl:value-of select="substring-before($text, '&#xa;')"/>
                           <br/>
                           <xsl:call-template name="break">
                                   <xsl:with-param name="text" select="substring-after($text,'&#xa;')"/>
                           </xsl:call-template>
                   </xsl:when>
                   <xsl:otherwise>
                   <xsl:value-of select="$text"/>
                   </xsl:otherwise>
               </xsl:choose>
         </xsl:template>
         <xsl:template match="/">"""
         
        xsltT = """ </xsl:template> </xsl:stylesheet>"""
        return xsltH, xsltT
    
    def generateIntroduction(self):
        introduction = """
           <h1>introduction</h1>
           <!-- **** INSERT PAGE CONTENT HERE **** -->
             <h2>Quality Assurance System</h2>
           <p> 
           The system is composed by several components and it works as a state machine. In order to complete the entire cycle which terminates with the publishing of the QA Results over internet, the needed steps are the following:
           <ul>
           <li> Build Documentation<br/> Each rule needs a source directory in which extracts information from a specified file types. Most part of QA scripts takes advantage from doxygen XML output that is created as first step. A script can also base its execution over another kind of source directory like code directory, and even extract information discriminating files using regular-expression.

             At present there are three source information used by scripts: doxygen xml output of the code without Tests and with Tests, Maf3 source directory.

             Operativelly after installing doxygen 1.5.9 in your computer, you need to run build_doc.bat for windows , or build_doc.sh for Unix like system. They'll be created two directories named Doc and DocWithTests in the same path.</li>
           <li>Generate python scripts<br/> GeneratorQA.py must be launched to create all the scripts based on RuleGroups and Rules inside the last.

             This script checks RuleGroups contained in Rules directory, and create for every RuleGroup a correspondent script with all the rules defined inside. Each RuleGroup and each Rule inside a rulegroup need an initialization file in order to handle parameters. Generally the initialization file of a RuleGroup contain the file type checked and the source directory, while the rule initialization file contains parameter which depends by the rule itself.

             Additionally GeneratorQA.py creates a file with the list of generated scripts.</li>
           <li>Execute generated scripts<br/> ScriptsLauncher.py fulfils the work of executing each generated script. The results are written in a bunch of files in QAResults directory at the root level of the local repository. These are subdivided into a number of files equals to the total number of rule.</li>
           <li>Publish the results<br/> On Parabuild the mechanism described above is present in Linux Server and Windows Server while only on Linux one is present the publication of the results. The publication is only the results of moving result files in a directory that is visible using Apache server.</li>

           </p>
           """
        return introduction
        
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
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        elif o in ("-l", "--enable-coverage"):
            param['coverage'] = True
        elif o in ("-c", "--enable-cppcheck"):
            param['cppcheck'] = True
        elif o in ("-C", "--enable-cccc"):
            param['cccc'] = True
        elif o in ("-M", "--enable-memory-profiling"):
            param['memory-profiling'] = True
        else:
            assert False, "unhandled option"
    
    r = Renderer()
    r.run(param)


if __name__ == "__main__":
  main()


