export * from "./adapters";
/** @hidden */
export interface BufferPosition {
    buf: Uint8Array;
    pos: number;
}
/** @hidden */
export declare function readVarint(p: BufferPosition): number;
/**
 * Convert Z,X,Y to a Hilbert TileID.
 */
export declare function zxyToTileId(z: number, x: number, y: number): number;
/**
 * Convert a Hilbert TileID to Z,X,Y.
 */
export declare function tileIdToZxy(i: number): [number, number, number];
/**
 * PMTiles v3 directory entry.
 */
export interface Entry {
    tileId: number;
    offset: number;
    length: number;
    runLength: number;
}
/**
 * Enum representing a compression algorithm used.
 * 0 = unknown compression, for if you must use a different or unspecified algorithm.
 * 1 = no compression.
 */
export declare enum Compression {
    Unknown = 0,
    None = 1,
    Gzip = 2,
    Brotli = 3,
    Zstd = 4
}
/**
 * Provide a decompression implementation that acts on `buf` and returns decompressed data.
 *
 * Should use the native DecompressionStream on browsers, zlib on node.
 * Should throw if the compression algorithm is not supported.
 */
export type DecompressFunc = (buf: ArrayBuffer, compression: Compression) => Promise<ArrayBuffer>;
/**
 * Describe the type of tiles stored in the archive.
 * 0 is unknown/other, 1 is "MVT" vector tiles.
 */
export declare enum TileType {
    Unknown = 0,
    Mvt = 1,
    Png = 2,
    Jpeg = 3,
    Webp = 4,
    Avif = 5
}
export declare function tileTypeExt(t: TileType): string;
/**
 * PMTiles v3 header storing basic archive-level information.
 */
export interface Header {
    specVersion: number;
    rootDirectoryOffset: number;
    rootDirectoryLength: number;
    jsonMetadataOffset: number;
    jsonMetadataLength: number;
    leafDirectoryOffset: number;
    leafDirectoryLength?: number;
    tileDataOffset: number;
    tileDataLength?: number;
    numAddressedTiles: number;
    numTileEntries: number;
    numTileContents: number;
    clustered: boolean;
    internalCompression: Compression;
    tileCompression: Compression;
    tileType: TileType;
    minZoom: number;
    maxZoom: number;
    minLon: number;
    minLat: number;
    maxLon: number;
    maxLat: number;
    centerZoom: number;
    centerLon: number;
    centerLat: number;
    etag?: string;
}
/**
 * Low-level function for looking up a TileID or leaf directory inside a directory.
 */
export declare function findTile(entries: Entry[], tileId: number): Entry | null;
export interface RangeResponse {
    data: ArrayBuffer;
    etag?: string;
    expires?: string;
    cacheControl?: string;
}
/**
 * Interface for retrieving an archive from remote or local storage.
 */
export interface Source {
    getBytes: (offset: number, length: number, signal?: AbortSignal, etag?: string) => Promise<RangeResponse>;
    /**
     * Return a unique string key for the archive e.g. a URL.
     */
    getKey: () => string;
}
/**
 * Use the Browser's File API, which is different from the NodeJS file API.
 * see https://developer.mozilla.org/en-US/docs/Web/API/File_API
 */
export declare class FileSource implements Source {
    file: File;
    constructor(file: File);
    getKey(): string;
    getBytes(offset: number, length: number): Promise<RangeResponse>;
}
/**
 * Uses the browser Fetch API to make tile requests via HTTP.
 *
 * This method does not send conditional request headers If-Match because of CORS.
 * Instead, it detects ETag mismatches via the response ETag or the 416 response code.
 *
 * This also works around browser and storage-specific edge cases.
 */
export declare class FetchSource implements Source {
    url: string;
    /**
     * A [Headers](https://developer.mozilla.org/en-US/docs/Web/API/Headers) object, specfying custom [Headers](https://developer.mozilla.org/en-US/docs/Web/API/Headers) set for all requests to the remote archive.
     *
     * This should be used instead of maplibre's [transformRequest](https://maplibre.org/maplibre-gl-js/docs/API/classes/Map/#example) for PMTiles archives.
     */
    customHeaders: Headers;
    /** @hidden */
    mustReload: boolean;
    /** @hidden */
    chromeWindowsNoCache: boolean;
    constructor(url: string, customHeaders?: Headers);
    getKey(): string;
    /**
     * Mutate the custom [Headers](https://developer.mozilla.org/en-US/docs/Web/API/Headers) set for all requests to the remote archive.
     */
    setHeaders(customHeaders: Headers): void;
    getBytes(offset: number, length: number, passedSignal?: AbortSignal, etag?: string): Promise<RangeResponse>;
}
/** @hidden */
export declare function getUint64(v: DataView, offset: number): number;
/**
 * Parse raw header bytes into a Header object.
 */
