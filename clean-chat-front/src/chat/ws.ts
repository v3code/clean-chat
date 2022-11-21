import type { WebSocketStoreHandler } from '../core/interfaces/WebSocketStoreHandler';
import type { ChatState } from './stores/store';
import { WSMessageTypes } from './types';
import type { Writable } from 'svelte/store';

export class ChatWebsocketHandler implements WebSocketStoreHandler<ChatState> {
	private ws: WebSocket;
	private readonly url: string;
	private store: Writable<ChatState>;

	constructor(url: string) {
		this.url = url;
		this.connect();
	}

	connectStore(store: Writable<ChatState>): void {
		this.store = store;
	}

	connect() {
		const handleMessage = this.handleMessage.bind(this);
		this.ws = new WebSocket(this.url);
		this.ws.addEventListener('message', handleMessage);
		this.ws.addEventListener('close', () => {
			this.ws.removeEventListener('message', handleMessage);
			this.connect();
		});
	}

	private handleMessage(message: any) {
		const parsedMessage = JSON.parse(message.data);
		switch (parsedMessage.type) {
			case WSMessageTypes.NEW_TYPE:
				return this.handleNewType(parsedMessage.payload);
			case WSMessageTypes.DELETE_MESSAGE:
				return this.handleDeleteMessage(parsedMessage.payload);
			case WSMessageTypes.UPDATE_MESSAGE:
				return this.handleUpdateMessage(parsedMessage.payload);
			case WSMessageTypes.NEW_MESSAGE:
				return this.handleAddMessage(parsedMessage.payload);
			default:
				return;
		}
	}

	private handleAddMessage(message) {
		this.store.update((state) => {
			const { messages, addedMessages, ...rest } = state;
			if (addedMessages.has(message.id)) {
				return state;
			}
			return {
				messages: [...messages, message],
				addedMessages: addedMessages.add(message.id),
				...rest
			};
		});
	}

	private handleUpdateMessage(new_message) {
		this.store.update(({ messages, ...rest }) => {
			return {
				messages: messages.map((message) => {
					if (message.id === new_message.id) {
						return new_message;
					}
					return message;
				}),
				...rest
			};
		});
	}

	private handleDeleteMessage(message_id) {
		return this.store.update(({ messages, ...rest }) => ({
			messages: messages.filter(({ id }) => id !== message_id),
			...rest
		}));
	}

	private handleNewType(message) {
		const { id, type } = message;
		console.log({ type });
		this.store.update(({ messages, ...rest }) => ({
			messages: messages.map((message) => {
				if (message.id === id) {
					return {
						...message,
						type
					};
				}
				return message;
			}),
			...rest
		}));
	}
}
