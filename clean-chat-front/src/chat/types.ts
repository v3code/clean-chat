export interface Message {
	id: string;
	content: string;
	created: string;
	edited?: number;
	type: MessageCheckStatus;
	author: MessageAuthor;
}

export interface MessageAuthor {
	id: string;
	username: string;
}

export enum MessageCheckStatus {
	UNCHECKED = 'UNCHECKED',
	TOXIC = 'TOXIC',
	SAFE = 'SAFE'
}

export enum WSMessageTypes {
	NEW_TYPE = 'new_type',
	NEW_MESSAGE = 'new_message',
	UPDATE_MESSAGE = 'update_message',
	DELETE_MESSAGE = 'delete_message',
	ADD_TO_CHANNEL = 'add_to_channel',
	REMOVE_FROM_CHANNEL = 'remove_from_channel'
}
