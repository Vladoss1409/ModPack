import type { Root, Text, Parent, PhrasingContent } from 'mdast';
import { visit } from 'unist-util-visit';

const ICON_RE = /\{\{icon\s+([a-z0-9_./-]+)\}\}/gi;

export interface RemarkWikiIconsOptions {
  base?: string;
}

function splitIconText(value: string, base: string): PhrasingContent[] {
  const nodes: PhrasingContent[] = [];
  let last = 0;
  ICON_RE.lastIndex = 0;
  let m: RegExpExecArray | null;
  while ((m = ICON_RE.exec(value)) !== null) {
    if (m.index > last) {
      nodes.push({ type: 'text', value: value.slice(last, m.index) });
    }
    const id = m[1];
    const [ns, ...rest] = id.split('/');
    const stem = rest.join('/').replace(/\//g, '_');
    const src = `${base}textures/icons/${ns}/${stem}.png`;
    nodes.push({
      type: 'html',
      value: `<img class="wiki-icon" src="${src}" alt="" loading="lazy" decoding="async" />`,
    });
    last = m.index + m[0].length;
  }
  if (last < value.length) {
    nodes.push({ type: 'text', value: value.slice(last) });
  }
  return nodes;
}

export function remarkWikiIcons(options: RemarkWikiIconsOptions = {}) {
  const base = options.base ?? '/';
  return (tree: Root) => {
    visit(tree, 'text', (node: Text, index, parent: Parent | undefined) => {
      if (index === undefined || !parent || !ICON_RE.test(node.value)) return;
      ICON_RE.lastIndex = 0;
      const replacement = splitIconText(node.value, base);
      if (replacement.length === 1 && replacement[0].type === 'text') return;
      parent.children.splice(index, 1, ...replacement);
    });
  };
}
