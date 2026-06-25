package com.nebulamind.kb.service.convert;

import com.nebulamind.kb.dao.entity.Document;
import com.nebulamind.kb.service.dto.DocumentUploadRequest;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.NullValuePropertyMappingStrategy;

/**
 * 文档上传请求DTO 与 Document数据库实体 对象转换器
 * 基于MapStruct实现编译期自动生成转换代码，避免手动set/get冗余代码
 * 适用场景：文件上传接口接收前端参数后，快速转换为数据库保存实体
 * 转换规则说明：
 * 1. 同名同类型字段自动映射：fileName、fileSize、fileType 无需手动@Mapping
 * 2. 数据库实体独有业务字段（文件路径、任务ID、处理状态、切片数）前端DTO无入参，入库前由业务层手动赋值
 * 3. BaseEntity父类字段（id、租户ID、创建时间等）由MyBatis-Plus自动填充，转换时不处理
 * 4. 反向转换：实体转回DTO仅保留前端原始上传参数，丢弃数据库业务扩展字段
 *
 * 核心优势：
 * 1. 零反射，性能远高于BeanUtils、ModelMapper
 * 2. 编译期校验字段名、类型，写错直接编译报错，线上无转换异常
 * 3. 自动生成get/set赋值代码，无重复模板代码
 */

/**
 * DTO <-> Entity 转换器
 * componentModel = "spring" → 交给Spring管理，可@Autowired注入
 */
@Mapper(
        componentModel = "spring",
        // 更新时，DTO中null字段不覆盖Entity原有数据（重点！解决更新丢字段）
        nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE
)
public interface DocumentConvert {

    /**
     * 【正向转换：前端上传DTO → 数据库Document实体】
     * 使用时机：接口收到DocumentUploadRequest参数，准备插入数据库前调用
     * @param uploadRequest 前端上传文件基础信息DTO（文件名、大小、文件类型）
     * @return Document 待入库数据库实体
     * 映射逻辑：
     * 自动映射：fileName / fileSize / fileType 三者字段名、类型完全一致，MapStruct自动赋值
     * 不自动映射字段说明（需要业务代码手动填充）：
     * 1. filePath：文件上传至存储服务后的完整存储路径（OSS/本地磁盘路径，上传成功后赋值）
     * 2. status：文档处理状态，新建文档默认 0-待处理
     * 3. taskId：文档解析异步任务ID，发起解析任务后赋值
     * 4. chunkCount：文档切片分段数量，解析切片后赋值
     * 父类BaseEntity字段：id(雪花ID)、tenantId(多租户)、createTime、updateTime、isDeleted 由MyBatis-Plus自动填充，转换不处理
     */

    // DTO -> 实体
    Document toEntity(DocumentUploadRequest uploadRequest);

    /**
     * 【反向转换：数据库Document实体 → 前端上传原始DTO】
     * 使用时机：查询数据库文档记录，需要返回前端原始上传文件基础信息时调用
     * @param document 数据库文档实体
     * @return DocumentUploadRequest 仅包含前端上传时传入的三个基础字段
     * 映射逻辑：
     * 仅映射前端提交过的fileName、fileSize、fileType，实体中其他数据库专属字段全部丢弃
     * 适用场景：文档详情页展示文件基础信息、文件列表展示文件名大小类型
     */

    DocumentUploadRequest toDTO(Document document);

    default String getSuffix(String fileName) {
        if(fileName == null || !fileName.contains(".")) return "unknown";
        return fileName.substring(fileName.lastIndexOf(".") + 1);
    }
}