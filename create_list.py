if __name__ == '__main__':
	import twitter
	import csv
	from database import encontra_lista
	from database import nova_lista

	twitter_list = encontra_lista('politicos7c0')
	if (not twitter_list):
		twitter_list = twitter.create_list('politicos7c0')
		nova_lista(twitter_list)
	

	with open('7c0.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

		for handle in data:
			twitter.add_to_list(twitter_list, handle)