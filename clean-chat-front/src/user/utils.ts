export function transformResponseToUserConfig(response: any) {
	// todo add type for response
	const { hide_toxic, hide_unchecked, ...rest } = response;
	return {
		hideToxic: hide_toxic,
		hideUnchecked: hide_unchecked,
		...rest
	};
}
