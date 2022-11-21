import type { Writable } from 'svelte/store';

export interface WebSocketStoreHandler<T> {
	connectStore(store: Writable<T>): void;
}
