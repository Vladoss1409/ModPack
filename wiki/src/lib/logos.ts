import logosManifest from '../data/logos.json';

export type LogoMap = Record<string, string>;

export const logos = logosManifest as LogoMap;

export function logoUrl(base: string, slug: string): string | null {
  const rel = logos[slug];
  if (!rel) return null;
  return `${base}${rel}`;
}

export function hasLogo(slug: string): boolean {
  return slug in logos;
}
