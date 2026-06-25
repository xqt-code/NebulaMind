package com.nebulamind.kb.common.util;

import java.util.UUID;

public class FileUtil {

    /**
     * 获取文件后缀（带. 例：.pdf）
     * @param fileName 原始文件名
     * @return .pdf / .docx / 空字符串（无后缀）
     */
    public static String getFileExtension(String fileName) {
        if (fileName == null|| "".equals(fileName) || fileName.isBlank() || !fileName.contains(".")) {
            return "";
        }
        // 截取最后一个小数点到末尾
        return fileName.substring(fileName.lastIndexOf("."));
    }

    // 获取不带点文档后缀
    public static String getPureExtension(String fileName) {
        String ext = getFileExtension(fileName);
        return ext.startsWith(".") ? ext.substring(1) : ext;
    }

    /**
     * 生成MinIO全局唯一存储文件名
     * UUID + 时间戳 + 后缀
     */
    public static String generateStorageFileName(String fileName) {
        String ext = getFileExtension(fileName);
        if ("".equals(ext)) {
            return "";
        }
        return UUID.randomUUID().toString()+ "_" + System.currentTimeMillis() + ext;
    }

    /**
     * 校验文档白名单，只允许pdf/docx/txt/xlsx
     */
    public static Boolean checkDocAllow(String fileName) {
        String ext = getFileExtension(fileName);
        return "docx".equals(ext) || "pdf".equals(ext)|| "txt".equals(ext) || "xlsx".equals(ext);
    }

}
