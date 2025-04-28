import type { GeoJSONStoreFeatures, TerraDrawExtend } from 'terra-draw';
import type { TerradrawMode } from './TerradrawMode';
export interface EventArgs {
    feature?: GeoJSONStoreFeatures[];
    mode: TerradrawMode;
    deletedIds?: TerraDrawExtend.FeatureId[];
}
//# sourceMappingURL=EventArgs.d.ts.map