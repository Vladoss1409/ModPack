import { defineCollection, z } from 'astro:content';

const linksSchema = z
  .object({
    curseforge: z.string().url().optional(),
    modrinth: z.string().url().optional(),
    wiki: z.string().url().optional(),
  })
  .optional();

const mods = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    modId: z.string(),
    version: z.string(),
    category: z.enum([
      'tech',
      'magic',
      'exploration',
      'combat',
      'utility',
      'worldgen',
      'library',
      'client',
      'other',
    ]),
    tags: z.array(z.string()).default([]),
    links: linksSchema,
    draft: z.boolean().default(false),
  }),
});

const machines = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    modId: z.string(),
    modSlug: z.string().optional(),
    structure: z.string(),
    category: z.enum(['multiblock', 'machine', 'generator', 'network', 'structure']).default('multiblock'),
    tags: z.array(z.string()).default([]),
    placement: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { mods, machines };
