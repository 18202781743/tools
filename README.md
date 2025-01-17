## crp 工具

### 快速使用

#### 1. 在`package-crp.py`填写必要信息

``` python
userName = "xxxx" # crp用户名（过滤topic）
userId = "utxxxx" # crp用户id（登录id）
password = "xxxx" # 密码
```

#### 2. 安装

```bash
./install.sh
```

注:  后续要修改`package-crp.py`可以在`/usr/share/tools/package-crp.py`修改


#### 使用示例

```bash
# patch打包
# crp --topic <测试主题名> --name <要打包的项目名> --branch <包分支名>
crp --topic DDE-V25-20250116 --name deepin-desktop-theme-v25 --branch upstream/master

# 指定版本打包
# crp --topic <测试主题名> --name <要打包的项目名> --branch <包分支名> --tag <版本号>
crp branches --topic test --name deepin-desktop-theme-v25 --tag 1.1.1
```

### 常用命令

```bash

# 示例包名: deepin-desktop-theme
# 示例主题名: DDE-V25-20250116

# 模糊查包名
crp projects --name deepin-desktop-theme

# 模糊查测试主题名
crp topics --topic DDE-V25-20250116

# 查询指定测试主题下已经打包的包列表
crp instances --topic DDE-V25-20250116

# 查询指定测试主题下的指定包有哪些分支
crp branches --topic DDE-V25-20250116 --name deepin-desktop-theme-v25

```