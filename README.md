# chai · 内容拆解 Skill

从作品链接、本地视频或图片出发，依据实际证据分析内容结构、创作原理和观众反应，整理可迁移的制作要求。

范围限定为面向中国大陆抖音发布的图文与短视频。推荐与热点策略只采用抖音依据，不移植其他平台流量逻辑。一般传播/动机研究明确标为内容设计参考，不构成抖音算法结论。

Skill 位于 [`skills/douyin-content-breakdown`](skills/douyin-content-breakdown/SKILL.md)。将该文件夹安装到所用环境支持的 skills 目录后调用：

```text
$douyin-content-breakdown 拆解这个链接：https://v.douyin.com/你的作品链接/
```

也可提供本地视频路径，或要求整理一份创作指南。输出包含读取范围、时间轴证据、分析假设与制作要求。默认使用中文，不操作剪映。

图文按页序拆解；短视频按实际读取的时间片段分析。要求下一条时默认给约三个实质不同的策划示例；需要Excel时交付“创作指导、下一条策划、原片拆解”三表，证据和验证资料保留在用户本地内部记录。UGC参与设计按任务选用，不强制每条作品做共创。

这是供 agent 执行的工作流，不是独立的视频理解服务。浏览器、音视频理解和转写依赖调用环境实际可用的能力；只有封面或标题时不会生成虚假的完整拆解。本地辅助脚本需要 Python 3 与 FFmpeg（ffprobe / ffmpeg），提供元数据、抽帧和可选音轨导出，不含语音识别模型。

参考材料的阅读／核验状态见 [来源登记](skills/douyin-content-breakdown/references/source-register.md)。原始第三方教材及用户媒体未上传。

维护时按 [定向回归用例](skills/douyin-content-breakdown/references/evaluation-cases.md) 检查新增能力，区分文档校验、受控情境回答和真实媒体/Excel端到端运行。
