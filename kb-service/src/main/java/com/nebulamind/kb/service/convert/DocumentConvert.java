package com.nebulamind.kb.service.convert;

import com.nebulamind.kb.dao.entity.Document;
import com.nebulamind.kb.service.dto.DocumentResponse;
import com.nebulamind.kb.service.dto.DocumentUploadRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;

/**
 * 文档对象转换器（MapStruct）。
 *
 * 职责：集中管理文档相关的所有 DTO ↔ Entity 转换。
 *
 * =========================================================================
 * 为什么需要 Convertor 层？（企业级规范的核心问题）
 * =========================================================================
 * 1. 安全性：Entity 包含 storageFileName（存储路径）、tenantId（租户ID）等内部字段，
 *    直接暴露给前端会造成安全隐患。
 * 2. 解耦：数据库表结构变更（如字段改名），只要 DTO 不变，前端就无需改动。
 * 3. 灵活性：可以组合多张表的数据，或对字段进行格式化（如日期转字符串）。
 * 4. 性能：MapStruct 编译期生成代码，等价于手写 setter，无反射损耗。
 *
 * =========================================================================
 * MapStruct vs BeanUtils（为什么选 MapStruct？）
 * =========================================================================
 * | 特性          | BeanUtils (反射)          | MapStruct (编译期生成)     |
 * |---------------|---------------------------|---------------------------|
 * | 执行方式       | 运行时反射                 | 编译期生成 .class 代码     |
 * | 性能          | 慢（有反射开销）           | 快（等价于手写 setter）    |
 * | 字段名不匹配   | 静默失败（不报错）         | 编译期报错（强制修正）     |
 * | 类型不匹配     | 运行时 ClassCastException | 编译期报错                 |
 * | 调试          | 困难（看不见转换过程）     | 可以看生成的代码           |
 *
 * =========================================================================
 * 核心配置说明
 * =========================================================================
 * componentModel = "spring"
 *   → 让 Spring 管理该 Mapper 实例，可在 Service 层用 @Autowired 注入。
 *
 * nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
 *   → 更新操作时，如果 DTO 中某个字段为 null，不覆盖 Entity 的原有值。
 *   → 解决了“部分更新时，未传字段被置 null”的经典问题。
 *
 * @author NebulaMind
 */
