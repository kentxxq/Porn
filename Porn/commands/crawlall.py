# coding:utf-8
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError
import optparse


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        parser.add_option("-i", dest="incremental", action="store_true",
                          default=False, help="enable incremental crawl")

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError(
                "Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        spider_loader = self.crawler_process.spider_loader
        for spidername in spider_loader.list():
            # python基础不好..vars这个函数都没见过,加强后续的学习。。
            # 通过vars函数把opts转换成dict字典
            # 然后*是以tuple的形式传入后续的多个值。**是以name=value的形式将字典传入函数
            # if isinstance(opts, optparse.Values):
            #     opts = vars(opts)
            # self.crawler_process.crawl(spidername, **opts)
            self.crawler_process.crawl(spidername, **vars(opts))
        self.crawler_process.start()
