import { PMTiles } from "./index";
/**
 * Add a raster PMTiles as a layer to a Leaflet map.
 *
 * For vector tiles see https://github.com/protomaps/protomaps-leaflet
 */
export declare const leafletRasterLayer: (source: PMTiles, options: unknown) => any;
type GetResourceResponse<T> = ExpiryData & {
    data: T;
};
type ExpiryData = {
    cacheControl?: string | null;
    expires?: string | null;
};
type RequestParameters = {
    url: string;
    headers?: unknown;
    method?: "GET" | "POST" | "PUT";
    body?: string;
    type?: "string" | "json" | "arrayBuffer" | "image";
    credentials?: "same-origin" | "include";
    collectResourceTiming?: boolean;
};
type ResponseCallbackV3 = (error?: Error | undefined, data?: unknown | undefined, cacheControl?: string | undefined, expires?: string | undefined) => void;
type V3OrV4Protocol = <T extends AbortController | ResponseCallbackV3, R = T extends AbortController ? Promise<GetResourceResponse<unknown>> : {
    cancel: () => void;
}>(requestParameters: RequestParameters, arg2: T) => R;
/**
 * MapLibre GL JS protocol. Must be added once globally.
 */
export declare class Protocol {
    /** @hidden */
    tiles: Map<string, PMTiles>;
    metadata: boolean;
    /**
     * Initialize the MapLibre PMTiles protocol.
     *
     * * metadata: also load the metadata section of the PMTiles. required for some "inspect" functionality
     * and to automatically populate the map attribution. Requires an extra HTTP request.
     */
    constructor(options?: {
        metadata: boolean;
    });
    /**
     * Add a {@link PMTiles} instance to the global protocol instance.
     *
     * For remote fetch sources, references in MapLibre styles like pmtiles://http://...
     * will resolve to the same instance if the URLs match.
     */
    add(p: PMTiles): void;
    /**
     * Fetch a {@link PMTiles} instance by URL, for remote PMTiles instances.
     */
    get(url: string): PMTiles | undefined;
    /** @hidden */
    tilev4: (params: RequestParameters, abortController: AbortController) => Promise<{
        data: unknown;
        cacheControl?: undefined;
        expires?: undefined;
    } | {
        data: Uint8Array;
        cacheControl: string | undefined;
        expires: string | undefined;
    }>;
    tile: V3OrV4Protocol;
}
export {};
