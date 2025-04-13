import type { ModeOptions } from './ModeOptions';
import type { TerradrawMode } from './TerradrawMode';
import { TerraDrawExtend } from 'terra-draw';
type BaseAdapterConfig = TerraDrawExtend.BaseAdapterConfig;
export interface TerradrawControlOptions {
    modes?: TerradrawMode[];
    open?: boolean;
    modeOptions?: ModeOptions;
    adapterOptions?: BaseAdapterConfig;
}
export {};
//# sourceMappingURL=TerradrawControlOptions.d.ts.map