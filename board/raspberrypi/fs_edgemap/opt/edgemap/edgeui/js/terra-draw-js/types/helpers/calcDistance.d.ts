import type { GeoJSONStoreFeatures } from 'terra-draw';
import type { Map } from 'maplibre-gl';
import type { DistanceUnit, TerrainSource } from '../interfaces';
export declare const calcDistance: (feature: GeoJSONStoreFeatures, distanceUnit: DistanceUnit, distancePrecision: number, map?: Map, computeElevation?: boolean, terrainSource?: TerrainSource) => GeoJSONStoreFeatures;
//# sourceMappingURL=calcDistance.d.ts.map