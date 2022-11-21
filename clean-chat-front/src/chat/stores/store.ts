import { writable } from 'svelte/store';
import { globalStore } from '../../core/global-store';
import {
	handleAddMessage,
	handleDeleteMessage,
	handleGetChannels,
	handleGetMessages
} from '../services/chat';
import type { Message } from '../types';
import type { WebSocketStoreHandler } from '../../core/interfaces/WebSocketStoreHandler';
import { Set } from 'immutable';

export interface ChatState {
	messages: Message[];
	channels: any[]; // TODO add types
	currentChannel?: string;
	addedMessages: Set<string>;
}

const initialState = {
	messages: [],
	channels: [],
	currentChannel: null,
	addedMessages: Set<string>()
};

function createChatStore() {
	const store = writable<ChatState>(initialState);
	const { subscribe, set } = store;

	// Todo rewrite after adding multiple channels feature
	const initialize = async () => {
		try {
			globalStore.resetError();
			globalStore.setLoading(true);
			const channelsResponse = await handleGetChannels();
			const mainChannel = channelsResponse.payload[0];
			const messagesResponse = await handleGetMessages(mainChannel.id);
			const messageIds = messagesResponse.payload.map(({ id }) => id);
			set({
				messages: messagesResponse.payload,
				channels: channelsResponse.payload,
				currentChannel: mainChannel,
				addedMessages: Set(messageIds)
			});
		} catch (e) {
			globalStore.setError(e);
		} finally {
			globalStore.setLoading(false);
		}
	};

	const postMessage = async (channel: string, content: string) => {
		try {
			globalStore.resetError();
			globalStore.setLoading(true);
			await handleAddMessage(channel, content);
		} catch (e) {
			globalStore.setError(e);
		} finally {
			globalStore.setLoading(false);
		}
	};

	const editMessage = async (channel: string, content: string) => {
		try {
			globalStore.resetError();
			globalStore.setLoading(true);
			await handleAddMessage(channel, content);
		} catch (e) {
			globalStore.setError(e);
		} finally {
			globalStore.setLoading(false);
		}
	};

	const deleteMessage = async (channel: string, message_id: string) => {
		try {
			globalStore.resetError();
			globalStore.setLoading(true);
			await handleDeleteMessage(channel, message_id);
		} catch (e) {
			globalStore.setError(e);
		} finally {
			globalStore.setLoading(false);
		}
	};

	const connectToWs = (ws: WebSocketStoreHandler<ChatState>) => {
		ws.connectStore(store);
	};

	return {
		subscribe,
		initialize,
		connectToWs,
		postMessage,
		deleteMessage,
		editMessage
	};
}

export const chatStore = createChatStore();
