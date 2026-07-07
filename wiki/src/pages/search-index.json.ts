import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

const clean = (s: string): string =>
  s
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/[#>*`_|]/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();

export const GET: APIRoute = async () => {
  const base = import.meta.env.BASE_URL;
  const mods = (await getCollection('mods')).filter((m) => !m.data.draft);
  const machines = (await getCollection('machines')).filter((m) => !m.data.draft);

  const items = [
    ...mods.map((m) => ({
      type: 'mod',
      title: m.data.name,
      url: `${base}mods/${m.slug}/`,
      category: m.data.category,
      tags: m.data.tags,
      modId: m.data.modId,
      excerpt: clean(m.body ?? '').slice(0, 180),
    })),
    ...machines.map((m) => ({
      type: 'machine',
      title: m.data.name,
      url: `${base}machines/${m.slug}/`,
      category: m.data.category,
      tags: m.data.tags,
      modId: m.data.modId,
      excerpt: (m.data.placement[0] ?? clean(m.body ?? '')).slice(0, 180),
    })),
  ];

  return new Response(JSON.stringify(items), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
