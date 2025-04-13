import type { CircleLayerSpecification, SymbolLayerSpecification } from 'maplibre-gl';
import type { ModeOptions } from './ModeOptions';
import type { TerraDrawExtend } from 'terra-draw';
import type { DistanceUnit } from './DistanceUnit';
import type { AreaUnit } from './AreaUnit';
import type { TerradrawMode } from './TerradrawMode';
import type { TerrainSource } from './TerrainSource';
export interface MeasureControlOptions {
    modes?: TerradrawMode[];
    open?: boolean;
    modeOptions?: ModeOptions;
    adapterOptions?: TerraDrawExtend.BaseAdapterConfig;
    pointLayerLabelSpec?: SymbolLayerSpecification;
    lineLayerLabelSpec?: SymbolLayerSpecification;
    lineLayerNodeSpec?: CircleLayerSpecification;
    polygonLayerSpec?: SymbolLayerSpecification;
    distanceUnit?: DistanceUnit;
    distancePrecision?: number;
    areaUnit?: AreaUnit;
    areaPrecision?: number;
    computeElevation?: boolean;
    terrainSource?: TerrainSource;
}
//# sourceMappingURL=MeasureControlOptions.d.ts.map