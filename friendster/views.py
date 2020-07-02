from django.shortcuts import render
import requests
from social_django.models import UserSocialAuth
# Create your views here.
def index(request):
	context = {}
	return render(request, 'friendster/index.html', context)

def friends(request):
	user = request.user
	print(user.id)
	authuser = UserSocialAuth.objects.get(user_id=user.id)
	getRecent = 'https://api.vk.com/method/friends.getRecent?'
	payload = {'uid': str(authuser.extra_data['id']),
			   'access_token': authuser.extra_data['access_token'],
			   'v': '5.120'}

	r = requests.get(getRecent, params=payload)
	listOfFriendsIds = r.json()['response']
	listOfFriendsNames = get_list_of_friends(request, listOfFriendsIds, authuser.extra_data['access_token'])
	context = {'friends': listOfFriendsNames}
	return render(request, 'friendster/friends.html', context)

def get_list_of_friends(request, listOfFriendsIds, access_token):
	getProfile = 'https://api.vk.com/method/users.get'
	listOfFriendsNames = []
	for friendId in listOfFriendsIds:
		try:
			payload = {'user_id': friendId, 'access_token': access_token, 'v': '5.120'}
			r = requests.get(getProfile, params=payload)
			first_name = r.json()['response'][0]['first_name']
			last_name = r.json()['response'][0]['last_name']
			listOfFriendsNames.append([str(friendId), first_name, last_name])
			print(first_name + last_name)
		except:
			print('Error')

	return listOfFriendsNames[:5]
