package com.nebulamind.kb.common.exception;

/**
 * 业务异常类。
 * 用于封装业务逻辑中的异常，包含错误码和错误信息，方便统一异常处理。
 *
 * @author NebulaMind
 */
public class BusinessException extends RuntimeException {

    /**
     * 错误码
     */
    private final String code;

    /**
     * 错误信息
     */
    private final String message;

    /**
     * 使用错误码和错误信息构造业务异常。
     *
     * @param code    错误码
     * @param message 错误信息
     */
    public BusinessException(String code, String message) {
        super(message);
        this.code = code;
        this.message = message;
    }

    /**
     * 使用错误码枚举构造业务异常。
     *
     * @param resultCode 错误码枚举
     */
    public BusinessException(com.nebulamind.kb.common.result.ResultCode resultCode) {
        super(resultCode.getMsg());
        this.code = resultCode.getCode();
        this.message = resultCode.getMsg();
    }

    /**
     * 使用错误码枚举和自定义错误信息构造业务异常。
     *
     * @param resultCode 错误码枚举
     * @param message    自定义错误信息
     */
    public BusinessException(com.nebulamind.kb.common.result.ResultCode resultCode, String message) {
        super(message);
        this.code = resultCode.getCode();
        this.message = message;
    }

    public String getCode() {
        return code;
    }

    @Override
    public String getMessage() {
        return message;
    }
}