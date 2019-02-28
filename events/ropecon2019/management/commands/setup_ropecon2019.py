import os
from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from dateutil.tz import tzlocal

from core.utils import slugify, full_hours_between


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', *parts))


class Setup(object):
    def __init__(self):
        self._ordering = 0

    def get_ordering_number(self):
        self._ordering += 10
        return self._ordering

    def setup(self, test=False):
        self.test = test
        self.tz = tzlocal()
        self.setup_core()
        self.setup_labour()
        self.setup_intra()
        self.setup_tickets()
        self.setup_programme()
        self.setup_payments()
        self.setup_badges()

    def setup_core(self):
        from core.models import Venue, Event, Organization

        self.venue, unused = Venue.objects.get_or_create(
            name='Messukeskus',
            defaults=dict(
                name_inessive='Messukeskuksessa',
            ),
        )
        self.organization, unused = Organization.objects.get_or_create(
            slug='ropecon-ry',
            defaults=dict(
                name='Ropecon ry',
                homepage_url='http://www.ropecon.fi/hallitus',
            )
        )
        self.event, unused = Event.objects.get_or_create(slug='ropecon2019', defaults=dict(
            name='Ropecon 2019',
            name_genitive='Ropecon 2019 -tapahtuman',
            name_illative='Ropecon 2019 -tapahtumaan',
            name_inessive='Ropecon 2019 -tapahtumassa',
            homepage_url='http://2019.ropecon.fi',
            organization=self.organization,
            start_time=datetime(2019, 7, 26, 15, 0, tzinfo=self.tz),
            end_time=datetime(2019, 7, 28, 18, 0, tzinfo=self.tz),
            venue=self.venue,
        ))

    def setup_labour(self):
        from core.models import Person
        from labour.models import (
            AlternativeSignupForm,
            InfoLink,
            Job,
            JobCategory,
            LabourEventMeta,
            Perk,
            PersonnelClass,
            Qualification,
            WorkPeriod,
        )
        from ...models import SignupExtra, SpecialDiet
        from django.contrib.contenttypes.models import ContentType

        labour_admin_group, = LabourEventMeta.get_or_create_groups(self.event, ['admins'])

        if self.test:
            person, unused = Person.get_or_create_dummy()
            labour_admin_group.user_set.add(person.user)

        content_type = ContentType.objects.get_for_model(SignupExtra)

        labour_event_meta_defaults = dict(
            signup_extra_content_type=content_type,
            work_begins=datetime(2019, 7, 26, 8, 0, tzinfo=self.tz),
            work_ends=datetime(2019, 7, 28, 23, 0, tzinfo=self.tz),
            admin_group=labour_admin_group,
            contact_email='Ropecon 2019 -työvoimatiimi <tyovoima@ropecon.fi>',
        )

        if self.test:
            t = now()
            labour_event_meta_defaults.update(
                registration_opens=t - timedelta(days=60),
                registration_closes=t + timedelta(days=60),
            )

        labour_event_meta, unused = LabourEventMeta.objects.get_or_create(
            event=self.event,
            defaults=labour_event_meta_defaults,
        )

        for pc_name, pc_slug, pc_app_label in [
            ('Conitea', 'conitea', 'labour'),
            ('Vuorovastaava', 'ylivankari', 'labour'),
            ('Ylityöntekijä', 'ylityovoima', 'labour'),
            ('Työvoima', 'tyovoima', 'labour'),
            ('Ohjelmanjärjestäjä', 'ohjelma', 'programme'),
            ('Guest of Honour', 'goh', 'programme'),
            ('Media', 'media', 'badges'),
            ('Myyjä', 'myyja', 'badges'),
            ('Vieras', 'vieras', 'badges'),
            ('Vapaalippu', 'vapaalippu', 'badges'),
        ]:
            personnel_class, created = PersonnelClass.objects.get_or_create(
                event=self.event,
                slug=pc_slug,
                defaults=dict(
                    name=pc_name,
                    app_label=pc_app_label,
                    priority=self.get_ordering_number(),
                ),
            )

        tyovoima = PersonnelClass.objects.get(event=self.event, slug='tyovoima')
        ylityovoima = PersonnelClass.objects.get(event=self.event, slug='ylityovoima')
        conitea = PersonnelClass.objects.get(event=self.event, slug='conitea')
        ylivankari = PersonnelClass.objects.get(event=self.event, slug='ylivankari')
        ohjelma = PersonnelClass.objects.get(event=self.event, slug='ohjelma')

        if not JobCategory.objects.filter(event=self.event).exists():
            for jc_data in [
                ('Conitea', 'Tapahtuman järjestelytoimikunnan eli conitean jäsen', [conitea]),
                ('Erikoistehtävä', 'Mikäli olet sopinut erikseen työtehtävistä ja/tai sinut on ohjeistettu täyttämään lomake, valitse tämä ja kerro tarkemmin Vapaa alue -kentässä mihin tehtävään ja kenen toimesta sinut on valittu.', [tyovoima, ylityovoima, ylivankari]),
                ('jv', 'Järjestyksenvalvoja', 'Kävijöiden turvallisuuden valvominen conipaikalla ja yömajoituksessa. Edellyttää voimassa olevaa JV-korttia ja asiakaspalveluasennetta. HUOM! Et voi valita tätä tehtävää hakemukseesi, ellet ole täyttänyt tietoihisi JV-kortin numeroa (oikealta ylhäältä oma nimesi &gt; Pätevyydet).', [tyovoima, ylityovoima, ylivankari]),
                ('kasaus', 'Kasaus ja purku', 'Kalusteiden siirtelyä & opasteiden kiinnittämistä. Ei vaadi erikoisosaamista. Työvuoroja vain perjantaina 8-16 ja sunnuntaina 15-22.', [tyovoima, ylityovoima, ylivankari]),
                ('logistiikka', 'Logistiikka', 'Tavaroiden roudaamista ja pakettiauton ajamista. Pääosa työvuoroista ajoittuu pe 8-16 ja su 15-22 väliselle ajalle.', [tyovoima, ylityovoima, ylivankari]),
                ('majoitus', 'Majoitusvalvoja', 'Huolehtivat lattiamajoituspaikkojen pyörittämisestä.', [tyovoima, ylityovoima, ylivankari]),
                ('lastenhoito', 'Lastenhoitohuone', 'Valvovat lastenhoitohuoneen toimintaa.', [tyovoima, ylityovoima, ylivankari]),
                ('takahuone', 'Takahuone', 'Pyörittävät takahuonetta.', [tyovoima, ylityovoima, ylivankari]),
                ('kaato', 'Kaato', 'Hoitavat kaadon. Tämän työpisteen toiminta tapahtuu kokonaisuudessaan conin jälkeisenä maanantaina ja osin tiistaiaamuna.', [tyovoima, ylityovoima, ylivankari]),
                ('lipunmyynti', 'Lipunmyynti', 'Pääsylippujen myyntiä sekä lippujen tarkastamista. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä.', [tyovoima, ylityovoima, ylivankari]),
                ('myyntituote', 'Myyntitiski', 'Ropecon-oheistuotteiden myyntiä. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä.', [tyovoima, ylityovoima, ylivankari]),
                ('kirpputori', 'Kirpputori', 'Kävijöiden tuomien kirppistuotteiden myyntiä. Myyjiltä edellytetään täysi-ikäisyyttä, asiakaspalveluhenkeä ja huolellisuutta rahankäsittelyssä.', [tyovoima, ylityovoima, ylivankari]),
                ('narikka', 'Narikka', 'Narikka, duh.', [tyovoima, ylityovoima, ylivankari]),
                ('ohjelmajuoksija', 'Ohjelmajuoksija', 'Avustaa ohjelmanjärjestäjiä salitekniikan ja ohjelmanumeron käynnistämisessä.', [tyovoima, ylityovoima, ylivankari]),
                ('info', 'Info', 'Infopisteen henkilökunta vastaa kävijöiden kysymyksiin ja ratkaisee heidän ongelmiaan tapahtuman paikana. Tehtävä edellyttää asiakaspalveluasennetta, tervettä järkeä ja ongelmanratkaisukykyä.', [tyovoima, ylityovoima, ylivankari]),
                ('figutiski', 'Figutiski', 'Figupelien infotiski opastaa kävijöitä ja turnausjärjestäjiä erityisesti figuturnauksiin liittyvissä asioissa.', [tyovoima, ylityovoima, ylivankari]),
                ('korttitiski', 'Korttitiski', 'Korttipelien infotiski opastaa kävijöitä ja turnausjärjestäjiä erityisesti korttiturnauksiin liittyvissä asioissa.', [tyovoima, ylityovoima, ylivankari]),
                ('larptiski', 'Larppitiski', 'Larppien infotiski opastaa kävijöitä ja larppien järjestäjiä larppeihin liittyvissä asioissa.', [tyovoima, ylityovoima, ylivankari]),
                ('ropetiski', 'Ropetiski', 'Roolipelien infotiski opastaa kävijöitä ja GM:iä roolipeleihin liittyvissä asioissa.', [tyovoima, ylityovoima, ylivankari]),
                ('kp', 'Kokemuspiste', 'Kokemuspisteen infotiski opastaa kävijöitä kokemuspisteeseen liittyvissä asioissa.', [tyovoima, ylityovoima, ylivankari]),
                ('kpharraste', 'Kokemuspisteen harraste-esittelijä', 'Kokemuspisteen harraste-esittelijät esittelevät jotain tiettyä peliä ja auttavat sen pelaamisessa.', [tyovoima, ylityovoima, ylivankari]),
                ('imp', 'International Meeting Point', 'Ulkomaalaisten kävijöiden auttamista International Meeting Pointilla. Vähintään yhden vieraan kielen sujuva taito vaatimuksena.', [tyovoima, ylityovoima, ylivankari]),
                ('tekniikka', 'Tekniikka', 'Tieto- ja/tai AV-tekniikan rakentamista, ylläpitoa ja purkamista.', [tyovoima, ylityovoima, ylivankari]),
                ('taltiointi', 'Taltiointi', 'Ohjelmanumeroiden taltiointia.', [tyovoima, ylityovoima, ylivankari]),

                ('ohjelma', 'Ohjelmanjärjestäjä', 'Luennon tai muun vaativan ohjelmanumeron pitäjä', [ohjelma]),
                ('pj', 'Pelinjohtaja', 'Roolipelien tai larppien järjestäjä', [ohjelma]),
                ('peli', 'Pelinjärjestäjä', 'Muiden kuin roolipelien tai larppien järjestäjä', [ohjelma]),
            ]:
                if len(jc_data) == 3:
                    name, description, pcs = jc_data
                    slug = slugify(name)
                elif len(jc_data) == 4:
                    slug, name, description, pcs = jc_data

                job_category, created = JobCategory.objects.get_or_create(
                    event=self.event,
                    slug=slug,
                    defaults=dict(
                        name=name,
                        description=description,
                    )
                )

                if created:
                    job_category.personnel_classes.set(pcs)

        labour_event_meta.create_groups()

        for name in ['Conitea']:
            JobCategory.objects.filter(event=self.event, name=name).update(public=False)

        for jc_name, qualification_name in [
            ('Järjestyksenvalvoja', 'JV-kortti'),
        ]:
            jc = JobCategory.objects.get(event=self.event, name=jc_name)
            qual = Qualification.objects.get(name=qualification_name)

        for diet_name in [
            'Gluteeniton',
            'Laktoositon',
            'Maidoton',
            'Vegaaninen',
            'Lakto-ovo-vegetaristinen',
        ]:
            SpecialDiet.objects.get_or_create(name=diet_name)

        AlternativeSignupForm.objects.get_or_create(
            event=self.event,
            slug='conitea',
            defaults=dict(
                title='Conitean ilmoittautumislomake',
                signup_form_class_path='events.ropecon2019.forms:OrganizerSignupForm',
                signup_extra_form_class_path='events.ropecon2019.forms:OrganizerSignupExtraForm',
                active_from=datetime(2019, 2, 24, 12, 0, 0, tzinfo=self.tz),
                active_until=datetime(2019, 7, 19, 23, 59, 59, tzinfo=self.tz),
            ),
        )

    def setup_programme(self):
        from labour.models import PersonnelClass
        from programme.models import (
            AlternativeProgrammeForm,
            Category,
            ProgrammeEventMeta,
            Role,
            Room,
            SpecialStartTime,
            TimeBlock,
            View,
        )
        from ...models import TimeSlot

        programme_admin_group, hosts_group = ProgrammeEventMeta.get_or_create_groups(self.event, ['admins', 'hosts'])
        programme_event_meta, unused = ProgrammeEventMeta.objects.get_or_create(event=self.event, defaults=dict(
            public=False,
            admin_group=programme_admin_group,
            contact_email='Ropecon 2019 -ohjelmatiimi <ohjelma@ropecon.fi>',
            schedule_layout='reasonable',
        ))

        if settings.DEBUG:
            programme_event_meta.accepting_cold_offers_from = now() - timedelta(days=60)
            programme_event_meta.accepting_cold_offers_until = now() + timedelta(days=60)
            programme_event_meta.save()

        if not Room.objects.filter(event=self.event).exists():
            for room_name in [
                'Halli 3',
                'Halli 3 Bofferialue',
                'Halli 1 Myyntialue',
                'Halli 3 Näyttelyalue',
                'Halli 3 Korttipelialue',
                'Halli 3 Figupelialue',
                'Halli 3 Pukukilpailutiski',
                'Halli 3 Ohjelmalava',
                'Halli 3 Puhesali',
                'Halli 3 Ohjelmasali',
                'Ylä-Galleria',
                'Ala-Galleria',
                'Larp-tiski',
                'Messuaukio',
                'Klubiravintola',
                'Sali 103',
                'Sali 201',
                'Sali 202',
                'Sali 203a',
                'Sali 203b',
                'Sali 204',
                'Sali 205',
                'Sali 206',
                'Sali 207',
                'Sali 211',
                'Sali 212',
                'Sali 213',
                'Sali 214',
                'Sali 215',
                'Sali 216',
                'Sali 216a',
                'Sali 217',
                'Sali 218',
                'Sali 301',
                'Sali 302',
                'Sali 303',
                'Sali 304',
                'Sali 305',
                'Sali 306',
                'Sali 307',
                'Salin 203 aula',
            ]:
                room, created = Room.objects.get_or_create(
                    event=self.event,
                    name=room_name,
                )

        for pc_slug, role_title, role_is_default in [
            ('ohjelma', 'Ohjelmanjärjestäjä', True),
            ('ohjelma', 'Pelinjohtaja', False),
            ('ohjelma', 'Pelinjärjestäjä', False),
            ('ohjelma', 'Peliesittelijä', False),
        ]:
            personnel_class = PersonnelClass.objects.get(event=self.event, slug=pc_slug)
            role, unused = Role.objects.get_or_create(
                personnel_class=personnel_class,
                title=role_title,
                defaults=dict(
                    is_default=role_is_default,
                )
            )

        have_categories = Category.objects.filter(event=self.event).exists()
        if not have_categories:
            for title, slug, style in [
                ('Puheohjelma: esitelmä / Presentation', 'pres', 'color1'),
                ('Puheohjelma: paneeli / Panel discussion', 'panel', 'color1'),
                ('Puheohjelma: keskustelu / Discussion group', 'disc', 'color1'),
                ('Työpaja: käsityö / Crafts', 'craft', 'color2'),
                ('Työpaja: figut / Miniature figurines', 'mini', 'color2'),
                ('Työpaja: musiikki / Music', 'music', 'color2'),
                ('Työpaja: muu / Other workshop', 'workshop', 'color2'),
                ('Pelitiski: Figupeli / Miniature wargame', 'miniwar', 'color3'),
                ('Pelitiski: Korttipeli / Card game', 'card', 'color3'),
                ('Pelitiski: Lautapeli / Board game', 'board', 'color3'),
                ('Pelitiski: Kokemuspiste / Experience Point', 'exp', 'color3'),
                ('Roolipeli / Pen & Paper RPG', 'rpg', 'color4'),
                ('LARP', 'larp', 'color5'),
                ('Muu ohjelma / None of the above', 'other', 'color6'),
                ('Sisäinen ohjelma', 'internal', 'sisainen'),
            ]:
                Category.objects.get_or_create(
                    event=self.event,
                    slug=slug,
                    defaults=dict(
                        title=title,
                        style=style,
                        public=style != 'sisainen',
                    )
                )

        TimeBlock.objects.get_or_create(
            event=self.event,
            start_time=self.event.start_time,
            defaults=dict(
                end_time=self.event.end_time,
            ),
        )

        for time_block in TimeBlock.objects.filter(event=self.event):
            # Half hours
            # [:-1] – discard 18:30
            for hour_start_time in full_hours_between(time_block.start_time, time_block.end_time)[:-1]:
                SpecialStartTime.objects.get_or_create(
                    event=self.event,
                    start_time=hour_start_time.replace(minute=30)
                )

        have_views = View.objects.filter(event=self.event).exists()
        if not have_views:
            for view_name, room_names in [
                ('Pääohjelmatilat', [
                    'Halli 3 Ohjelmalava',
                    'Halli 3 Korttipelialue',
                    'Halli 3 Figupelialue',
                ]),
            ]:
                view, created = View.objects.get_or_create(event=self.event, name=view_name)

                if created:
                    rooms = [
                        Room.objects.get(name__iexact=room_name, event=self.event)
                        for room_name in room_names
                    ]

                    view.rooms = rooms
                    view.save()

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug='roolipeli',
            defaults=dict(
                title='Tarjoa pöytäroolipeliä',
                description='''
Tule pöytäpelinjohtajaksi Ropeconiin! Voit testata kehittämiäsi seikkailuja uusilla pelaajilla ja saada näkökulmia muilta harrastajilta. Pelauttamalla onnistuneita skenaariota pääset jakamaan tietotaitoa ja ideoita muille pelinjohtajille ja pelaajille. Voit myös esitellä uusia pelijärjestelmiä ja -maailmoja tai vain nauttia pelauttamisen riemusta.

Pelinjohtajat saavat Ropeconin viikonloppurannekkeen kahdeksan tunnin pelautuksella tai päivärannekkeen neljän tunnin pelautuksella. Lisäksi pelinjohtajat palkitaan sunnuntaina jaettavalla lootilla, eli ilmaisella roolipelitavaralla. Mitä useamman pelin pidät, sitä korkeammalle kohoat loottiasteikossa!
                '''.strip(),
                programme_form_code='events.ropecon2019.forms:RpgForm',
                num_extra_invites=0,
                order=20,
            )
        )

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug='larp',
            defaults=dict(
                title='Tarjoa larppia',
                short_description='Larpit eli liveroolipelit',
                description='''
Tervetuloa tarjoamaan Ropeconin kävijöille larp-elämyksiä!

Voit tarjota tällä lomakkeella sekä itse kirjoittamiasi pelejä että valmiita skenaarioita. Toivomme saavamme coniin hienon kattauksen sekä kotimaisia ensipelautuksia että kansainvälisiä klassikoita. Yhdellä oman pelisi pelautuksella (n. 3-4 tuntia) tai kahdella valmiin skenaarion pelautuksella (n. 6-8 tuntia) saat yhden viikonloppulipun Ropeconiin.

Suosittelemme keskittymään pelisuunnittelussa/valinnassa olennaiseen: conikävijöillä ei välttämättä ole mahdollisuuksia tuoda mukanaan tarkasti määriteltyjä proppeja tai opetella kymmenien sivujen taustamateriaaleja. Parhaiten toimivat lyhyehköt pelit, joihin pelaajat voivat saapua mukanaan vain oma mielikuvituksensa ja halu pelata toistensa kanssa. Toivomme myös, että mahdollisimman moni peli olisi mahdollisimman monen kävijän pelattavissa, eivätkä pelaajan tiedot, taidot tai ominaisuudet estä peliin osallistumista.

Kävijät toivoivat viime vuonna etenkin lyhyitä pelejä sekä lapsille sopivia larppeja, joten toivomme ehdotuksia lyhyistä, toistettavissa olevista pelautuksista sekä lapsille suunnitelluista larpeista.

Larpit järjestetään tänäkin vuonna Siiven huoneissa 215-217, joihin voit tutustua <a href="https://messukeskus.visualizer360.com/tilat#20250,20307,0,0" target="_blank">Messukeskuksen sivuilla</a>. Pyrimme rakentamaan yhteen huoneista black boxin (black box -larpeista voit lukea <a href="https://nordiclarp.org/wiki/Black_Box_Larp" target="_blank">Nordic Larp Wikissä</a>) ja varustamaan muut huoneista tunnelmaa luovilla valospoteilla. Kerrothan tilatoiveissa, mikäli suunnitelmissasi on black box -larppi! Valitettavasti emme voi tarjota suurempia lavasteita tai proppeja, joten otathan tämän peliäsi suunnitellessa huomioon.

Jos sinulla kuitenkin sattuu olemaan omasta takaa mahdollisuus esimerkiksi lavastaa jokin tila peliisi sopivaksi tai haluat tarjota koko Ropeconin ajan kestävän, Messukeskuksen alueelle levittyvän immersiivisen kokemuksen, emme missään tapauksessa kiellä tällaisten spektaakkelien suunnittelua. Kerro siinä tapauksessa meille lisää suunnitelmistasi, ja pohditaan yhdessä, kuinka sen voisi toteuttaa!

Kaikkien Ropeconissa pelautettavien larppien tulee soveltaa <a href="https://turvallisempaa.wordpress.com/" target="_blank">häirinnän vastaista materiaalipakettia</a>, eikä niissä hyväksytä ahdistelua ja häirintää (paitsi hahmojen toimintana pelissä, kaikkien osapuolten rajoja kunnioittaen). Tavoitteena on luoda yhdessä turvallinen peliympäristö jokaiselle peliin osallistujalle. Odotamme pelinjohtajien tuntevan materiaalin ja sitoutuvan omalla toiminnallaan edistämään turvallista peliympäristöä ja torjumaan häirintää.

Otathan huomioon myös inklusiivisuuskysymykset, eli pelisi esteettömyyden esimerkiksi liikuntarajoitteisille tai näkövammaisille pelaajille. Toivomme, että mahdollisimman moni kävijä voisi osallistua Ropeconin larppeihin. Ole meihin rohkeasti yhteydessä osoitteeseen <a href="mailto:larpit@ropecon.fi">larpit@ropecon.fi</a>, jos nämä kysymykset askarruttavat.
                '''.strip(),
                programme_form_code='events.ropecon2019.forms:LarpForm',
                num_extra_invites=0,
                order=30,
            )
        )

