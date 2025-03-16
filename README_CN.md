![cover-v5-optimized](https://github.com/langgenius/dify/assets/13230914/f9e19af5-61ba-4119-b926-d10c4c06ebab)

<div align="center">
  <a href="https://cloud.dify.ai">Dify 云服务</a> ·
  <a href="https://docs.dify.ai/getting-started/install-self-hosted">自托管</a> ·
  <a href="https://docs.dify.ai">文档</a> ·
  <a href="https://udify.app/chat/22L1zSxg6yW1cWQg">（需用英文）常见问题解答 / 联系团队</a>
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

Dify 是一个开源的 LLM 应用开发平台。其直观的界面结合了 AI 工作流、RAG 管道、Agent、模型管理、可观测性功能等，让您可以快速从原型到生产。以下是其核心功能列表：
<br> </br>
**1. 工作流**: 
<br>  在画布上构建和测试功能强大的 AI 工作流程，利用以下所有功能以及更多功能。
<br>**2. 全面的模型支持**: 
<br>  与数百种专有/开源 LLMs 以及数十种推理提供商和自托管解决方案无缝集成，涵盖 GPT、Mistral、Llama3 以及任何与 OpenAI API 兼容的模型。完整的支持模型提供商列表可在[此处](https://docs.dify.ai/getting-started/readme/model-providers)找到。
<br>**3. Prompt IDE**: 
<br>  用于制作提示、比较模型性能以及向基于聊天的应用程序添加其他功能（如文本转语音）的直观界面。
<br>**4. RAG Pipeline**: 
<br>  广泛的 RAG 功能，涵盖从文档摄入到检索的所有内容，支持从 PDF、PPT 和其他常见文档格式中提取文本的开箱即用的支持。
<br>**5. Agent 智能体**: 
<br>  您可以基于 LLM 函数调用或 ReAct 定义 Agent，并为 Agent 添加预构建或自定义工具。Dify 为 AI Agent 提供了50多种内置工具，如谷歌搜索、DALL·E、Stable Diffusion 和 WolframAlpha 等。
<br>**6. LLMOps**: 
<br>  随时间监视和分析应用程序日志和性能。您可以根据生产数据和标注持续改进提示、数据集和模型。
<br>**7. 后端即服务**: 
<br>  所有 Dify 的功能都带有相应的 API，因此您可以轻松地将 Dify 集成到自己的业务逻辑中。
<br> </br>

## 使用 Dify
<br> </br>

- **云 </br>**
Dify官方提供[ Dify 云服务](https://dify.ai)，任何人都可以零设置尝试。它提供了自部署版本的所有功能，并在沙盒计划中包含 200 次免费的 GPT-4 调用。

- 本项目是基于社区版的,需要以源代码方式部署运行
- **自托管 Dify 社区版</br>**


在 GitHub 上给 Dify Star，并立即收到新版本的通知。

![star-us](https://github.com/langgenius/dify/assets/13230914/b823edc1-6388-4e25-ad45-2f6b187adbb4)

## 安装社区版

### 系统要求

在安装 Dify 之前，请确保您的机器满足以下最低系统要求：

- CPU >= 2 Core
- RAM >= 4 GiB

### 使用源码部署方式请按下面步骤

```bash
cd docker
cp .env.example .env
docker compose up -d
```

## Contributing

对于那些想要贡献代码的人，请参阅我们的[贡献指南](https://github.com/langgenius/dify/blob/main/CONTRIBUTING.md)。
同时，请考虑通过社交媒体、活动和会议来支持 Dify 的分享。

> 我们正在寻找贡献者来帮助将Dify翻译成除了中文和英文之外的其他语言。如果您有兴趣帮助，请参阅我们的[i18n README](https://github.com/langgenius/dify/blob/main/web/i18n/README.md)获取更多信息，并在我们的[Discord社区服务器](https://discord.gg/8Tpq4AcN9c)的`global-users`频道中留言。

**Contributors**

<a href="https://github.com/langgenius/dify/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=langgenius/dify" />
</a>

## 社区与支持

我们欢迎您为 Dify 做出贡献，以帮助改善 Dify。包括：提交代码、问题、新想法，或分享您基于 Dify 创建的有趣且有用的 AI 应用程序。同时，我们也欢迎您在不同的活动、会议和社交媒体上分享 Dify。

## 安全问题

为了保护您的隐私，请避免在 GitHub 上发布安全问题。发送问题至 security@dify.ai，我们将为您做更细致的解答。

## License

本仓库遵循 [Dify Open Source License](LICENSE) 开源协议，该许可证本质上是 Apache 2.0，但有一些额外的限制。
