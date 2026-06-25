package com.nebulamind.kb.common.result;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 通用分页结果封装
 * @param <T> 数据泛型
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageResult<T> {

    /**
     * 总记录数
     */
    private Long total;

    /**
     * 当前页数据
     */
    private List<T> records;

    /**
     * 当前页码
     */
    private Integer pageNum;

    /**
     * 每页大小
     */
    private Integer pageSize;

    public static <T> PageResult<T> of(Long total, List<T> records, Integer pageNum, Integer pageSize) {
        return new PageResult<>(total, records, pageNum, pageSize);
    }
}