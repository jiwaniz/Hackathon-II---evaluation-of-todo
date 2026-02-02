"use client";

/**
 * API response caching hook.
 *
 * Provides simple caching for API responses with:
 * - Time-based cache invalidation
 * - Manual cache invalidation
 * - Stale-while-revalidate pattern
 * - Memory-efficient Map-based storage
 *
 * Reference: T149 - Add API response caching strategy in frontend
 */

import { useState, useCallback, useRef, useEffect } from "react";

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  isStale: boolean;
}

interface UseCacheOptions {
  /** Time in milliseconds before cache becomes stale (default: 30 seconds) */
  staleTime?: number;
  /** Time in milliseconds before cache entry is removed (default: 5 minutes) */
  cacheTime?: number;
}

interface UseCacheReturn<T> {
  /** Get cached data for a key */
  get: (key: string) => T | undefined;
  /** Set cached data for a key */
  set: (key: string, data: T) => void;
  /** Invalidate a specific cache key */
  invalidate: (key: string) => void;
  /** Invalidate all cache entries matching a prefix */
  invalidatePrefix: (prefix: string) => void;
  /** Clear all cached data */
  clear: () => void;
  /** Check if a key has stale data */
  isStale: (key: string) => boolean;
}

// Global cache store (persists across component re-renders)
const globalCache = new Map<string, CacheEntry<unknown>>();

/**
 * Hook for caching API responses.
 *
 * @param options - Cache configuration options
 * @returns Cache utilities
 *
 * @example
 * ```tsx
 * const cache = useApiCache<Task[]>({ staleTime: 30000 });
 *
 * // Check cache first
 * const cachedTasks = cache.get(`tasks-${userId}`);
 * if (cachedTasks && !cache.isStale(`tasks-${userId}`)) {
 *   return cachedTasks;
 * }
 *
 * // Fetch and cache
 * const tasks = await api.getTasks(userId);
 * cache.set(`tasks-${userId}`, tasks);
 * ```
 */
export function useApiCache<T>(options: UseCacheOptions = {}): UseCacheReturn<T> {
  const { staleTime = 30000, cacheTime = 300000 } = options;

  // Track mounted state for cleanup
  const isMounted = useRef(true);
  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
    };
  }, []);

  // Force re-render when cache changes
  const [, setUpdateTrigger] = useState(0);
  const triggerUpdate = useCallback(() => {
    if (isMounted.current) {
      setUpdateTrigger((prev) => prev + 1);
    }
  }, []);

  const get = useCallback(
    (key: string): T | undefined => {
      const entry = globalCache.get(key) as CacheEntry<T> | undefined;

      if (!entry) return undefined;

      // Check if entry has expired completely
      const age = Date.now() - entry.timestamp;
      if (age > cacheTime) {
        globalCache.delete(key);
        return undefined;
      }

      return entry.data;
    },
    [cacheTime]
  );

  const set = useCallback(
    (key: string, data: T): void => {
      const entry: CacheEntry<T> = {
        data,
        timestamp: Date.now(),
        isStale: false,
      };
      globalCache.set(key, entry as CacheEntry<unknown>);
      triggerUpdate();
    },
    [triggerUpdate]
  );

  const invalidate = useCallback(
    (key: string): void => {
      const entry = globalCache.get(key);
      if (entry) {
        entry.isStale = true;
        triggerUpdate();
      }
    },
    [triggerUpdate]
  );

  const invalidatePrefix = useCallback(
    (prefix: string): void => {
      for (const key of globalCache.keys()) {
        if (key.startsWith(prefix)) {
          const entry = globalCache.get(key);
          if (entry) {
            entry.isStale = true;
          }
        }
      }
      triggerUpdate();
    },
    [triggerUpdate]
  );

  const clear = useCallback((): void => {
    globalCache.clear();
    triggerUpdate();
  }, [triggerUpdate]);

  const isStale = useCallback(
    (key: string): boolean => {
      const entry = globalCache.get(key);
      if (!entry) return true;

      // Check if marked as stale
      if (entry.isStale) return true;

      // Check if past stale time
      const age = Date.now() - entry.timestamp;
      return age > staleTime;
    },
    [staleTime]
  );

  return {
    get,
    set,
    invalidate,
    invalidatePrefix,
    clear,
    isStale,
  };
}

/**
 * Generate a cache key for tasks.
 */
export function getTasksCacheKey(userId: string, filters?: Record<string, unknown>): string {
  const baseKey = `tasks-${userId}`;
  if (!filters || Object.keys(filters).length === 0) {
    return baseKey;
  }
  // Sort filters for consistent key
  const sortedFilters = Object.entries(filters)
    .filter(([, value]) => value !== undefined && value !== "")
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => `${key}=${value}`)
    .join("&");
  return sortedFilters ? `${baseKey}?${sortedFilters}` : baseKey;
}

/**
 * Generate a cache key for tags.
 */
export function getTagsCacheKey(userId: string): string {
  return `tags-${userId}`;
}

export default useApiCache;
