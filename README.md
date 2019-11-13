# PythonProject
自己的例子
git 使用说明
# 1. git init //初始化仓库
# 2. git add .(文件name) //添加文件到本地仓库

# 3. git commit -m "first commit" //添加文件描述信息

# 4. git remote add origin + 远程仓库地址 //链接远程仓库，创建主分支

# 5. git pull origin master // 把本地仓库的变化连接到远程仓库主分支
  git pull 失败 ,提示：fatal: refusing to merge unrelated histories

  其实这个问题是因为 两个 根本不相干的 git 库， 一个是本地库， 一个是远端库， 然后本地要去推送到远端， 远端觉得这个本地库跟自己不相干， 所以告知无法合并

  具体的方法， 一个种方法： 是 从远端库拉下来代码 ， 本地要加入的代码放到远端库下载到本地的库， 然后提交上去 ， 因为这样的话， 你基于的库就是远端的库，  这是一次update了

  第二种方法：
  使用这个强制的方法

  git pull origin master --allow-unrelated-histories

  后面加上 --allow-unrelated-histories ， 把两段不相干的 分支进行强行合并

# 6. git push -u origin master //把本地仓库的文件推送到远程仓库
