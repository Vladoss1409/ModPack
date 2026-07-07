export interface BlockPaletteEntry {
  name: string;
  color: string;
  /** Relative path under public/textures/blocks/, e.g. powah/uraninite_block */
  texture?: string;
  controller?: boolean;
  empty?: boolean;
}

export interface StructureNote {
  pos: [number, number, number];
  text: string;
}

export interface MultiblockStructure {
  id: string;
  size: [number, number, number];
  palette: Record<string, BlockPaletteEntry>;
  layers: string[][];
  placement?: string[];
  notes?: StructureNote[];
}

export function loadStructure(data: MultiblockStructure): MultiblockStructure {
  return data;
}

export function textureUrl(base: string, texture?: string): string | null {
  if (!texture) return null;
  return `${base}textures/blocks/${texture}.png`;
}
