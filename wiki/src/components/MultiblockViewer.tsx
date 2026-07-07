import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import * as THREE from 'three';
import type { MultiblockStructure } from '../lib/structures';
import { textureUrl } from '../lib/structures';

interface Props {
  structure: MultiblockStructure;
  placement?: string[];
  baseUrl?: string;
}

interface Voxel {
  x: number;
  y: number;
  z: number;
  key: string;
  entry: MultiblockStructure['palette'][string];
  note?: string;
}

const textureCache = new Map<string, THREE.Texture>();
const loader = new THREE.TextureLoader();

function getTexture(base: string, rel?: string): THREE.Texture | null {
  const url = textureUrl(base, rel);
  if (!url) return null;
  const cached = textureCache.get(url);
  if (cached) return cached;
  const tex = loader.load(url);
  tex.magFilter = THREE.NearestFilter;
  tex.minFilter = THREE.NearestFilter;
  tex.colorSpace = THREE.SRGBColorSpace;
  textureCache.set(url, tex);
  return tex;
}

function parseVoxels(structure: MultiblockStructure): Voxel[] {
  const voxels: Voxel[] = [];
  const noteMap = new Map(
    (structure.notes ?? []).map((n) => [`${n.pos[0]},${n.pos[1]},${n.pos[2]}`, n.text]),
  );

  structure.layers.forEach((layer, y) => {
    layer.forEach((row, z) => {
      [...row].forEach((ch, x) => {
        const entry = structure.palette[ch];
        if (!entry || entry.empty) return;
        const key = `${x},${y},${z}`;
        voxels.push({ x, y, z, key, entry, note: noteMap.get(key) });
      });
    });
  });

  return voxels;
}