export declare function bytesToHeader(bytes: ArrayBuffer, etag?: string): Header;
/**
 * Error thrown when a response for PMTiles over HTTP does not match previous, cached parts of the archive.
 * The default PMTiles implementation will catch this error once internally and retry a request.
 */
export declare class EtagMismatch extends Error {
}
/**
 * Interface for caches of parts (headers, directories) of a PMTiles archive.
 */
export interface Cache {
    getHeader: (source: Source) => Promise<Header>;
    getDirectory: (source: Source, offset: number, length: number, header: Header) => Promise<Entry[]>;
    getArrayBuffer: (source: Source, offset: number, length: number, header: Header) => Promise<ArrayBuffer>;
    invalidate: (source: Source) => Promise<void>;
}
interface ResolvedValue {
    lastUsed: number;
    data: Header | Entry[] | ArrayBuffer;
}
/**
 * A cache for parts of a PMTiles archive where promises are never shared between requests.
 *
 * Runtimes such as Cloudflare Workers cannot share promises between different requests.
 *
 * Only caches headers and directories, not individual tile contents.
 */
export declare class ResolvedValueCache {
    cache: Map<string, ResolvedValue>;
    maxCacheEntries: number;
    counter: number;
    decompress: DecompressFunc;
    constructor(maxCacheEntries?: number, prefetch?: boolean, // deprecated
    decompress?: DecompressFunc);
    getHeader(source: Source): Promise<Header>;
    getDirectory(source: Source, offset: number, length: number, header: Header): Promise<Entry[]>;
    getArrayBuffer(source: Source, offset: number, length: number, header: Header): Promise<ArrayBuffer>;
    prune(): void;
    invalidate(source: Source): Promise<void>;
}
interface SharedPromiseCacheValue {
    lastUsed: number;
    data: Promise<Header | Entry[] | ArrayBuffer>;
}
/**
 * A cache for parts of a PMTiles archive where promises can be shared between requests.
 *
 * Only caches headers and directories, not individual tile contents.
 */
export declare class SharedPromiseCache {
    cache: Map<string, SharedPromiseCacheValue>;
    invalidations: Map<string, Promise<void>>;
    maxCacheEntries: number;
    counter: number;
    decompress: DecompressFunc;
    constructor(maxCacheEntries?: number, prefetch?: boolean, // deprecated
    decompress?: DecompressFunc);
    getHeader(source: Source): Promise<Header>;
    getDirectory(source: Source, offset: number, length: number, header: Header): Promise<Entry[]>;
    getArrayBuffer(source: Source, offset: number, length: number, header: Header): Promise<ArrayBuffer>;
    prune(): void;
    invalidate(source: Source): Promise<void>;
}
/**
 * Main class encapsulating PMTiles decoding logic.
 *
 * if `source` is a string, creates a FetchSource using that string as the URL to a remote PMTiles.
 * if no `cache` is passed, use a SharedPromiseCache.
 * if no `decompress` is passed, default to the browser DecompressionStream API with a fallback to `fflate`.
 */
export declare class PMTiles {
    source: Source;
    cache: Cache;
    decompress: DecompressFunc;
    constructor(source: Source | string, cache?: Cache, decompress?: DecompressFunc);
    /**
     * Return the header of the archive,
     * including information such as tile type, min/max zoom, bounds, and summary statistics.
     */
    getHeader(): Promise<Header>;
    /** @hidden */
    getZxyAttempt(z: number, x: number, y: number, signal?: AbortSignal): Promise<RangeResponse | undefined>;
    /**
     * Primary method to get a single tile's bytes from an archive.
     *
     * Returns undefined if the tile does not exist in the archive.
     */
    getZxy(z: number, x: number, y: number, signal?: AbortSignal): Promise<RangeResponse | undefined>;
    /** @hidden */
    getMetadataAttempt(): Promise<unknown>;
    /**
     * Return the arbitrary JSON metadata of the archive.
     */
    getMetadata(): Promise<unknown>;
    /**
     * Construct a [TileJSON](https://github.com/mapbox/tilejson-spec) object.
     *
     * baseTilesUrl is the desired tiles URL, excluding the suffix `/{z}/{x}/{y}.{ext}`.
     * For example, if the desired URL is `http://example.com/tileset/{z}/{x}/{y}.mvt`,
     * the baseTilesUrl should be `https://example.com/tileset`.
     */
    getTileJson(baseTilesUrl: string): Promise<unknown>;
}
