package com.nebulamind.kb.exception;

import com.nebulamind.kb.common.exception.BusinessException;
import com.nebulamind.kb.common.result.Result;
import com.nebulamind.kb.common.result.ResultCode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.stream.Collectors;

/**
 * 全局异常处理器。
 * 统一捕获 Controller 层抛出的异常，返回标准 Result 格式的响应。
 *
 * @author NebulaMind
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * 处理业务异常。
     * 将 BusinessException 转换为 Result 统一返回格式。
     *
     * @param e 业务异常
     * @return 失败结果
     */
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusinessException(BusinessException e) {
        log.warn("业务异常: code={}, message={}", e.getCode(), e.getMessage());
        return Result.fail(e.getMessage());
    }

    /**
     * 处理参数校验异常。
     * 提取字段级别的校验错误信息并返回。
     *
     * @param e 参数校验异常
     * @return 包含校验错误详情的失败结果
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<?> handleValidationException(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
                .map(fieldError -> fieldError.getField() + ": " + fieldError.getDefaultMessage())
                .collect(Collectors.joining("; "));
        log.warn("参数校验失败: {}", msg);
        return Result.fail(ResultCode.BAD_REQUEST, msg);
    }

    /**
     * 处理未知异常。
     * 兜底处理所有未捕获的异常，返回系统内部错误。
     *
     * @param e 异常
     * @return 系统内部错误结果
     */
    @ExceptionHandler(Exception.class)
    public Result<?> handleException(Exception e) {
        log.error("系统异常: ", e);
        return Result.fail(ResultCode.INTERNAL_ERROR);
    }
}