import { chatApi } from '../api';
import { withAuthHeader } from '../../user/api';

export async function handleGetChannels() {
	const response = await chatApi.get('/channel', {
		headers: {
			...withAuthHeader()
		}
	});
	return response.data;
}

export async function handleGetMessages(channelId: string) {
	const response = await chatApi.get(`/channel/${channelId}/message`, {
		headers: {
			...withAuthHeader()
		}
	});
	return response.data;
}

export async function handleDeleteMessage(channelId: string, messageId: string) {
	const response = await chatApi.delete(`/channel/${channelId}/message/${messageId}`, {
		headers: {
			...withAuthHeader()
		}
	});
	return response.data;
}

export async function handleAddMessage(channelId: string, content: string) {
	await chatApi.post(
		`/channel/${channelId}/message`,
		{ content },
		{
			headers: {
				...withAuthHeader()
			}
		}
	);
}

export async function editMessage(channelId: string, messageId: string, new_content: string) {
	await chatApi.patch(
		`/channel/${channelId}/message/${messageId}`,
		{ new_content },
		{
			headers: {
				...withAuthHeader()
			}
		}
	);
}