export default function MultiblockViewer({ structure, placement = [], baseUrl }: Props) {
  const base = baseUrl ?? (typeof document !== 'undefined' ? document.querySelector('base')?.href ?? '/' : '/');
  const mountRef = useRef<HTMLDivElement>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const groupRef = useRef<THREE.Group | null>(null);
  const meshMapRef = useRef<Map<string, THREE.Mesh>>(new Map());
  const raycaster = useMemo(() => new THREE.Raycaster(), []);
  const pointer = useMemo(() => new THREE.Vector2(), []);

  const maxY = structure.layers.length - 1;
  const [layer, setLayer] = useState(maxY);
  const [selected, setSelected] = useState<Voxel | null>(null);
  const [hovered, setHovered] = useState<Voxel | null>(null);

  const voxels = useMemo(() => parseVoxels(structure), [structure]);
  const placementRules = placement.length > 0 ? placement : structure.placement ?? [];

  const rebuildMeshes = useCallback(
    (group: THREE.Group, map: Map<string, THREE.Mesh>, activeLayer: number) => {
      while (group.children.length) {
        const child = group.children[0];
        group.remove(child);
        if (child instanceof THREE.Mesh) {
          child.geometry.dispose();
          const mats = Array.isArray(child.material) ? child.material : [child.material];
          mats.forEach((m) => m.dispose());
        }
        if (child instanceof THREE.LineSegments) {
          child.geometry.dispose();
          (child.material as THREE.Material).dispose();
        }
      }
      map.clear();

      const geo = new THREE.BoxGeometry(0.92, 0.92, 0.92);
      const cx = structure.size[0] / 2 - 0.5;
      const cz = structure.size[2] / 2 - 0.5;

      voxels.forEach((v) => {
        if (v.y > activeLayer) return;
        const color = new THREE.Color(v.entry.color);
        const tex = getTexture(base, v.entry.texture);
        const mat = new THREE.MeshStandardMaterial({
          color: tex ? 0xffffff : color,
          map: tex ?? undefined,
          emissive: v.entry.controller ? new THREE.Color(0xfff176).multiplyScalar(0.15) : new THREE.Color(0x000000),
          metalness: tex ? 0.05 : 0.15,
          roughness: tex ? 0.9 : 0.65,
          transparent: v.y < activeLayer,
          opacity: v.y < activeLayer ? 0.35 : 1,
        });
        const mesh = new THREE.Mesh(geo.clone(), mat);
        mesh.position.set(v.x - cx, v.y, v.z - cz);
        mesh.userData = { voxel: v };
        if (v.entry.controller) {
          const edges = new THREE.EdgesGeometry(geo.clone());
          const line = new THREE.LineSegments(
            edges,
            new THREE.LineBasicMaterial({ color: 0xfff176 }),
          );
          line.position.copy(mesh.position);
          group.add(line);
        }
        group.add(mesh);
        map.set(v.key, mesh);
      });
    },
    [base, structure.size, voxels],
  );

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    const width = mount.clientWidth;
    const height = 360;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x121820);
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 200);
    camera.position.set(6, 5, 8);
    camera.lookAt(0, structure.size[1] / 2 - 0.5, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mount.appendChild(renderer.domElement);

    scene.add(new THREE.AmbientLight(0xffffff, 0.65));
    const dir = new THREE.DirectionalLight(0xffffff, 0.9);
    dir.position.set(5, 10, 7);
    scene.add(dir);

    const grid = new THREE.GridHelper(Math.max(structure.size[0], structure.size[2]) + 2, 12, 0x2d3a4f, 0x1a2332);
    scene.add(grid);

    const group = new THREE.Group();
    scene.add(group);

    sceneRef.current = scene;
    cameraRef.current = camera;
    rendererRef.current = renderer;
    groupRef.current = group;

    rebuildMeshes(group, meshMapRef.current, maxY);

    let frameId = 0;
    const animate = () => {
      frameId = requestAnimationFrame(animate);
      group.rotation.y += 0.003;
      renderer.render(scene, camera);
    };
    animate();

    const onResize = () => {
      const w = mount.clientWidth;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    };
    window.addEventListener('resize', onResize);

    return () => {
      cancelAnimationFrame(frameId);
      window.removeEventListener('resize', onResize);
      renderer.dispose();
      mount.removeChild(renderer.domElement);
    };
  }, [maxY, rebuildMeshes, structure.size]);

  useEffect(() => {
    const group = groupRef.current;
    if (!group) return;
    rebuildMeshes(group, meshMapRef.current, layer);
  }, [layer, rebuildMeshes]);

  const pickVoxel = (clientX: number, clientY: number) => {
    const mount = mountRef.current;
    const camera = cameraRef.current;
    const scene = sceneRef.current;
    if (!mount || !camera || !scene) return null;

    const rect = mount.getBoundingClientRect();
    pointer.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(scene.children, true);
    for (const hit of hits) {
      const v = hit.object.userData?.voxel as Voxel | undefined;
      if (v) return v;
    }
    return null;
  };

  const active = selected ?? hovered;

  return (
    <div className="rounded-xl border border-wiki-border bg-wiki-panel/60 overflow-hidden">
      <div
        ref={mountRef}
        className="w-full cursor-grab active:cursor-grabbing"
        style={{ height: 360 }}
        onPointerMove={(e) => setHovered(pickVoxel(e.clientX, e.clientY))}
        onClick={(e) => setSelected(pickVoxel(e.clientX, e.clientY))}
        role="presentation"
      />
      <div className="border-t border-wiki-border p-4 space-y-4">
        <div>
          <label className="mb-1 block text-sm text-slate-400" htmlFor="layer-slider">
            Слой Y: {layer} / {maxY}
          </label>
          <input
            id="layer-slider"
            type="range"
            min={0}
            max={maxY}
            value={layer}
            onChange={(e) => setLayer(Number(e.target.value))}
            className="w-full accent-wiki-accent"
          />
          <p className="mt-1 text-xs text-slate-500">
            Текстуры блоков из модов. Нижние слои полупрозрачны. Контроллер — жёлтый контур.
          </p>
        </div>

        {active && (
          <div className="rounded-lg border border-wiki-border bg-wiki-bg/50 p-3 text-sm">
            <p className="font-medium text-wiki-glow">{active.entry.name}</p>
            <p className="font-mono text-xs text-slate-500">
              позиция [{active.x}, {active.y}, {active.z}]
              {active.entry.controller ? ' · контроллер' : ''}
            </p>
            {active.note && <p className="mt-1 text-slate-300">{active.note}</p>}
          </div>
        )}

        {placementRules.length > 0 && (
          <div>
            <h4 className="mb-2 text-sm font-semibold text-wiki-warn">Размещение</h4>
            <ul className="list-inside list-disc space-y-1 text-sm text-slate-300">
              {placementRules.map((rule) => (
                <li key={rule}>{rule}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
