export interface BlockPaletteEntry {
  name: string;
  color: string;
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
