package com.nebulamind.kb.common.result;

/**
 * 统一返回状态码枚举。
 * 定义项目中常用的 HTTP 状态码及其对应的中文描述。
 *
 * @author NebulaMind
 */
public enum ResultCode {

    /**
     * 请求成功
     */
    SUCCESS("200", "成功"),

    /**
     * 请求参数错误
     */
    BAD_REQUEST("400", "请求参数错误"),

    /**
     * 未授权
     */
    UNAUTHORIZED("401", "未授权"),

    /**
     * 禁止访问
     */
    FORBIDDEN("403", "禁止访问"),

    /**
     * 资源不存在
     */
    NOT_FOUND("404", "资源不存在"),

    /**
     * 系统内部错误
     */
    INTERNAL_ERROR("500", "系统内部错误");

    /**
     * 状态码
     */
    private final String code;

    /**
     * 状态描述
     */
    private final String msg;

    ResultCode(String code, String msg) {
        this.code = code;
        this.msg = msg;
    }

    public String getCode() {
        return code;
    }

    public String getMsg() {
        return msg;
    }
}