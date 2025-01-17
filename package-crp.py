import sys
import argparse
import requests
import json
import re

# 全局参数
class ArgsInfo:
    topicName = "test-xxxx" # 主题名称
    projectName = "xxxx" # 项目名称
    projectBranch = "upstream/master" # 项目分支
    projectTag = "5.0.0" # 自定义tag
    projectUpdateMode = True # 根据changelog自动更新版本号
    branchId = 55 # snipe分支
    archs = "amd64;arm64;loong64"
    topicType = "test"
    userName = "xxxx" # crp用户名（过滤topic）
    userId = "utxxxx"     # crp用户id（登陆获取token）
    #（登陆crp后， Post：https://crp.uniontech.com/api/login 的Body），其中token字段
    password ="xxxx"

    token = "xxxx" 

argsInfo = ArgsInfo()

class ProjectInfo:
    name = "dtk6"
    id = 0
    url = "https://gitee.com/xxxxx/dtk6.git"

class TopicInfo:
    name = "test-treeland-private1"
    id = 0

class BranchInfo:
    projectId = 0
    name = "upstream/master"
    commit = "b9e8b6b"
    changelog = "chore: update changelog"

class InstanceInfo:
    Arches = "amd64"
    BaseTag = None
    Branch = "upstream/master"
    BuildID = 0
    BuildState = None
    Changelog = ["chore: update changelog"]
    Commit = "xxxx"
    History = None
    ID = 0
    ProjectID = 4305
    ProjectName = "dtkcommon-v25"
    ProjectRepoUrl = None
    SlaveNode = None
    Tag = "1"
    TagSuffix = None
    TopicID = 20825
    TopicName = "test-treeland"
    TopicType = "test"
    ChangeLogMode = True
    RepoType = "deb"
    Custom = True
    BranchID = "55"

def fetchToken():
    url = "https://crp.uniontech.com/api/login"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "userName": argsInfo.userId,
        "password": argsInfo.password
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print("Status Code:", response.status_code, response.text)
        return ""

    result = response.json()
    for key, value in result.items():
        if (key == "Token"):
            return value
    return ""

