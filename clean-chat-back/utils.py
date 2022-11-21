def create_subrouter(main_route: str):
    def create_route(sub_route: str):
        if not sub_route:
            return main_route
        if not sub_route.startswith('/'):
            sub_route = f'/{sub_route}'
        return f'{main_route}{sub_route}'

    return create_route
