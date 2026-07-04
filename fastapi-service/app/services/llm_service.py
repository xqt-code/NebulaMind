from typing import List, Optional


class LLMService:
    """大语言模型服务

    封装 LLM 调用，支持多模型切换，提供统一的对话接口。
    """

    def chat(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """调用大语言模型进行对话

        TODO: 调用通义千问 API（DashScope），实现 LLM 对话功能

        技术方案：
        - 使用 dashscope SDK 调用 qwen-plus 模型
        - 支持 JSON Mode：强制模型输出结构化 JSON，便于后续解析
        - 支持 system_prompt 角色设定，控制模型行为
        - 预留多模型切换能力（通过配置项 llm_model 切换模型）

        抽象层的价值：
        - 解耦：上层业务（RagService）不依赖具体 LLM 实现，方便单元测试 Mock
        - 可切换：从通义千问切换到 OpenAI/文心一言只需修改本层，不影响上层
        - 面试讲：服务层抽象是「依赖倒置原则」的体现，上层依赖接口而非实现，
          当需要切换模型时，只需新增一个实现类，符合开闭原则

        Args:
            prompt: 用户提示词（包含上下文和问题）
            system_prompt: 系统提示词（角色设定）

        Returns:
            模型生成的回答文本
        """
        # TODO: 实现 LLM 调用
        raise NotImplementedError("LLMService.chat 尚未实现")