#         AlternativeProgrammeForm.objects.get_or_create(
#             event=self.event,
#             slug='lautapeli',
#             defaults=dict(
#                 title='Tarjoa lautapeliohjelmaa',
#                 short_description='Lautapelit',
#                 description='''
# Muhiiko mielessäsi hullu tai tuiki tavallinen lautapeleihin liittyvä idea? Kerro se meille! Ropeconissa käsitellään lautapelaamista niin pelisuunnittelutyöpajojen, omituisia teemoja käsittelevien luentojen kuin erikoisten turnausformaattienkin muodossa. Jos vielä epäröit, lautapelivastaava vastaa mielellään kysymyksiisi.

# Ohjelman lisäksi haemme työvoimaa lautapelitiskille, joka huolehtii pelien lainaamisesta ja kunnossa pysymisestä. Ilmoittaudu lautapelitiskin työntekijäksi täyttämällä työvoimalomake.
#                 '''.strip(),
#                 programme_form_code='events.ropecon2019.forms:LautapeliForm',
#                 num_extra_invites=0,
#                 order=60,
#             )
#         )

#         AlternativeProgrammeForm.objects.get_or_create(
#             event=self.event,
#             slug='korttipeli',
#             defaults=dict(
#                 title='Tarjoa korttipeliturnausta',
#                 short_description='Korttipeliturnaukset',
#                 description='''
# Ropecon hakee järjestäjiä korttipeliturnauksille ja korttipeliaiheiselle ohjelmalle. Tarvitsemme myös työntekijöitä korttipelitiskille vastaanottamaan turnausilmoittautumisia ja pitämään huolta siitä, että ohjelma etenee suunnitelmien mukaisesti. Kaikkea ei tarvitse tietää etukäteen, sillä neuvoja ja ohjeita työskentelyyn sekä ohjelman suunnitteluun saat korttipelivastaavalta ja kokeneemmilta turnausten järjestäjiltä. Myös korttipelitiskin työntekijät perehdytetään tehtävään.
#                 '''.strip(),
#                 programme_form_code='events.ropecon2019.forms:KorttipeliForm',
#                 num_extra_invites=0,
#                 order=40,
#             )
#         )

