# chai · 内容拆解 Skill

从作品链接、本地视频或图片出发，依据实际证据分析内容结构、创作原理和观众反应，整理可迁移的制作要求。

Skill 位于 [`skills/douyin-content-breakdown`](skills/douyin-content-breakdown/SKILL.md)。将该文件夹安装到所用环境支持的 skills 目录后调用：

```text
$douyin-content-breakdown 拆解这个链接：https://v.douyin.com/你的作品链接/
```

也可提供本地视频路径，或要求整理一份创作指南。输出包含读取范围、时间轴证据、分析假设与制作要求。默认使用中文，不操作剪映。

这是供 agent 执行的工作流，不是独立的视频理解服务。浏览器、音视频理解和转写依赖调用环境实际可用的能力；只有封面或标题时不会生成虚假的完整拆解。本地辅助脚本需要 Python 3 与 FFmpeg（ffprobe / ffmpeg），提供元数据、抽帧和可选音轨导出，不含语音识别模型。

参考材料的阅读／核验状态见 [来源登记](skills/douyin-content-breakdown/references/source-register.md)。原始第三方教材及用户媒体未上传。
