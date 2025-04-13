import { Map, type StyleSpecification } from 'maplibre-gl';
import { MaplibreTerradrawControl } from './MaplibreTerradrawControl';
import type { AreaUnit, DistanceUnit, MeasureControlOptions } from '../interfaces';
import { type GeoJSONStoreFeatures } from 'terra-draw';
export declare class MaplibreMeasureControl extends MaplibreTerradrawControl {
    private measureOptions;
    get distanceUnit(): DistanceUnit;
    set distanceUnit(value: DistanceUnit);
    get distancePrecision(): number;
    set distancePrecision(value: number);
    get areaUnit(): AreaUnit;
    set areaUnit(value: AreaUnit);
    get areaPrecision(): number;
    set areaPrecision(value: number);
    get computeElevation(): boolean;
    set computeElevation(value: boolean);
    constructor(options?: MeasureControlOptions);
    onAdd(map: Map): HTMLElement;
    onRemove(): void;
    activate(): void;
    recalc(): void;
    cleanStyle(style: StyleSpecification, options?: {
        excludeTerraDrawLayers?: boolean;
        onlyTerraDrawLayers?: boolean;
    }): StyleSpecification;
    private registerMesureControl;
    private handleTerradrawDeselect;
    private handleTerradrawFeatureReady;
    private handleTerradrawFeatureChanged;
    private unregisterMesureControl;
    private clearMeasureFeatures;
    private replaceGeoJSONSource;
    private computeElevationByLineFeatureID;
    private computeElevationByPointFeatureID;
    private measurePolygon;
    private measureLine;
    private measurePoint;
    private onFeatureDeleted;
    getFeatures(onlySelected?: boolean): {
        type: string;
        features: GeoJSONStoreFeatures[];
    };
}
//# sourceMappingURL=MaplibreMeasureControl.d.ts.map