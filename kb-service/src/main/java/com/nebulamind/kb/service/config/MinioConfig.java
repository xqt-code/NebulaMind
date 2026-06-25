package com.nebulamind.kb.service.config;

import io.minio.MinioClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * MinIO 对象存储配置类
 * <p>
 * 职责：创建 MinIO 客户端 Bean，供 Service 层注入使用
 * 配置来源：application-dev.yml 中的 minio 配置段
 * </p>
 */
@Configuration
public class MinioConfig {

    /**
     * MinIO 服务端地址
     * 例如：http://47.106.21.219:9000
     */
    @Value("${minio.endpoint}")
    private String endpoint;

    /**
     * MinIO 访问密钥（Access Key）
     * 对应登录控制台的用户名
     */
    @Value("${minio.access-key}")
    private String accessKey;

    /**
     * MinIO 秘密密钥（Secret Key）
     * 对应登录控制台的密码
     */
    @Value("${minio.secret-key}")
    private String secretKey;

    /**
     * 创建 MinIO 客户端 Bean
     * <p>
     * 在 Service 层通过 @Autowired 注入即可使用
     * </p>
     *
     * @return MinioClient 实例
     */
    @Bean
    public MinioClient minioClient() {
        return MinioClient.builder()
                .endpoint(endpoint)
                .credentials(accessKey, secretKey)
                .build();
    }
}