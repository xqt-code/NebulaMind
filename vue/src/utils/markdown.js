/**
 * Markdown 渲染工具
 * 基于 markdown-it + highlight.js + katex
 */

import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const md = new MarkdownIt({
  html: false,
  breaks: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return (
          '<pre class="hljs"><code>' +
          hljs.highlight(str, { language: lang, ignoreIllegals: true }).value +
          '</code></pre>'
        )
      } catch {
        // fallthrough
      }
    }
    return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>'
  },
})

// 自定义行内 LaTeX 规则：$...$
md.use((mdInstance) => {
  const defaultRender =
    mdInstance.renderer.rules.text ||
    function (tokens, idx) {
      return mdInstance.utils.escapeHtml(tokens[idx].content)
    }

  mdInstance.renderer.rules.text = function (tokens, idx) {
    const content = tokens[idx].content
    // 匹配 $...$ 行内公式
    const inlineMathRegex = /\$([^$]+)\$/g

    if (!inlineMathRegex.test(content)) {
      return defaultRender(tokens, idx)
    }

    inlineMathRegex.lastIndex = 0

    let result = ''
    let lastIndex = 0
    let match

    while ((match = inlineMathRegex.exec(content)) !== null) {
      result += mdInstance.utils.escapeHtml(content.slice(lastIndex, match.index))
      try {
        result += katex.renderToString(match[1], {
          throwOnError: false,
          displayMode: false,
        })
      } catch {
        result += match[0]
      }
      lastIndex = match.index + match[0].length
    }
    result += mdInstance.utils.escapeHtml(content.slice(lastIndex))

    return result
  }
})

// 自定义块级 LaTeX：$$...$$
md.use((mdInstance) => {
  mdInstance.block.ruler.before('fence', 'math_block', (state, startLine, endLine, silent) => {
    const pos = state.bMarks[startLine] + state.tShift[startLine]
    const max = state.eMarks[startLine]
    const lineText = state.src.slice(pos, max)

    if (!lineText.startsWith('$$')) return false

    if (silent) return true

    let nextLine = startLine
    let mathContent = ''

    // 单行 $$...$$
    if (lineText.length > 2 && lineText.endsWith('$$')) {
      mathContent = lineText.slice(2, -2).trim()
    } else {
      // 多行
      mathContent = lineText.slice(2).trim()
      nextLine++
      while (nextLine < endLine) {
        const nextPos = state.bMarks[nextLine] + state.tShift[nextLine]
        const nextMax = state.eMarks[nextLine]
        const nextText = state.src.slice(nextPos, nextMax)
        if (nextText.endsWith('$$')) {
          mathContent += '\n' + nextText.slice(0, -2).trim()
          nextLine++
          break
        }
        mathContent += '\n' + nextText
        nextLine++
      }
    }

    try {
      const html = katex.renderToString(mathContent, {
        throwOnError: false,
        displayMode: true,
      })

      const token = state.push('math_block', '', 0)
      token.content = html
      token.block = true
      token.map = [startLine, nextLine]
      state.line = nextLine - 1
    } catch {
      return false
    }

    return true
  })

  mdInstance.renderer.rules.math_block = function (tokens, idx) {
    return `<div class="math-block">${tokens[idx].content}</div>`
  }
})

/**
 * 渲染 Markdown 为 HTML
 * @param {string} content - Markdown 文本
 * @returns {string} HTML 字符串
 */
export function renderMarkdown(content) {
  if (!content) return ''
  return md.render(content)
}

/**
 * 渲染流式 Markdown 片段（可能不完整）
 * 对不完整的代码块做容错处理
 */
export function renderStreamingMarkdown(content) {
  if (!content) return ''
  // 补全未闭合的代码块，避免渲染异常
  const backtickCount = (content.match(/```/g) || []).length
  if (backtickCount % 2 !== 0) {
    return md.render(content + '\n```')
  }
  return md.render(content)
}

export default md