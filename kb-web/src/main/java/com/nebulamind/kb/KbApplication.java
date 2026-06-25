package com.nebulamind.kb;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.ApplicationContext;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * NebulaMind 知识库管理系统启动类。
 * 项目入口，负责引导 Spring Boot 应用的启动，
 * 并启用异步任务支持和 MyBatis Mapper 扫描。
 *
 * @author NebulaMind
 */
@SpringBootApplication(scanBasePackages = "com.nebulamind.kb")
@EnableAsync
@MapperScan("com.nebulamind.kb.dao.mapper")
public class KbApplication {

    public static void main(String[] args) {

        SpringApplication.run(KbApplication.class, args);

//        ApplicationContext context = SpringApplication.run(KbApplication.class, args);

        // 打印所有 Bean 名称
//        String[] beanNames = context.getBeanDefinitionNames();
//        System.out.println("===== 当前 IOC 容器中的 Bean 数量: " + beanNames.length + " =====");
//        for (String name : beanNames) {
//            System.out.println(name);
//        }
    }
}