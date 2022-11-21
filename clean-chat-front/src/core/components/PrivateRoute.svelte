<script lang="ts">
	export let shouldRedirect;
	export let path;
	export let redirectPath = '/';

	import { navigate, Route } from "svelte-navigator";

	$: if (shouldRedirect) {
		navigate(redirectPath)
	}



</script>

<Route path={path} >
	<slot></slot>
</Route>