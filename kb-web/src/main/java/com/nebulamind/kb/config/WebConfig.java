package com.nebulamind.kb.config;

import com.nebulamind.kb.interceptor.TraceIdInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web MVC 配置类。
 * 注册拦截器和配置跨域资源共享（CORS）。
 *
 * @author NebulaMind
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    private final TraceIdInterceptor traceIdInterceptor;

    public WebConfig(TraceIdInterceptor traceIdInterceptor) {
        this.traceIdInterceptor = traceIdInterceptor;
    }

    /**
     * 注册拦截器。
     * 将 TraceIdInterceptor 添加到拦截器链中，拦截所有请求。
     *
     * @param registry 拦截器注册表
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(traceIdInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/api/v1/health/**");
    }

    /**
     * 配置跨域资源共享。
     * 开发环境允许所有源、所有方法和所有请求头。
     *
     * @param registry CORS 注册表
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("*")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);
    }
}