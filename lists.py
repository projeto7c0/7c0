import twitter
from database import insere_lista
from database import get_all_lists
from database import recupera_ids_total
from database import insere_membros
from database import atualiza_membros
from database import prepara_atualizacao
from database import deleta_membros


def get_new_tweets(twitter_list):
    topo = recupera_ids_total(twitter_list)
    tweets = twitter.list_tweets(topo, twitter_list)
    insere_lista(tweets, twitter_list)


def get_all():
    return get_all_lists()


def get_members(twitter_list):
    members = twitter.list_members(twitter_list)
    prepara_atualizacao()
    insere_membros(members, twitter_list)
    atualiza_membros(members)
    deleta_membros()
    