#         AlternativeProgrammeForm.objects.get_or_create(
#             event=self.event,
#             slug='figupeli',
#             defaults=dict(
#                 title='Tarjoa figupeliturnausta',
#                 short_description='Figut eli miniatyyripelit',
#                 description='''
# Heilutatko sivellintä kuin säilää? Pyöritätkö noppaa kuin puolijumala? Taipuuko foamboard käsissäsi upeiksi palatseiksi? Haluaisitko jakaa erikoistaitosi conikansan syville riveille?

# Figuohjelma hakee puhujia miniatyyriaiheiseen puheohjelmaan, innostuneita keskustelijoita paneelikeskusteluihin, vetäjiä työpajoihin sekä peluuttajia eri pelimuotoihin. Ideoilla – olivat ne sitten viimeisen päälle hiottua timanttia tai vasta aihioita – voit lähestyä figuvastaavaa sähköpostitse.
#                 '''.strip(),
#                 programme_form_code='events.ropecon2019.forms:FigupeliForm',
#                 num_extra_invites=0,
#                 order=50,
#             )
#         )

#         AlternativeProgrammeForm.objects.get_or_create(
#             event=self.event,
#             slug='kokemuspiste',
#             defaults=dict(
#                 title='Tarjoa kokemuspisteohjelmaa',
#                 short_description='Kokemuspiste eli tutustu peleihin',
#                 description='''
# Vuoden klassikot-teeman mukaisesti nyt on oikea hetki kaivaa kaapista se vanha perintökalleutena sukupolvelta toiselle siirtynyt klassikko ja tulla esittelemään sitä koko kansalle!

