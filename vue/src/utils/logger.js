// src/utils/logger.js

// 简单日志工具，开发时输出到控制台
export function getLogger(module) {
    return {
        debug: (...args) => console.debug(`[${module}]`, ...args),
        info: (...args) => console.info(`[${module}]`, ...args),
        warn: (...args) => console.warn(`[${module}]`, ...args),
        error: (...args) => console.error(`[${module}]`, ...args),
    };
}

// 默认导出（兼容不同导入方式）
export default { getLogger };