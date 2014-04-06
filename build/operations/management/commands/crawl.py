
#python imports
import sys

#django imports
from django.core.management.base import BaseCommand, CommandError

#crawler imports
sys.path.append('/home/ec2-user/bblio/scraper/')
import scrapeController

class Command(BaseCommand):
    site_id = 0
    def handle(self, *args, **options):
        print args[0]
        scrapeController.run_site_id(args[0])
        try:
            scrapeController.run_site_id(args[0])
        except:
            raise CommandError('Cannot crawl site id %s' % str(args[0]))
        self.stdout.write('[Management Command] Crawling site id %s' % str(args[0]))
