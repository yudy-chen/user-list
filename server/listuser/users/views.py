import csv
from django.http import HttpResponse
from .models import User

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")
    
def export(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    
    serverIP = request.get_host()    

    for user in User.objects.all():
        photoPath = ""
        if user.photo_path != None:
            photoPath = 'http://%s/public/userphoto/%s' % (serverIP, user.photo_path)
        row = [
            user.user_name,
            str(user.age),
            photoPath
        ]

        writer.writerow(row)

    return response
