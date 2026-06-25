package com.nebulamind.kb.service.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * 异步任务线程池配置类。
 * 为 Spring @Async 注解提供自定义线程池，用于执行异步任务。
 *
 * @author NebulaMind
 */
@Configuration
@EnableAsync
public class AsyncConfig {

    /**
     * 配置异步任务线程池。
     * 核心线程数 10，最大线程数 20，队列容量 100。
     * 拒绝策略为 CallerRunsPolicy，当线程池满时由调用线程执行。
     *
     * @return 线程池执行器
     */
    @Bean(name = "asyncTaskExecutor")
    public Executor asyncTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-task-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.setWaitForTasksToCompleteOnShutdown(true);
        executor.setAwaitTerminationSeconds(60);
        executor.initialize();
        return executor;
    }
}