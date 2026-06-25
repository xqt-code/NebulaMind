package com.nebulamind.kb.dao.config;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.TenantLineInnerInterceptor;
import net.sf.jsqlparser.expression.Expression;
import net.sf.jsqlparser.expression.LongValue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * MyBatis-Plus 配置类。
 * 统一配置分页插件、多租户插件以及逻辑删除全局配置。
 *
 * @author NebulaMind
 */
@Configuration
public class MyBatisPlusConfig {

    /**
     * 配置 MyBatis-Plus 拦截器链。
     * 包含分页插件和多租户插件。
     *
     * @return MybatisPlusInterceptor 实例
     */
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();

        // 分页插件：支持 MySQL 分页查询
        PaginationInnerInterceptor paginationInterceptor = new PaginationInnerInterceptor(DbType.MYSQL);
        // 设置最大单页限制条数，防止大数据量查询
        paginationInterceptor.setMaxLimit(1000L);
        interceptor.addInnerInterceptor(paginationInterceptor);

        // 多租户插件：自动在 SQL 中追加租户 ID 条件
        // 租户 ID 从当前请求上下文（如 ThreadLocal、Header）中获取
        TenantLineInnerInterceptor tenantInterceptor = new TenantLineInnerInterceptor(() -> {
            // TODO: 从上下文（如 ThreadLocal、Token 等）获取当前租户 ID
            // 示例：return new LongValue(TenantContextHolder.getCurrentTenantId());
            return new LongValue(1L);
        });
        interceptor.addInnerInterceptor(tenantInterceptor);

        return interceptor;
    }
}