package com.nebulamind.kb.api.controller;

import com.nebulamind.kb.common.result.Result;
import com.nebulamind.kb.service.dto.AskRequest;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 聊天控制器。
 * 提供基于知识库的智能问答接口。
 *
 * @author NebulaMind
 */
@Tag(name = "智能问答", description = "基于知识库的 AI 问答接口")
@RestController
@RequestMapping("/api/v1/chat")
public class ChatController {

    /**
     * 智能问答。
     * 接收用户提问，基于知识库进行语义检索和 AI 回答。
     *
     * @param request 问答请求参数
     * @return AI 回答结果
     */
    @Operation(summary = "智能问答")
    @PostMapping("/ask")
    public Result<Void> ask(@RequestBody AskRequest request) {
        // TODO: 实现智能问答逻辑，调用 RAG 检索和 LLM 生成
        return Result.success(null);
    }
}