# Kokemuspisteellä kävijä pääsee tutustumaan uusiin peleihin peliesittelijän opastuksella. Haemme esittelijöitä niin vakiintuneisiin peruspeleihin (esim. Settlers of Catan, Magic: the Gathering, Warhammer, Go) kuin vielä tuntemattomiin peleihin. Peliesittelijänä pääset pelauttamaan lempipeliäsi uudelle yleisölle. Myös pelintekijät ovat tervetulleita esittelemään sekä valmiita että melkein valmiita pelejä kiinnostuneelle yleisölle. Peliesittelyiden tulee olla kestoltaan lyhyitä, alle tunnin mittaisia. Tervetulleita ovat niin figut, lautapelit, korttipelit, pöytäropet kuin larpitkin.

# Huomaathan, että Kokemuspiste on vain peliesittelyä varten. Tuotteiden myyntiä varten tulee varata osasto Ropeconin myyntialueelta.
#                 '''.strip(),
#                 programme_form_code='events.ropecon2019.forms:KokemuspisteForm',
#                 num_extra_invites=0,
#                 order=70,
#             )
#         )

        AlternativeProgrammeForm.objects.get_or_create(
            event=self.event,
            slug='default',
            defaults=dict(
                title='Tarjoa puheohjelmaa tai työpajoja',
                short_description='Puheohjelmat eli esitelmät, paneelit, jne',
                description='''
Tervetuloa tarjoamaan ohjelmaa Ropecon-kävijöille!

Tällä lomakkeella voit tarjota kaikkea ei-pelillistä ohjelmaa: puheohjelmaa, työpajoja tai muuta ohjelmaa, joka ei sovi pelien kategorioihin.

Vuoden 2019 Ropeconiin etsitään kiinnostavia ja mukaansatempaavia esitelmiä, työpajoja sekä paneelikeskusteluja erityisesti teemalla mytologia. Toivomme lisää englanninkielistä ohjelmaa, joten mainitsethan, jos pystyt vetämään ohjelmanumerosi sekä suomeksi että englanniksi. Toivomme myös lapsille ja perheille soveltuvaa ohjelmaa.

Etsimme taiteisiin, käsitöihin ja muuhun roolipelaamisen ympärillä tapahtuvaan luovaan harrastamiseen liittyvää ohjelmaa. Haemme myös lauta-, figu- ja pöytäroolipeliaiheista puheohjelmaa ja työpajoja.

Puheohjelman pituus on 45 minuuttia tai 105 minuuttia; työpaja voi olla pidempikin, 165 minuuttia. Jos ilmoitat ohjelmaan työpajan, toivomme että se järjestetään kahdesti tapahtuman aikana.

Tällä lomakkeella voi ilmoittaa myös muuta ohjelmaa, kuten taistelunäytöksen tai tanssiesityksen.

Kaiken ohjelman on noudatettava <a href="https://2019.ropecon.fi/kavijalle/hairinta/" target="_blank">Ropeconin häirinnänvastaista linjausta</a>.

Ropeconissa on myös akateeminen seminaari. Akateemiseen seminaariin on erillinen haku.
                '''.strip(),
                programme_form_code='events.ropecon2019.forms:ProgrammeForm',
                num_extra_invites=0,
                order=300,
            )
        )

        for time_slot_name in [
            'Perjantaina iltapäivällä / Friday afternoon',
            'Perjantaina illalla / Friday evening',
            'Perjantain ja lauantain välisenä yönä / Friday night',
            'Lauantaina aamupäivällä / Saturday morning',
            'Lauantaina päivällä / Saturday noon',
            'Lauantaina iltapäivällä / Saturday afternoon',
            'Lauantaina illalla / Saturday evening',
            'Lauantain ja sunnuntain välisenä yönä / Saturday night',
            'Sunnuntaina aamupäivällä / Sunday morning',
            'Sunnuntaina päivällä / Sunday noon',
        ]:
            TimeSlot.objects.get_or_create(name=time_slot_name)

    def setup_tickets(self):
        from tickets.models import TicketsEventMeta, LimitGroup, Product

        tickets_admin_group, pos_access_group = TicketsEventMeta.get_or_create_groups(self.event, ['admins', 'pos'])

        defaults = dict(
            admin_group=tickets_admin_group,
            pos_access_group=pos_access_group,
            due_days=14,
            shipping_and_handling_cents=0,
            reference_number_template="2019{:05d}",
            contact_email='Ropecon 2019 -lipunmyynti <lipunmyynti@ropecon.fi.fi>',
            ticket_free_text="Tämä on sähköinen lippusi Ropecon 2019 -tapahtumaan. Sähköinen lippu vaihdetaan rannekkeeseen\n"
                "lipunvaihtopisteessä saapuessasi tapahtumaan. Voit tulostaa tämän lipun tai näyttää sen\n"
                "älypuhelimen tai tablettitietokoneen näytöltä. Mikäli kumpikaan näistä ei ole mahdollista, ota ylös\n"
                "kunkin viivakoodin alla oleva neljästä tai viidestä sanasta koostuva Kissakoodi ja ilmoita se\n"
                "lipunvaihtopisteessä.\n\n"
                "Tervetuloa Ropeconiin!",
            front_page_text="<h2>Tervetuloa Ropeconin lippukauppaan!</h2>"
                "<p>Liput maksetaan tilauksen yhteydessä käyttämällä suomalaia verkkopankkipalveluja.</p>"
                "<p>Maksetut liput toimitetaan e-lippuina sähköpostitse asiakkaan antamaan osoitteeseen. E-liput vaihdetaan rannekkeiksi tapahtuman lipunmyyntipisteillä 27.–29.7.2019.</p>"
                "<p>Lisätietoja lipuista saat tapahtuman verkkosivuilta. <a href='https://2019.ropecon.fi/liput/'>Siirry takaisin tapahtuman verkkosivuille</a>.</p>"
                "<p>Huom! Tämä verkkokauppa palvelee ainoastaan asiakkaita, joilla on osoite Suomessa. Mikäli tarvitset "
                "toimituksen ulkomaille, ole hyvä ja ota sähköpostitse yhteyttä: <em>lipunmyynti@ropecon.fi</em>"
        )

        if self.test:
            t = now()
            defaults.update(
                ticket_sales_starts=t - timedelta(days=60),
                ticket_sales_ends=t + timedelta(days=60),
            )
        else:
            defaults.update(
                ticket_sales_starts=datetime(2019, 2, 28, 10, 0, tzinfo=self.tz),
                ticket_sales_ends=datetime(2019, 7, 26, 0, 0, tzinfo=self.tz),
            )

        meta, unused = TicketsEventMeta.objects.get_or_create(event=self.event, defaults=defaults)

        def limit_group(description, limit):
            limit_group, unused = LimitGroup.objects.get_or_create(
                event=self.event,
                description=description,
                defaults=dict(limit=limit),
            )

            return limit_group

        for product_info in [
            dict(
                name='Ropecon 2019 Early Dragon -viikonloppulippu',
                description='Sisältää pääsyn Ropecon 2019 -tapahtumaan koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=4000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Lasten Early Dragon -viikonloppulippu',
                description='Sisältää pääsyn lapselle (7-12 v) Ropecon 2019 -tapahtumaan koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=2000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Ennakkoviikonloppulippu',
                description='Sisältää pääsyn Ropecon 2019 -tapahtumaan koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=4500,
                requires_shipping=False,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Lasten ennakkoviikonloppulippu',
                description='Sisältää pääsyn lapselle (7-12 v) Ropecon 2019 -tapahtumaan koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=2500,
                requires_shipping=False,
                electronic_ticket=True,
                available=False,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Perheviikonloppulippupaketti',
                description='Sisältää pääsyn Ropecon 2019 -tapahtumaan 2 aikuiselle ja 1-3 lapselle (7-12 v) koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=9900,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Sponsoriviikonloppulippu',
                description='Sisältää pääsyn Ropecon 2019 -tapahtumaan koko viikonlopun ajan.',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=10000,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
            dict(
                name='Ropecon 2019 Akateeminen seminaari + perjantaipäivälippu',
                description='Sisältää pääsyn Akateemiseen seminaariin ja Ropecon 2019 -tapahtumaan perjantaina. Muista myös <a href="https://goo.gl/forms/J9X1401lERxaX3M52">rekisteröityä</a>!',
                limit_groups=[
                    limit_group('Pääsyliput', 9999),
                ],
                price_cents=5500,
                requires_shipping=False,
                electronic_ticket=True,
                available=True,
                ordering=self.get_ordering_number(),
            ),
        ]:
            name = product_info.pop('name')
            limit_groups = product_info.pop('limit_groups')

            product, unused = Product.objects.get_or_create(
                event=self.event,
                name=name,
                defaults=product_info
            )

            if not product.limit_groups.exists():
                product.limit_groups.set(limit_groups)
                product.save()

    def setup_payments(self):
        from payments.models import PaymentsEventMeta
        PaymentsEventMeta.get_or_create_dummy(event=self.event)

    def setup_badges(self):
        from badges.models import BadgesEventMeta

        badge_admin_group, = BadgesEventMeta.get_or_create_groups(self.event, ['admins'])
        meta, unused = BadgesEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=badge_admin_group,
                badge_layout='nick',
            )
        )

    def setup_intra(self):
        from intra.models import IntraEventMeta, Team

        admin_group, = IntraEventMeta.get_or_create_groups(self.event, ['admins'])
        organizer_group = self.event.labour_event_meta.get_group('conitea')
        meta, unused = IntraEventMeta.objects.get_or_create(
            event=self.event,
            defaults=dict(
                admin_group=admin_group,
                organizer_group=organizer_group,
            )
        )

        for team_slug, team_name in [
            ('tuottajat', 'Tuottajat'),
            ('infra', 'Infra'),
            ('palvelut', 'Palvelut'),
            ('ohjelma', 'Ohjelma'),
        ]:
            team_group, = IntraEventMeta.get_or_create_groups(self.event, [team_slug])
            Team.objects.get_or_create(
                event=self.event,
                slug=team_slug,
                defaults=dict(
                    name=team_name,
                    order=self.get_ordering_number(),
                    group=team_group,
                )
            )


class Command(BaseCommand):
    args = ''
    help = 'Setup ropecon2019 specific stuff'

    def handle(self, *args, **opts):
        Setup().setup(test=settings.DEBUG)
