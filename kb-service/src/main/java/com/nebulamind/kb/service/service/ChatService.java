package com.nebulamind.kb.service.service;

import java.util.Map;

/**
 * 聊天服务接口。
 * 定义 AI 对话、问答等业务操作。
 *
 * @author NebulaMind
 */
public interface ChatService {

    // TODO: 定义聊天相关业务方法
    Map<String, Object> ask(Map<String, Object> request);
}