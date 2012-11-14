import os
import sys
import getopt
import shutil

try:
    from qa import mafPath
except ImportError:
    import mafPath

currentPathScript = os.path.split(os.path.realpath(__file__))[0]
modulesDir = mafPath.mafSourcesDir
outputDir = mafPath.mafQADir

def run(param):
    scriptsDir = currentPathScript
    f = None
    try:
        f = open("PluginsList.txt")
    except:
        print "QA FAILED"
        print "Probem opening PluginsList.txt"

    lines = f.readlines()
    python = "python "

    suffix = "PluginQA.py"

    resultDir = os.path.abspath(os.path.join(outputDir, "QAResults" , "xml"))
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)

    tempDir = os.path.join(outputDir , "Temp")
    #destroy and create temporary directory for Rules operations
    if  os.path.exists(tempDir):
        shutil.rmtree(tempDir)
    os.makedirs(tempDir)

    for line in lines:
        line = line.replace("\r", "").replace("\n", "")
        script = line
        plugin = script.replace(suffix,"")

        print "QA Running...", plugin
  
        command = python + script 
        print "command: ", command
        os.system(command.replace("\"","").replace("\r", "").replace("\n", ""))

    print "QA SUCCESSFUL"

def usage():
    print "Usage: python PluginsLauncher.py "
    print "-h, --help                    show help (this)"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help",])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    LCOVCoverageFlag = False
    cppcheckFlag = False
    ccccFlag = False
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            return
        else:
            assert False, "unhandled option"

    param = {}
    run(param)
    
if __name__ == "__main__":
  main()
