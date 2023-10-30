from django.shortcuts import render
from django.db.models import Sum
from .models import *
from urllib.parse import unquote
from django.http import Http404
import psycopg2
from Site.settings import CONFIG, MEDIA_ROOT, MONEY_SYMBOL


conn = psycopg2.connect(dbname=  CONFIG.get('Postgres DB', 'name'),
                        user=    CONFIG.get('Postgres DB', 'user'),
                        password=CONFIG.get('Postgres DB', 'password'),
                        host=    CONFIG.get('Postgres DB', 'host'),
                        port=    CONFIG.get('Postgres DB', 'port'))
conn.set_isolation_level(0)


def serialise_restore_works(objects_list, is_card_view=False):
    if not objects_list and is_card_view:
        raise Http404()
    restore_list = []
    for restore in objects_list:
        given_summ = Donation.objects.filter(restore_id=restore.restore_id) \
                 .aggregate(sum=Sum('sum'))['sum']
        restore_list.append(
            {'id': restore.restore_id,
             'name': restore.name,
             'image': restore.image.url if restore.image and restore.image.url else None,
             'total_sum': restore.total_sum,
             'given_sum': given_summ if given_summ else 0,
             'descr': restore.description[:50] + '...'
             })
        if is_card_view:
            restore_list[0].update({
                'descr': restore.description,
                'percent':
                    round(restore_list[0]['given_sum'] / restore_list[0]['total_sum'] * 100, 2)
            })
    return restore_list


def cards_view(request):
    # Deletion processing:
    restore_id = request.POST.get('delete')
    if restore_id:
        with conn.cursor() as curs:
            curs.execute(f'DELETE FROM "RestoreWorks" WHERE "restore_ID" = {restore_id}')

    # Search filter processing:
    restore_objects = RestoreWork.objects.all()
    # search = request.GET.get('search')
    search = request.POST.get('search')
    search =  unquote(search) if search else None
    if search:
        restore_objects = restore_objects.filter(name__iregex=search) | \
                          restore_objects.filter(description__iregex=search)

    restore_list = serialise_restore_works(restore_objects)
    # restore_list = [
    #     {'name': 'Name 1', 'id': 1,
    #     'image': 'https://avatars.mds.yandex.net/i?id=c767592f3a8b7f958a8b16b1ed7341f2969114e0-9830843-images-thumbs&n=13',
    #     'total_sum': 9_000_000 , 'given_sum': 1_000_000, 'descr': 'descr 1'},
    #     {'name': 'Name 2', 'id': 2,
    #      'image': 'https://yandex-images.clstorage.net/sw5O6Q131/97ec7dilroCN/wOYQ7JBwZ2q4pUeXNILuLuunjIXemfQGEFtleFsnsUxU0JAoCjp8CxOvg0ModnylqzOJMtWnPSu9LUjZxMvRqFHC1NihhbIu6XGzV0QSr9pacwyBr1zUt2Hu8OlLogGpZIbzun0t35nQ3XQB6res9V4zjTOxE0udWWlL7qBuAH6z5GGfdROnu-42Zoe38u07eQcsg_1s94UU_ZLpPXK0njAncApeHt3KoX_VYZhkHlWNApxEwUOaTj0KmfzS_5GP8pQhr8ehF3ueJpQWt5HdKnsE3TBMf6f3xbzRmV5gVewy13BYfj-MmZCtRJB65111fDDuRzMRWBwPeznP0t3DDrFEEm00IaXrDPV15zZSrLqq1u8QfJyExRVf4Ps_U7TOoaZAOA-tLJlwz5fS2MddtRwTfeRiAVivzYloXBB-QyyCNXNctjOkq6wGxwd3QS64OgV8YYydpeVXrAIZzCBHbiI3smntTPzKoq71IcknDPWvIN5HYlD5XH-o6h9Qf4DdwDUjvjUyZDnN1aUnZOAOuVmW3XO-7Wf29o1w6wzCdB4D1FJZDYzsOEGfFDAKd7xk3MBdlCFiOCwPCymeYv4ibSHmwp8Xw6S5_pX1RaawLSuqNL2hXrz2RiTMkwleUrSPM8dSCk5dPetAnUXgKSVuRK7B7HZjciguTzhorCBs4z6DNxPutwJXyK6EV7aUE-4KG-e-sqxtFsRFv2IZbGIF3hPFYni9H83KE3z00Ti3PBdfMZ-1gbNKXk95uV7zHNN_Q9aCXOcz1xquFcal5HANaNmlLXB_DTeklX1jWh8CdW9zBgE4Pj6-uiONhTEpNH5GjfBPleFiOT58OZp_MkzzL0AEwV_n0sa53uV0BoWRnKhaRsxBDly0hwaMkKvcYFYe4_dyOl3snxlhvkSTKpcsZI1DD9XzUSoO3Zm57sD_AI3hxSH8xREV-fz2ZBe0Mf_bS3VdAx9tNfd3DIKao',
    #      'total_sum': 1_000_000 , 'given_sum': 100_000, 'descr': 'descr 2'},
    #     {'name': 'Name 3', 'id': 3,
    #      'image': 'https://idei.club/uploads/posts/2022-02/1644602936_14-idei-club-p-dom-stena-v-odesse-interer-krasivo-foto-21.jpg',
    #      'total_sum': 110_000_000 , 'given_sum': 830_000, 'descr': 'descr 3'},
    #     {'name': 'Name 4', 'id': 4,
    #      'image': 'https://avatars.dzeninfra.ru/get-zen_doc/118604/pub_5c9dc73e93c31d00b21fd166_5c9dc760e5345700b36bc096/scale_1200',
    #      'total_sum': 1_100_000 , 'given_sum': 130_000, 'descr': 'descr 4'},
    #     {'name': 'Name 5', 'id': 5,
    #      'image': 'https://fsk-soyuz.ru/img/1-2.jpg',
    #      'total_sum': 11_000_000 , 'given_sum': 130_000, 'descr': 'descr 5'},
    # ]

    return render(request, 'Restorations/index.html',  {'restore_list': restore_list,
                                                        'money_symbhol': MONEY_SYMBOL})


def card_view(request, restore_id):
    restore = serialise_restore_works(RestoreWork.objects.filter(restore_id=restore_id),
                                      is_card_view=True)[0]  # Comment to use mock
    donaters_objects = Donater.objects.filter(donation__restore_id=restore_id)

    donaters_list = []
    for donater in donaters_objects:
        sum = Donation.objects.filter(donater_id=donater.donater_id) \
            .filter(restore_id=restore_id) \
            .aggregate(sum=Sum('sum'))['sum']
        donaters_list.append(
            {'name': donater.name,
             'type': donater.type if donater.type else '-',
             'given_sum': sum,
             'percent': sum/restore['total_sum']*100}) # Comment to use mock
    # given = 90_000
    # total = 100_000
    # restore = {'name': 'Name 1', 'id': restore_id,
    #     'image': 'https://avatars.mds.yandex.net/i?id=c767592f3a8b7f958a8b16b1ed7341f2969114e0-9830843-images-thumbs&n=13',
    #     'total_sum': total, 'given_sum': given, 'descr': 'Some descr', 'percent': given/total*100
    #            }

    # donaters_objects = []
    return render(request, 'Restorations/card.html', {'restore': restore,
                                                      'donaters_list': donaters_list,
                                                      'money_symbhol': MONEY_SYMBOL})


