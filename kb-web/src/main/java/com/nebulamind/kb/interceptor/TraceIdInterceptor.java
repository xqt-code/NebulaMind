package com.nebulamind.kb.interceptor;

import com.nebulamind.kb.common.constants.Constants;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.UUID;

/**
 * 链路追踪拦截器。
 * 在每个请求到达时，从请求头中提取或生成 Trace ID，
 * 放入 MDC 和 ThreadLocal，并设置到响应头中。
 * 请求结束后清除 MDC 和 ThreadLocal 中的 Trace ID。
 *
 * @author NebulaMind
 */
@Component
public class TraceIdInterceptor implements HandlerInterceptor {

    /**
     * 用于在当前线程中传递 Trace ID 的 ThreadLocal。
     */
    private static final ThreadLocal<String> TRACE_ID_HOLDER = new ThreadLocal<>();

    /**
     * 请求前置处理。
     * 从请求头获取 X-Trace-ID，若无则生成 UUID，放入 MDC 和 ThreadLocal，
     * 并设置到响应头中。
     *
     * @param request  当前 HTTP 请求
     * @param response 当前 HTTP 响应
     * @param handler  处理器
     * @return true 继续执行
     */
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String traceId = request.getHeader(Constants.TRACE_ID_HEADER);
        if (traceId == null || traceId.isEmpty()) {
            traceId = UUID.randomUUID().toString().replace("-", "");
        }
        TRACE_ID_HOLDER.set(traceId);
        MDC.put("traceId", traceId);
        response.setHeader(Constants.TRACE_ID_HEADER, traceId);
        return true;
    }

    /**
     * 请求完成后处理。
     * 清除 ThreadLocal 和 MDC 中的 Trace ID，防止内存泄漏。
     *
     * @param request  当前 HTTP 请求
     * @param response 当前 HTTP 响应
     * @param handler  处理器
     * @param ex       异常（如有）
     */
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) {
        TRACE_ID_HOLDER.remove();
        MDC.remove("traceId");
    }

    /**
     * 获取当前线程的 Trace ID。
     *
     * @return 当前 Trace ID，可能为 null
     */
    public static String getTraceId() {
        return TRACE_ID_HOLDER.get();
    }
}