@Mapper(
        componentModel = "spring",
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface DocumentConvert {

    // ================================================================
    // 场景1：上传（前端 → 数据库）
    // ================================================================

    /**
     * 【正向转换】将前端上传 DTO 转换为数据库实体。
     *
     * 使用时机：用户上传文档时，将 DocumentUploadRequest 转为 Document 实体。
     *
     * 映射规则：
     *   - 自动映射：字段名相同、类型相同的字段（如 originalFileName、fileSize、mimeType）。
     *   - 忽略字段：Document 实体中有，但 DTO 中没有的字段（如 storageFileName、fileUrl、parseStatus），
     *     由 Service 层在后续逻辑中手动赋值。
     *
     * 你已有的方法，保持不变。
     *
     * @param uploadRequest 前端上传请求 DTO（包含文件元数据）
     * @return Document 数据库实体（待补充业务字段后入库）
     */
    Document toEntity(DocumentUploadRequest uploadRequest);

    // ================================================================
    // 场景2：查询详情（数据库 → 前端）
    // ================================================================

    /**
     * 【查询详情转换】将数据库 Document 实体转换为 DocumentResponse DTO。
     *
     * 使用时机：GET /api/v1/documents/{id} 接口返回。
     *
     * 映射规则：
     *   - 自动映射：字段名相同、类型相同的字段（id、originalFileName、fileSize、fileUrl）。
     *   - 特殊处理：
     *       - parseStatus：如果数据库里没有该字段，Service 层会手动填充默认值（PENDING）。
     *       - parseResult：详情页需要返回大 JSON 数据，此处正常映射。
     *
     * 为什么需要单独的 toResponse() 而不是复用 toDTO()？
     *   因为 DocumentUploadRequest 是“输入型 DTO”，包含 MultipartFile 等上传专用字段；
     *   DocumentResponse 是“输出型 DTO”，包含解析状态、进度、结果等查询专用字段。
     *   两者职责不同，强行复用会造成字段污染。
     *
     * @param entity 数据库实体（包含所有业务字段）
     * @return DocumentResponse 前端需要的响应 DTO
     */
    @Mapping(target = "parseStatus", ignore = true)   // 由 Service 层手动填充
    @Mapping(target = "parseProgress", ignore = true) // 由 Service 层手动填充
    @Mapping(target = "errorMessage", ignore = true)  // 由 Service 层手动填充
    DocumentResponse toResponse(Document entity);

    // ================================================================
    // 场景3：更新（前端 → 已有数据库实体）【可选，但强烈建议保留】
    // ================================================================

    /**
     * 【更新转换】将前端 DTO 的字段合并到已有的数据库实体（支持部分更新）。
     *
     * 使用时机：PUT /api/v1/documents/{id} 接口，用户修改文档备注或分类时。
     *
     * 核心机制说明：
     *   - @MappingTarget 注解：表示这是一个“目标对象”，不是“新建对象”。
     *   - 配合 IGNORE 策略：如果 DTO 中某个字段为 null，则不覆盖 Entity 的原有值。
     *
     * 举例说明：
     *   数据库里有一条记录：{id:1, originalFileName:"典则.pdf", remark:"重要文件"}
     *   前端只传：{remark:"已更新为2024版"}
     *   调用 updateEntity(dto, existingEntity) 后：
     *     - originalFileName 保持不变（因为 DTO 中该字段为 null，不覆盖）
     *     - remark 变为 "已更新为2024版"
     *
     * 这解决了“前端只传部分字段，其他字段不能丢失”的经典更新问题。
     *
     * @param dto   前端传入的更新数据（只包含需要修改的字段）
     * @param entity 数据库已有的实体（会被修改，直接作用于传入的对象）
     */
    void updateEntity(DocumentUploadRequest dto, @MappingTarget Document entity);

    // ================================================================
    // 场景4：分页列表（数据库 → 前端列表项）【可选，可按需启用】
    // ================================================================

    /**
     * 【列表转换】将 Document 实体转换为轻量级列表项 DTO。
     *
     * 使用时机：GET /api/v1/documents/list 接口，展示文档列表时。
     *
     * 为什么列表和详情要分开？
     *   列表页不需要 parseResult（大 JSON 字段），只展示文件名、状态、时间等元数据。
     *   如果复用 toResponse()，每次列表查询都会加载 parseResult 大字段，造成性能浪费。
     *
     * 当前实现：直接复用 toResponse()，因为 DocumentResponse 包含了列表所需的字段。
     * 企业级规范建议：当列表字段和详情字段差异较大时，建议拆分为独立的 DTO 类。
     *
     * 如果你后期需要独立的 DocumentListResponse 类，可以新增方法：
     *   DocumentListResponse toListResponse(Document entity);
     *
     * @param entity 数据库实体
     * @return DocumentResponse 列表项 DTO（轻量级，不含大文本字段）
     */
    default DocumentResponse toListResponse(Document entity) {
        // 直接复用 toResponse 方法，因为 DocumentResponse 包含了列表所需的基本字段。
        // 注：如果你想明确区分列表和详情，可以单独定义一个 DocumentListResponse 类。
        return toResponse(entity);
    }

    // ================================================================
    // 工具方法
    // ================================================================

    /**
     * 提取文件后缀名（从原始文件名中解析）。
     *
     * 示例：
     *   getSuffix("典则.pdf")     → "pdf"
     *   getSuffix("设计图.DOCX")   → "docx"
     *   getSuffix("无后缀文件")    → "unknown"
     *
     * 为什么用 default 方法？
     *   因为这是“纯工具函数”，不依赖任何外部资源，也不需要 MapStruct 生成代码。
     *   default 方法在 Java 8 接口中允许提供默认实现。
     *
     * @param fileName 原始文件名
     * @return 小写的文件后缀，如果无后缀则返回 "unknown"
     */
    default String getSuffix(String fileName) {
        if (fileName == null || !fileName.contains(".")) {
            return "unknown";
        }
        // 取最后一个点后面的部分，转为小写
        return fileName.substring(fileName.lastIndexOf(".") + 1).toLowerCase();
    }

    // ================================================================
    // 废弃方法（已移除，不推荐使用）
    // ================================================================

    /**
     * 【已移除】DocumentUploadRequest toDTO(Document document) 方法。
     *
     * 原因：用上传 DTO 作为响应 DTO，会导致 MultipartFile 字段为空，语义混乱。
     * 请使用 toResponse() 替代。
     */
    // DocumentUploadRequest toDTO(Document document); // ❌ 不推荐

}