package com.nebulamind.kb.common.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableLogic;

import java.time.LocalDateTime;

/**
 * 基础实体类。
 * 所有数据库实体类的公共父类，封装了主键、租户ID、创建时间、更新时间、逻辑删除等通用字段。
 * 子类通过继承即可获得这些通用属性的能力。
 *
 * @author NebulaMind
 */
public abstract class BaseEntity {

    /**
     * 主键 ID，使用雪花算法自动生成。
     */
    @TableId(type = IdType.ASSIGN_ID)
    private Long id;

    /**
     * 租户 ID，用于多租户数据隔离。
     */
    private Long tenantId;

    /**
     * 创建时间，插入时自动填充。
     */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    /**
     * 更新时间，插入和更新时自动填充。
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;

    /**
     * 逻辑删除标识：0 = 未删除，1 = 已删除。
     */
    @TableLogic
    private Integer isDeleted;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getTenantId() {
        return tenantId;
    }

    public void setTenantId(Long tenantId) {
        this.tenantId = tenantId;
    }

    public LocalDateTime getCreateTime() {
        return createTime;
    }

    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }

    public LocalDateTime getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(LocalDateTime updateTime) {
        this.updateTime = updateTime;
    }

    public Integer getIsDeleted() {
        return isDeleted;
    }

    public void setIsDeleted(Integer isDeleted) {
        this.isDeleted = isDeleted;
    }
}