package com.nebulamind.kb.dao.config;

import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;
import lombok.extern.slf4j.Slf4j;
import org.apache.ibatis.reflection.MetaObject;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

/**
 * MyBatis-Plus 自动填充处理器
 * <p>
 * 功能说明：在执行 INSERT 和 UPDATE 操作时，自动填充公共字段（如创建时间、更新时间、操作人等），
 * 避免在业务代码中重复编写这些样板代码。
 * </p>
 * <p>
 * 使用前提：实体类中对应的字段需要加上 @TableField(fill = FieldFill.INSERT) 等注解，
 * 此处理器才能识别并填充。
 * </p>
 *
 * @author NebulaMind Team
 * @since 1.0.0
 */
@Slf4j
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {

    /**
     * INSERT 操作时自动填充
     * <p>
     * 触发时机：执行 mapper.insert(entity) 时，在 SQL 执行前被调用
     * </p>
     * <p>
     * 填充字段：
     * <ul>
     *     <li>createTime：当前时间</li>
     *     <li>updateTime：当前时间（插入时也初始化，便于后续按时间排序）</li>
     *     <li>createUserId：当前登录用户ID（暂用固定值，后续从 Token 获取）</li>
     *     <li>createUserName：当前登录用户名（暂用固定值，后续从 Token 获取）</li>
     *     <li>updateUserId：当前登录用户ID（暂用固定值）</li>
     * </ul>
     * </p>
     *
     * @param metaObject MyBatis-Plus 传入的元数据对象，包含实体类所有字段信息
     */
    @Override
    public void insertFill(MetaObject metaObject) {
        log.debug("执行 insertFill 自动填充");

        // 1. 填充时间字段
        this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, LocalDateTime.now());
        this.strictInsertFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());

        // 2. 获取当前用户信息
        // TODO: 当前为开发阶段，使用固定占位值。后续接入登录模块后，从 SecurityContextHolder 或 Token 中获取真实用户信息
        Long currentUserId = getCurrentUserId();
        String currentUserName = getCurrentUserName();

        // 3. 填充用户信息字段
        this.strictInsertFill(metaObject, "createUserId", Long.class, currentUserId);
        this.strictInsertFill(metaObject, "createUserName", String.class, currentUserName);
        this.strictInsertFill(metaObject, "updateUserId", Long.class, currentUserId);
    }

    /**
     * UPDATE 操作时自动填充
     * <p>
     * 触发时机：执行 mapper.updateById(entity) 时，在 SQL 执行前被调用
     * </p>
     * <p>
     * 填充字段：
     * <ul>
     *     <li>updateTime：当前时间</li>
     *     <li>updateUserId：当前登录用户ID</li>
     * </ul>
     * </p>
     * <p>
     * 注意：不更新 createTime 和 createUserId，因为它们是创建时一次性写入的，不应被后续更新覆盖
     * </p>
     *
     * @param metaObject MyBatis-Plus 传入的元数据对象
     */
    @Override
    public void updateFill(MetaObject metaObject) {
        log.debug("执行 updateFill 自动填充");

        // 1. 填充更新时间
        this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());

        // 2. 获取当前用户信息
        Long currentUserId = getCurrentUserId();

        // 3. 填充更新人ID
        this.strictUpdateFill(metaObject, "updateUserId", Long.class, currentUserId);
    }

    /**
     * 获取当前登录用户ID
     * <p>
     * 当前为开发阶段，返回固定占位值 1L。
     * 后续接入登录模块后，从 SecurityContextHolder 或 JWT Token 中解析获取。
     * </p>
     *
     * @return 当前用户ID
     */
    private Long getCurrentUserId() {
        // TODO: 后续从 SecurityContextHolder.getContext().getAuthentication() 或 Token 中获取
        return 1L;
    }

    /**
     * 获取当前登录用户名
     * <p>
     * 当前为开发阶段，返回固定占位值 "system"。
     * 后续接入登录模块后，从 SecurityContextHolder 或 JWT Token 中解析获取。
     * </p>
     *
     * @return 当前用户名
     */
    private String getCurrentUserName() {
        // TODO: 后续从 SecurityContextHolder.getContext().getAuthentication() 或 Token 中获取
        return "system";
    }
}