from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def post_list(request):
    return Response({"name":"Mobin"})