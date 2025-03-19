![cover-v5-optimized](https://github.com/langgenius/dify/assets/13230914/f9e19af5-61ba-4119-b926-d10c4c06ebab)

<div align="center">
  <a href="https://docs.dify.ai/getting-started/install-self-hosted">自托管</a> ·
  <a href="https://docs.dify.ai">文档</a> ·
</div>

<p align="center">
    <a href="https://dify.ai" target="_blank">
        <img alt="Static Badge" src="https://img.shields.io/badge/Product-F04438"></a>
    <a href="https://dify.ai/pricing" target="_blank">
        <img alt="Static Badge" src="https://img.shields.io/badge/free-pricing?logo=free&color=%20%23155EEF&label=pricing&labelColor=%20%23528bff"></a>
    <a href="https://discord.gg/FngNHpbcY7" target="_blank">
        <img src="https://img.shields.io/discord/1082486657678311454?logo=discord&labelColor=%20%235462eb&logoColor=%20%23f5f5f5&color=%20%235462eb"
            alt="chat on Discord"></a>
    <a href="https://reddit.com/r/difyai" target="_blank">  
        <img src="https://img.shields.io/reddit/subreddit-subscribers/difyai?style=plastic&logo=reddit&label=r%2Fdifyai&labelColor=white"
            alt="join Reddit"></a>
    <a href="https://twitter.com/intent/follow?screen_name=dify_ai" target="_blank">
        <img src="https://img.shields.io/twitter/follow/dify_ai?logo=X&color=%20%23f5f5f5"
            alt="follow on X(Twitter)"></a>
    <a href="https://hub.docker.com/u/langgenius" target="_blank">
        <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/langgenius/dify-web?labelColor=%20%23FDB062&color=%20%23f79009"></a>
    <a href="https://github.com/langgenius/dify/graphs/commit-activity" target="_blank">
        <img alt="Commits last month" src="https://img.shields.io/github/commit-activity/m/langgenius/dify?labelColor=%20%2332b583&color=%20%2312b76a"></a>
    <a href="https://github.com/langgenius/dify/" target="_blank">
        <img alt="Issues closed" src="https://img.shields.io/github/issues-search?query=repo%3Alanggenius%2Fdify%20is%3Aclosed&label=issues%20closed&labelColor=%20%237d89b0&color=%20%235d6b98"></a>
    <a href="https://github.com/langgenius/dify/discussions/" target="_blank">
        <img alt="Discussion posts" src="https://img.shields.io/github/discussions/langgenius/dify?labelColor=%20%239b8afb&color=%20%237a5af8"></a>
</p>

<div align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./README_CN.md"><img alt="简体中文版自述文件" src="https://img.shields.io/badge/简体中文-d9d9d9"></a>
</div>


#

<div align="center">
  <a href="https://trendshift.io/repositories/2152" target="_blank"><img src="https://trendshift.io/api/badge/repositories/2152" alt="langgenius%2Fdify | 趋势转变" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>

本项目源自 <a href="https://github.com/langgenius/dify">Dify</a> 这个开源LLM 应用开发平台项目, 并参考将Dify项目元数据库postgres迁移到MySQL的<a href="https://github.com/oceanbase-devhub/dify">oceanbase-devhub/dify</a>项目, 将该项目元数据库适配到Oracle
数据库(目前适配Dify自托管 社区版的<a href="https://github.com/langgenius/dify/tree/0.14.2">0.14.2</a>版本),适配供学习和参考。

## 安装部署
目前仅支持使用源码部署方式部署
### 1、Clone Dify 
获得源码
```bash
git https://github.com/art-jin/dify-oracle.git
```

启动容器:
在启用业务服务之前，我们需要先部署 Oracle / Redis ，可以使用以下命令启动它们：
```bash
cd docker
cp middleware.env.example middleware.env
docker compose -f docker-compose.middleware.yaml up -d
docker compose -f docker-compose.middleware.yaml up -d oracle
```
启动oracle容器,会拉取oracle 23ai free的镜像,并且执行/docker/startupscripts/init_user.script脚本。
创建两个用户: 用户difyMeta0142,用于元数据库表的搭建。 用户dify,用于向量库的搭建。

### 2、Server Deployment
源代码的部署步骤,参考自Dify文档: <a href="https://docs.dify.ai/getting-started/install-self-hosted/local-source-code">Start with Local Source Code</a>, 并在差异部分做详细说明.
#### 2.1、Installation of the basic environment:
Server startup requires Python 3.12. It is recommended to use pyenv for quick installation of the Python environment.<br>
To install additional Python versions, use pyenv install.
```bash
pyenv install 3.12
```
To switch to the "3.12" Python environment, use the following command:
```bash
pyenv global 3.12
```

#### 2.2 Follow these steps :
1、
```bash
cd api
```
2、.env.example中,已经将默认向量数据库,配置为oracle
```bash
cp .env.example .env
```
3、 :
```bash
awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env
```
4、Dify API service uses <a href="https://python-poetry.org/docs/">Poetry</a> to manage dependencies.:
需要先安装Poetry, 还要再安装poetry shell插件.
```bash
poetry self add poetry-plugin-shell : https://github.com/python-poetry/poetry-plugin-shell
```
然后按照Dify文档步骤继续执行如下命令
```bash
poetry shell
poetry env use 3.12
poetry install
```

5 :Perform the database migration:<br>
Perform database migration to the latest version:
```bash
poetry run flask db upgrade
```
这一步会通过/api/migrations/下的脚步,创建元数据库表.

#### 2.3 Start the API server:

```bash
poetry run flask run --host 0.0.0.0 --port=5001 --debug
```

#### 2.4 Start the Worker service

```bash
poetry run celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q dataset,generation,mail,ops_trace
```
### 3、Deploy the frontend page

#### 3.1、Enter the web directory
```bash
cd web
```

#### 3.2、Install the dependencies.
```bash
npm install
```

#### 3.3、 Build the code
```bash
npm run build
```

#### 3.4、Start the web service
```bash
npm run start
```
## Contributing

## License

本仓库遵循 [Dify Open Source License](LICENSE) 开源协议，该许可证本质上是 Apache 2.0，但有一些额外的限制。
