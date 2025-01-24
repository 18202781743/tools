import sys
import argparse
import subprocess
import re
import os

# 全局参数
class ArgsInfo:
    projectName = "xxxtools" # 项目名称
    projectBranch = "master" # 项目分支
    projectTag = "1.0.0" # 自定义tag
    githubID = "xxxx"     # github 用户id
    debEmail = "xxxx"
    projectOrg = "linuxdeepin"

    projectRootDir = "~/.cache/git-tag-dir" # 打tag项目根目录

argsInfo = ArgsInfo()

def createRepo():
    a = subprocess.call(["git", "clone", "git@github.com:" + argsInfo.projectOrg + "/" + argsInfo.projectName + ".git"], shell=False)

def initRepo():
    a = subprocess.call("git remote add github git@github.com:" + argsInfo.githubID + "/" + argsInfo.projectName + ".git", shell=True)
    a = subprocess.call(["gh", "repo", "set-default", argsInfo.projectOrg + "/" + argsInfo.projectName], shell=False)
    
def fetchLastTag():
    a = subprocess.call("git fetch origin", shell=True)
    lastTag = subprocess.check_output("git describe --tags --abbrev=0", shell=True)
    lastTag = lastTag.decode().replace('\n', '')
    return lastTag

def initTagPR():
    a = subprocess.call("git fetch origin", shell=True)
    # a = subprocess.call("git stash", shell=True)
    a = subprocess.call(["git", "reset", "--hard", "origin/" + argsInfo.projectBranch], shell=False)
    a = subprocess.call("git checkout -B dev-changelog origin/" + argsInfo.projectBranch, shell=True)
    a = subprocess.call("export " + "DEBEMAIL=" + "'" + argsInfo.debEmail + "'", shell=True)

    lastTag = fetchLastTag()

    commitInfoProcess = subprocess.Popen(["git", "log", "--pretty=format:%s", "--no-merges", lastTag + "..HEAD"], shell=False, stdout=subprocess.PIPE)
    a = subprocess.check_output(["xargs", "-I", "{}", "dch", "-v", argsInfo.projectTag, "{}"], shell=False, stdin=commitInfoProcess.stdout)
    a = subprocess.call("dch -r ''", shell=True)

    a = subprocess.call(["git", "commit", "-a", "-m", "chore: bump version to " + argsInfo.projectTag + "\n\n" + "update changelog to " + argsInfo.projectTag], shell=False)

def createTagPR():
    a = subprocess.call("git push github dev-changelog -f", shell=True)
    a = subprocess.call(["gh", "pr", "create", "--title", "chore: bump version to " + argsInfo.projectTag,  "--body", "update changelog to " + argsInfo.projectTag], shell=False)

def mergePR():
    a = subprocess.call(["gh", "pr", "merge", "-r", "dev-changelog"], shell=False)

def createOrUpdateRepo():
    dir = os.path.expanduser(argsInfo.projectRootDir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    print("Tagging project: ", dir, argsInfo.projectName)
    os.chdir(dir)

    if not os.path.exists(dir + "/" + argsInfo.projectName):
        createRepo()
        os.chdir(argsInfo.projectName)
        initRepo()
    else:
        os.chdir(argsInfo.projectName)

def main(argv):
    parser = argparse.ArgumentParser(description='Pack for CRP.')
    parser.add_argument('command', nargs='?', default='tag', choices=['tag', 'merge', 'test', 'lasttag'], help='The command type (list or pack)')

    parser.add_argument('--dir', type=str, default=None, help='The project directory')
    parser.add_argument('--org', type=str, default=None, help='The project organization, e.g: linuxdeepin')
    parser.add_argument('--name', type=str, default=None, help='The project name')
    parser.add_argument('--branch', type=str, default=None, help='The project branch')
    parser.add_argument('--tag', type=str, default=None, help='The project tag')

    args = parser.parse_args()

    if (args.name is not None):
        argsInfo.projectName = args.name
    if (args.branch is not None):
        argsInfo.projectBranch = args.branch
    if (args.tag is not None):
        argsInfo.projectTag = args.tag
    if (args.dir is not None):
        argsInfo.projectRootDir = args.dir
    if (args.org is not None):
        argsInfo.projectOrg = args.org

    createOrUpdateRepo()
    if (args.command == 'merge'):
        mergePR()
    elif (args.command == 'test'):
        initTagPR()
        subprocess.call("git diff HEAD^ HEAD | cat", shell=True)
    elif (args.command == 'lasttag'):
        lastTag = fetchLastTag()
        print("Last Tag:", lastTag)
    else:
        initTagPR()
        createTagPR()

if(__name__=="__main__"):
    main(sys.argv)
