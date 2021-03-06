#
#  crowley.py
#  
#  Copyright 2020 Gabriel "bsd0x" Dutra <root@bsd0x.me>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import click

from lib.crawler import google
from lib.banner import banner
from vull import sql_injection
from vull import reporting
from multiprocessing.dummy import Pool as ThreadPool

@click.command()
@click.option('--dork', nargs=1)
@click.option('--max_results', default=100, nargs=1, type=click.INT)
@click.option('--timeout', default=3, nargs=1, type=click.INT)
@click.option('--threads', default=1, nargs=1, type=click.INT)
def main(dork, max_results, timeout, threads):

    search = google.SearchGoogle(dork, max_results, timeout)
    google_results = search.search_results()
    sqli = sql_injection.SqlInjection(timeout)
    report = reporting.ReportVulnerabilities()

    thread_pool = ThreadPool(threads)

    results = thread_pool.map(sqli.check_vull, google_results)
    thread_pool.close()
    thread_pool.join()

    report.create_report()

if __name__=='__main__':
    banner.banner()
    main()