def listPojects():
    url = "https://crp.uniontech.com/api/project"
    headers = {
        "Authorization": "Bearer " + argsInfo.token,
        "Content-Type": "application/json"
    }
    data = {
        "page": 0,
        "perPage": 0,
        "projectGroupID": 0,
        "newCommit": False,
        "archived": False,
        "branchID": argsInfo.branchId,
        "name": argsInfo.projectName
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print("Status Code:", response.status_code, response.text)
        return []
    
    projects = []
    result = response.json()
    for key, value in result.items():
        if (key == "Projects" and value != None):
            for project in value:
                projectName = project["Name"]
                id = project["ID"]
                repoUrl =  project["RepoUrl"]
                targetName = argsInfo.projectName
                if (re.search(targetName, projectName, re.IGNORECASE)):
                    info = ProjectInfo()
                    info.id = id
                    info.name = projectName
                    info.url = repoUrl
                    projects.append(info)

    return projects

def listTopics():
    url = "https://crp.uniontech.com/api/topics/search"
    headers = {
        "Authorization": "Bearer " + argsInfo.token,
        "Content-Type": "application/json"
    }
    data = {
        "TopicType": argsInfo.topicType, 
        "UserName": argsInfo.userName, 
        "BranchID": argsInfo.branchId
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    topics = []
    result = response.json()
    for i, topic in enumerate(result):
        id = topic["ID"]
        topicName = topic["Name"]
        targetName = argsInfo.topicName
        if (re.search(targetName, topicName, re.IGNORECASE)):
            info = TopicInfo()
            info.id = id
            info.name = topicName
            topics.append(info)

    return topics

def fetchCommitInfo(repoUrl, commit):
    url = "https://crp.uniontech.com/api/projects/getGerritCommitMessage"
    headers = {
        "Authorization": "Bearer " + argsInfo.token,
        "Content-Type": "application/json"
    }
    data = {
        "repo_url": repoUrl, 
        "commit_id": commit
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return

    result = response.json()
    for key, value in result.items():
        if (key == "message"):
            return value
    return ""

def listBranchs(projectId, projectUrl, targetName):
    url = "https://crp.uniontech.com/api/projects/" + str(projectId) + "/branches"
    headers = {
        "Authorization": "Bearer " + argsInfo.token
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    branchs = []
    result = response.json()
    for i, branch in enumerate(result):
        commit = branch["Commit"]
        name = branch["Name"]
        if (re.search(targetName, name, re.IGNORECASE)):
            info = BranchInfo()
            info.commit = commit
            info.name = name
            info.projectId = projectId
            changelog = fetchCommitInfo(projectUrl, commit)
            info.changelog = changelog
            branchs.append(info)

    return branchs

def listCreatedInstances(topicId):
    url = "https://crp.uniontech.com/api/topics/" + str(topicId) + "/releases"
    headers = {
        "Authorization": "Bearer " + argsInfo.token
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    instances = []
    result = response.json()
    for i, instance in enumerate(result):
        info = InstanceInfo()
        info.ID = instance["ID"]
        info.ProjectID = instance["ProjectID"]
        info.ProjectName = instance["ProjectName"]
        info.Branch = instance["Branch"]
        info.BuildState = instance["BuildState"]["state"]
        instances.append(info)

    return instances

def deleteInstance(instanceId):
    url = "https://crp.uniontech.com/api/topic_releases/" + str(instanceId)
    headers = {
        "Authorization": "Bearer " + argsInfo.token
    }

    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
    else: 
        print("delete instance success:", instanceId)

def createInstance(instanceInfo):
    url = "https://crp.uniontech.com/api/topics/" + str(instanceInfo.TopicID) + "/new_release"
    headers = {
        "Authorization": "Bearer " + argsInfo.token,
        "Content-Type": "application/json"
    }
    data = {
        "Arches": instanceInfo.Arches,
        "BaseTag": instanceInfo.BaseTag,
        "Branch": instanceInfo.Branch,
        "BuildID": instanceInfo.BuildID,
        "BuildState": instanceInfo.BuildState,
        "Changelog":  [instanceInfo.Changelog],
        "Commit": instanceInfo.Commit,
        "History": instanceInfo.History,
        "ID": instanceInfo.ID,
        "ProjectID": instanceInfo.ProjectID,
        "ProjectName": instanceInfo.ProjectName,
        "ProjectRepoUrl": instanceInfo.ProjectRepoUrl,
        "SlaveNode": instanceInfo.SlaveNode,
        "Tag": instanceInfo.Tag,
        "TagSuffix": instanceInfo.TagSuffix,
        "TopicID": instanceInfo.TopicID,
        "TopicType": instanceInfo.TopicType,
        "ChangeLogMode": instanceInfo.ChangeLogMode,
        "RepoType": instanceInfo.RepoType,
        "Custom": instanceInfo.Custom,
        "BranchID": instanceInfo.BranchID
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        print("Error:", response.status_code, response.text, data)
    else:
        print("Success:", response.text)

def listInstances():
    instances = []
    topics = listTopics()
    if len(topics) == 0:
        print("Error: No topics found")
        return []

    for topic in topics:
        projects = listPojects()
        if len(projects) == 0:
            continue
        for project in projects:
            branchs = listBranchs(project.id, project.url, argsInfo.projectBranch)
            if len(branchs) == 0:
                continue
            for branch in branchs:
                info = InstanceInfo()
                info.Commit = branch.commit
                info.Branch = branch.name
                info.Arches = argsInfo.archs
                info.BranchID = argsInfo.branchId
                info.TopicType = argsInfo.topicType
                info.TopicID = topic.id
                info.TopicName = topic.name
                info.ProjectID = project.id
                info.ProjectName = project.name
                info.Changelog = branch.changelog
                info.Tag = argsInfo.projectTag
                info.ChangeLogMode = argsInfo.projectUpdateMode
                instances.append(info)

    return instances

def createOrUpdate():
    instances = listInstances()
    for item in instances:
        print("create", item.TopicName, item.ProjectName, item.Branch, item.Changelog)
        createdInstance = listCreatedInstances(item.TopicID)
        for (createdInstance) in createdInstance:
            if (createdInstance.ProjectName == item.ProjectName and createdInstance.Branch == item.Branch):
                deleteInstance(createdInstance.ID)
        createInstance(item)

def main(argv):
    parser = argparse.ArgumentParser(description='Package for CRP.')
    parser.add_argument('command', nargs='?', default='package', choices=['package', 'projects', 'topics', 'instances', 'branches'], help='The command type (list or package)')

    parser.add_argument('--topic', type=str, default=None, help='The topic name parameter')
    parser.add_argument('--name', type=str, default=None, help='The project name parameter')
    parser.add_argument('--branch', type=str, default=None, help='The project branch parameter')
    parser.add_argument('--tag', type=str, default=None, help='The project tag parameter')

    args = parser.parse_args()

    if (args.topic is not None):
        argsInfo.topicName = args.topic
    if (args.name is not None):
        argsInfo.projectName = args.name
    if (args.branch is not None):
        argsInfo.projectBranch = args.branch
    if (args.tag is not None):
        argsInfo.projectTag = args.tag
        argsInfo.projectUpdateMode = False
    
    token = fetchToken()
    argsInfo.token = token
    
    if (args.command == 'projects'):
        projects = listPojects()
        for project in projects:
            print(project.name)
    if (args.command == 'topics'):
        topics = listTopics()
        for topic in topics:
            print(topic.name)
    if (args.command == 'instances'):
        topics = listTopics()
        if (len(topics) == 0):
            print("No topics found")
            return
        for topic in topics:
            instances = listCreatedInstances(topic.id)
            for instance in instances:
                print(topic.name, instance.ProjectName, instance.Branch, instance.BuildState)
    if (args.command == 'branches'):
        topics = listTopics()
        if len(topics) == 0:
            print("Error: No topics found")
            return []
        for topic in topics:
            projects = listPojects()
            if len(projects) == 0:
                continue
            for project in projects:
                branchs = listBranchs(project.id, project.url, "")
                for branch in branchs:
                    print(topic.name, project.name, branch.name, branch.changelog)
    if (args.command == 'package'):
        createOrUpdate()

if(__name__=="__main__"):
    main(sys.argv)
