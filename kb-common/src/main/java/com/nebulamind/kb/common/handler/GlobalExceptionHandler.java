package com.nebulamind.kb.common.handler;

import com.nebulamind.kb.common.exception.BusinessException;
import com.nebulamind.kb.common.result.Result;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// 全局拦截所有Rest接口异常
@RestControllerAdvice
public class GlobalExceptionHandler {
    // 1. 捕获我们自己手动抛的业务异常 BusinessException
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusinessException(BusinessException e) {
        // 直接包装成统一失败返回体给前端
        return Result.fail(e.getCode(), e.getMessage());
    }

    // 2. 兜底：捕获所有未知系统异常（空指针、SQL错误、数组越界等）
    @ExceptionHandler(Exception.class)
    public Result<?> handleAllException(Exception e) {
        // 打印完整异常栈，方便后台排查bug
        e.printStackTrace();
        return Result.fail("5000", "系统异常，请联系管理员");
    }
}
