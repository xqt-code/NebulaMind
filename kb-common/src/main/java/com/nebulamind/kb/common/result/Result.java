package com.nebulamind.kb.common.result;

/**
 * 统一返回结果封装类。
 * 用于 Controller 层统一返回格式，包含状态码、提示信息和数据体。
 *
 * @param <T> 返回数据的类型
 * @author NebulaMind
 */
public class Result<T> {

    /**
     * 状态码
     */
    private String code;

    /**
     * 提示信息
     */
    private String msg;

    /**
     * 返回数据
     */
    private T data;

    public Result() {
    }

    public Result(String code, String msg, T data) {
        this.code = code;
        this.msg = msg;
        this.data = data;
    }

    /**
     * 返回成功结果，默认提示信息为"成功"。
     *
     * @param data 返回数据
     * @param <T>  数据类型
     * @return 成功结果
     */
    public static <T> Result<T> success(T data) {
        return new Result<>(ResultCode.SUCCESS.getCode(), ResultCode.SUCCESS.getMsg(), data);
    }

    /**
     * 返回成功结果，自定义提示信息。
     *
     * @param msg  提示信息
     * @param data 返回数据
     * @param <T>  数据类型
     * @return 成功结果
     */
    public static <T> Result<T> success(String msg, T data) {
        return new Result<>(ResultCode.SUCCESS.getCode(), msg, data);
    }

    /**
     * 返回失败结果，使用默认状态码 500。
     *
     * @param msg 提示信息
     * @param <T> 数据类型
     * @return 失败结果
     */
    public static <T> Result<T> fail(String msg) {
        return new Result<>(ResultCode.INTERNAL_ERROR.getCode(), msg, null);
    }

    /**
     * 返回失败结果，使用指定的错误码枚举。
     *
     * @param resultCode 错误码枚举
     * @param <T>        数据类型
     * @return 失败结果
     */
    public static <T> Result<T> fail(ResultCode resultCode) {
        return new Result<>(resultCode.getCode(), resultCode.getMsg(), null);
    }

    /**
     * 返回失败结果，使用指定的错误码枚举，自定义提示信息。
     *
     * @param resultCode 错误码枚举
     * @param msg        提示信息
     * @param <T>        数据类型
     * @return 失败结果
     */
    public static <T> Result<T> fail(ResultCode resultCode, String msg) {
        return new Result<>(resultCode.getCode(), msg, null);
    }
    /**
     * 返回失败结果，使用自定义的错误码，自定义提示信息。
     *
     * @param code       其他错误码
     * @param msg        提示信息
     * @param <T>        数据类型
     * @return 失败结果
     */
    public static <T> Result<T> fail(String code, String msg) {
        return new Result<>(code, msg, null);
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }
}