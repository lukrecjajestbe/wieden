function renderInline(text, keyPrefix) {
  const tokenRe = /\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)/g
  const parts = []
  let lastIndex = 0
  let match

  while ((match = tokenRe.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }
    if (match[1] !== undefined) {
      parts.push(
        <strong key={`${keyPrefix}-${match.index}`}>
          {renderInline(match[1], `${keyPrefix}-${match.index}`)}
        </strong>,
      )
    } else {
      parts.push(<span key={`${keyPrefix}-${match.index}`}>{match[2]}</span>)
    }
    lastIndex = tokenRe.lastIndex
  }
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }
  return parts
}

export default function MarkdownText({ text, as: Tag = 'p', className }) {
  if (!text) return null

  const lines = text.split('\n')

  return (
    <Tag className={className}>
      {lines.map((line, i) => {
        const content = line.startsWith('- ') ? line.slice(2) : line
        return (
          <span key={i} style={{ display: 'block' }}>
            {line.startsWith('- ') ? '• ' : ''}
            {renderInline(content, `line-${i}`)}
          </span>
        )
      })}
    </Tag>
  )
}
