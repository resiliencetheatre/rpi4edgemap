import type { ControlPosition, IControl, Map, StyleSpecification } from 'maplibre-gl';
import { type GeoJSONStoreFeatures, TerraDraw } from 'terra-draw';
import type { TerradrawControlOptions, EventType, TerradrawMode } from '../interfaces';
export declare class MaplibreTerradrawControl implements IControl {
    protected controlContainer?: HTMLElement;
    protected map?: Map;
    protected modeButtons: {
        [key: string]: HTMLButtonElement;
    };
    protected _isExpanded: boolean;
    get isExpanded(): boolean;
    set isExpanded(value: boolean);
    protected terradraw?: TerraDraw;
    protected options: TerradrawControlOptions;
    protected events: {
        [key: string]: [(event?: {
            feature?: GeoJSONStoreFeatures[];
            mode?: TerradrawMode;
        }) => void];
    };
    protected defaultMode: string;
    constructor(options?: TerradrawControlOptions);
    getDefaultPosition(): ControlPosition;
    onAdd(map: Map): HTMLElement;
    onRemove(): void;
    on(event: EventType, callback: (event?: {
        feature?: GeoJSONStoreFeatures[];
    }) => void): void;
    off(event: EventType, callback: (event?: {
        feature?: GeoJSONStoreFeatures[];
    }) => void): void;
    protected dispatchEvent(event: EventType, args?: {
        [key: string]: unknown;
    }): void;
    activate(): void;
    deactivate(): void;
    getTerraDrawInstance(): TerraDraw;
    protected toggleEditor(): void;
    protected resetActiveMode(): void;
    protected addTerradrawButton(mode: TerradrawMode): void;
    getFeatures(onlySelected?: boolean): {
        type: string;
        features: GeoJSONStoreFeatures[];
    };
    cleanStyle(style: StyleSpecification, options?: {
        excludeTerraDrawLayers?: boolean;
        onlyTerraDrawLayers?: boolean;
    }): StyleSpecification;
    protected handleDownload(): void;
    protected toggleButtonsWhenNoFeature(): void;
    protected toggleDeleteSelectionButton(): void;
}
//# sourceMappingURL=MaplibreTerradrawControl.d.ts.map