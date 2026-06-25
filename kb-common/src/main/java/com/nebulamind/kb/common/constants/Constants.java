package com.nebulamind.kb.common.constants;

/**
 * 系统常量定义类。
 * 统一管理项目中的公共常量，避免魔法值散落在代码各处。
 *
 * @author NebulaMind
 */
public final class Constants {

    private Constants() {
        // 工具类，禁止实例化
    }

    /**
     * HTTP 请求头中传递的链路追踪 ID 的 key。
     */
    public static final String TRACE_ID_HEADER = "X-Trace-ID";

    /**
     * 默认租户 ID，用于未指定租户时的默认值。
     */
    public static final Long DEFAULT_TENANT_ID = 1L;
}