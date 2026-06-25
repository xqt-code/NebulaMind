package com.nebulamind.kb.config;

import com.nebulamind.kb.common.constants.Constants;
import io.netty.channel.ChannelOption;
import org.slf4j.MDC;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;

/**
 * WebClient 配置类。
 * 创建统一的 WebClient.Builder Bean，配置超时和链路追踪请求头注入。
 *
 * @author NebulaMind
 */
@Configuration
public class WebClientConfig {

    /**
     * 创建 WebClient.Builder Bean。
     * 配置连接超时 5 秒、读取超时 30 秒，
     * 并自动在请求头中注入 X-Trace-ID。
     *
     * @return WebClient.Builder 实例
     */
    @Bean
    public WebClient.Builder webClientBuilder() {
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000)
                .responseTimeout(Duration.ofSeconds(30));

        return WebClient.builder()
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .filter(traceIdFilter());
    }

    /**
     * 链路追踪过滤器。
     * 在发起请求时，从 MDC 中获取当前 Trace ID 并添加到请求头。
     *
     * @return ExchangeFilterFunction 实例
     */
    private ExchangeFilterFunction traceIdFilter() {
        return ExchangeFilterFunction.ofRequestProcessor(request -> {
            String traceId = MDC.get("traceId");
            if (traceId != null && !traceId.isEmpty()) {
                return reactor.core.publisher.Mono.just(
                        ClientRequest.from(request)
                                .header(Constants.TRACE_ID_HEADER, traceId)
                                .build()
                );
            }
            return reactor.core.publisher.Mono.just(request);
        });
    }
}