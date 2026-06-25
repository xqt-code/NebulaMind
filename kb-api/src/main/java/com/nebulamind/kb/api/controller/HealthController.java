package com.nebulamind.kb.api.controller;

import com.nebulamind.kb.common.result.Result;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 健康检查控制器。
 * 提供系统健康状态检查接口，用于监控和探活。
 *
 * @author NebulaMind
 */
@Tag(name = "健康检查", description = "系统健康状态检查接口")
@RestController
@RequestMapping("/api/v1/health")
public class HealthController {

    /**
     * 健康检查。
     * 返回系统当前运行状态。
     *
     * @return 系统状态
     */
    @Operation(summary = "健康检查")
    @GetMapping("/health")
    public Result<String> health() {
        // TODO: 可扩展检查数据库、Redis 等依赖组件的连通性
        return Result.success("UP");
    }
}