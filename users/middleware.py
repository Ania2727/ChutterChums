class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add theme to request context
        request.theme = request.COOKIES.get('theme', 'light')

        # Process the request and get the response
        response = self.get_response(request)

        return response