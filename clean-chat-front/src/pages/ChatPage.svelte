<script lang="ts">
	import { chatStore } from '../chat/stores/store';
	import { onDestroy, onMount } from 'svelte';
	import { userStore } from '../user/store';
	import Message from '../chat/components/Message.svelte';
	import { MessageCheckStatus } from '../chat/types';
	import { ChatWebsocketHandler } from '../chat/ws';
	import { ENV } from '../env';
	import { getToken } from '../core/services/token-service';
	import { Button, Textarea, Toolbar } from 'flowbite-svelte';
	import { globalStore } from '../core/global-store.js';

	let chatState;
	let userState;

	let isLoading;
	let ws;

	let newMessage = '';

	onDestroy(
		chatStore.subscribe((v) => {
			chatState = v;
		})
	);
	onDestroy(userStore.subscribe((v) => (userState = v)));

	// TODO, this code is temporary, before multiple channels feature will appear
	onMount(async () => {
		isLoading = true;
		await chatStore.initialize();
		ws = new ChatWebsocketHandler(
			`${ENV.WS_URL}/${chatState.currentChannel.id}?token=${getToken()}`
		);
		chatStore.connectToWs(ws);
		isLoading = false;
	});

	onDestroy(() => {
		if (ws) {
			ws.close();
		}
	});

	let messagesToShow = [];

	$: {
		messagesToShow = chatState.messages;
		if (userState?.userData?.hideToxic) {
			messagesToShow = messagesToShow.filter(
				(message) => message.type !== MessageCheckStatus.TOXIC
			);
		}
		if (userState?.userData?.hideUnchecked) {
			messagesToShow = messagesToShow.filter(
				(message) => message.type !== MessageCheckStatus.UNCHECKED
			);
		}
	}

	const submitNewMessage = async () => {
		if (newMessage) {
			await chatStore.postMessage(chatState.currentChannel.id, newMessage);
			newMessage = ''
		}
	};

	const onKeydownText = (e) => {
		if (e.key === 'Enter') {
			submitNewMessage();
		}
	};
</script>

<div class="max-h-[590px] w-full flex flex-col gap-8 p-10 overflow-y-auto">
	{#each messagesToShow as message (message.id)}
		<Message {message} />
	{/each}
</div>
<div class="mt-6 flex flex-row justify-center">
	<Textarea
		rows="3"
		disabled={$globalStore.isLoading}
		bind:value={newMessage}
		on:keydown={onKeydownText}
		class="mb-4 md:w-[480px]"
		placeholder="Write a message"
	>
		<div slot="footer" class="flex items-center justify-between">
			<Button disabled={$globalStore.isLoading || !newMessage} on:click={submitNewMessage}
				>Post message</Button
			>
		</div>
	</Textarea>
</div>
