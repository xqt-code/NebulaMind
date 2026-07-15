package com.nebulamind.kb.service.service.impl;

import com.nebulamind.kb.service.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Map;

/**
 * 聊天服务实现类。
 * 提供 AI 对话、问答等业务逻辑实现。
 *
 * @author NebulaMind
 */
@Service
public class ChatServiceImpl implements ChatService {

    // TODO: 实现聊天相关业务方法
    private final WebClient webClient;

    // 构造器注入（推荐，不要用 @Autowired 字段注入）
    public ChatServiceImpl(WebClient.Builder webClientBuilder) {
        // 配置专属于 AI 引擎的超时和重试（生产级细节）
        this.webClient = webClientBuilder
                .baseUrl("http://localhost:8000")
                .defaultHeader("Content-Type", "application/json")
                .build();
    }

    /**
     * 业务层方法：专门负责调用 FastAPI
     */
    public Map<String, Object> ask(Map<String, Object> request) {
        try {
            // 🔥 第1步：发起 POST 请求，指定路径（baseUrl 已经在构造器里配好了）
            return webClient.post()
                    // 指定接口路径（拼接 baseUrl => http://localhost:8000/api/v1/chat/ask）
                    .uri("/api/v1/chat/ask")
                    // 把 Spring 接收到的参数（Map）直接作为 JSON Body 发给 FastAPI
                    .bodyValue(request)
                    // 🔥 第2步：retrieve() 意为“检索响应”，区别于 exchange()（后者要手动释放资源）
                    .retrieve()

                    // 🔥 第3步：【核心企业级增强】onStatus 拦截 HTTP 状态码
                    // 如果 FastAPI 返回 4xx（客户端错误）或 5xx（服务端错误）
                    .onStatus(HttpStatusCode::isError, response -> {
                        // 这里的 response 包含状态码和错误体
                        // 为了不丢失错误细节，你可以尝试读取 response.bodyToMono(String.class)
                        // 这里直接抛出一个带有状态码的运行时异常
                        String errorMsg = String.format(
                                "AI引擎响应异常，状态码: %d, 路径: %s",
                                response.statusCode().value(),
                                "/api/v1/chat/ask"
                        );
                        // Mono.error 创建了一个包含异常的反应流（Reactive Stream）
                        return Mono.error(new RuntimeException(errorMsg));
                    })

                    // 🔥 第4步：声明响应的反序列化类型（因为是异构系统，用 Map 最灵活）
                    // 如果是强类型，这里可以写 .bodyToMono(AiResponseDto.class)
                    .bodyToMono(Map.class)

                    // 🔥 第5步：【终极痛点】block() 将“反应式异步”转为“同步阻塞”
                    // WebClient 默认是非阻塞的（Netty），但你的 Tomcat 是阻塞的（Servlet）
                    // 调用 block() 表示：当前 Tomcat 线程在这里“等着”，直到 FastAPI 返回结果
                    // ⚠️ 注意：block() 不加参数会无限等待，必须加超时！
                    .block(Duration.ofSeconds(120)); // 最多等 120 秒，超时抛异常
        } catch (Exception e) {
            // 可以在这里做降级处理（比如返回缓存）
            throw new RuntimeException("调用 AI 引擎失败: " + e.getMessage(), e);
        }
    }
}